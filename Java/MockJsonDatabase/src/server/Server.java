package server;

import Models.*;
import com.google.gson.Gson;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class Server {
    private final Map<String, String> MUCH_DATA = new HashMap<>();
    private final String ipAddress;
    private final int port;

    public Server(String ipAddress, int port) {
        this.port = port;
        this.ipAddress = ipAddress;
    }

    private Response getResponse(Request request) {
        try {
            return request.getCommand().execute(MUCH_DATA, request.getKey(), request.getValue());
        }
        catch (RuntimeException e) {
            return new Response(Config.ERROR_STATUS, e.getMessage());
        }
    }

    private Request acceptRequest(DataInputStream input, Gson gson) throws IOException {
        String jason = input.readUTF();
        System.out.println("Received: %s".formatted(jason));
        return gson.fromJson(jason, Request.class);
    }

    private void sendResponse(DataOutputStream output, Response response, Gson gson) throws IOException {
        String jason = gson.toJson(response);
        output.writeUTF(jason);
        System.out.println("Sent: %s".formatted(jason));
    }

    private void saveToDB(Lock lock, Gson gson) throws IOException {
        lock.lock();
        Files.writeString(
            Config.DB_LOCAL_PATH,
            gson.toJson(MUCH_DATA),
            StandardCharsets.UTF_8,
            StandardOpenOption.CREATE,
            StandardOpenOption.TRUNCATE_EXISTING,
            StandardOpenOption.WRITE
            );
        lock.unlock();
    }

    public void run() {
        System.out.println("Server started!");
        ReadWriteLock lock = new ReentrantReadWriteLock(true);
        Lock writeLock = lock.writeLock();
        AtomicBoolean running = new AtomicBoolean(true);
        try (
            ServerSocket server = new ServerSocket(port);
            ExecutorService exec = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())
        )
        {
            while (running.get()) {
                Socket socket = server.accept();
                Gson gson = new Gson();
                exec.execute(
                    new Thread(() -> {
                        try (
                            DataInputStream input = new DataInputStream(socket.getInputStream());
                            DataOutputStream output = new DataOutputStream(socket.getOutputStream())
                        ) {
                            Request request = acceptRequest(input, gson);
                            Response response = getResponse(request);

                            sendResponse(output, response, gson);
                            if (request.getCommand() == Command.SET) {
                                saveToDB(writeLock, gson);
                            }
                            else if (request.getCommand() == Command.EXIT) {
                                running.set(false);
                                server.close();
                            }
                        }
                        catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    })
                );
            }
        } catch (UnknownHostException uhe) {
            throw new RuntimeException("Cannot resolve the IP %s".formatted(ipAddress));
        } catch (IOException ioe) {
            throw new RuntimeException(ioe.getMessage());
        }
    }
}

