package server;

import Config.Config;
import Models.Method;
import Models.Request;
import Models.Response;
import Models.StatusCode;

import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

public class FileServer {
    private static final String WELCOME_MESSAGE = "Server started!";
    private static final String NO_ID = "File identifier type was not provided";
    private static final String UNKNOWN_ID_TYPE = "Unrecognized identifier type: %s";
    private static final String UNDEFINED_VERB = "Verb %s is not defined";
    private static final String UNRESOLVED_IP = "Unable to resolve IP address '%s'\r\n%s";
    private final String ipAddress;
    private final int port;

    public FileServer(int port) {
        this.ipAddress = Config.IP_ADDRESS;
        this.port = port;
    }

    public FileServer(String ipAddress, int port) {
        this.port = port;
        this.ipAddress = ipAddress;
    }

    private boolean processGet(ServerFileHandler fileHandler, int id) {
        fileHandler.setTarget(id);
        return fileHandler.get();
    }

    private boolean processGet(ServerFileHandler fileHandler, String id) {
        fileHandler.setTarget(id);
        return fileHandler.get();
    }

    private boolean processDelete(ServerFileHandler fileHandler, int id) {
        fileHandler.setTarget(id);
        return fileHandler.del();
    }

    private boolean processDelete(ServerFileHandler fileHandler, String id) {
        fileHandler.setTarget(id);
        return fileHandler.del();
    }

    private boolean processById(Request request, ServerFileHandler fileHandler) {
        if (request.by.isEmpty()) {
            throw new IllegalArgumentException(NO_ID);
        }
        return switch (request.method) {
            case Method.GET -> switch (request.by) {
                case "BY_ID" -> processGet(fileHandler, Integer.parseInt(request.id));
                case "BY_NAME" -> processGet(fileHandler, request.id);
                default -> throw new IllegalArgumentException(UNKNOWN_ID_TYPE.formatted(request.by));
            };
            case Method.DELETE -> switch (request.by) {
                case "BY_ID" -> processDelete(fileHandler, Integer.parseInt(request.id));
                case "BY_NAME" -> processDelete(fileHandler, request.id);
                default -> throw new IllegalArgumentException(UNKNOWN_ID_TYPE.formatted(request.by));
            };
            default -> throw new IllegalArgumentException(UNDEFINED_VERB.formatted(request.method));
        };
    }

    private boolean processPut(Request request, ServerFileHandler fileHandler, DataInputStream input) throws IOException {
        fileHandler.setTarget(request.id);
        int length = input.readInt();
        byte[] payload = new byte[length];
        input.readFully(payload, 0, payload.length);
        return fileHandler.put(payload);
    }

    private Response getResponse(Request request, DataInputStream input) throws IOException {
        ServerFileHandler fileHandler = new ServerFileHandler();
        return switch (request.method) {
            case Method.GET -> processById(request, fileHandler) ?
                    new Response(StatusCode.OK, fileHandler.getContent())
                    : new Response(StatusCode.NotFound);
            case Method.DELETE -> new Response(
                    processById(request, fileHandler) ?
                    StatusCode.OK : StatusCode.NotFound);
            case Method.PUT -> new Response(
                    processPut(request, fileHandler, input) ?
                    StatusCode.OK : StatusCode.GTFO, fileHandler.getId());
            default -> throw new IllegalArgumentException(UNDEFINED_VERB.formatted(request.method));
        };
    }

    public void run() {
        System.out.println(WELCOME_MESSAGE);
        AtomicBoolean running = new AtomicBoolean(true);
        try (
            ServerSocket server = new ServerSocket(port);
            ExecutorService exec = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())
        ) {
            while (running.get()) {
                Socket socket = server.accept();
                exec.execute(
                    new Thread(() -> {
                        try (
                            DataInputStream input = new DataInputStream(socket.getInputStream());
                            DataOutputStream output = new DataOutputStream(socket.getOutputStream())
                        ) {
                            String request_input = input.readUTF();
                            if (request_input.equals(Config.EXIT_CODE)) {
                                running.set(false);
                                server.close();
                                return;
                            }
                            Request request = new Request(request_input);
                            output.writeUTF(getResponse(request, input).toString());
                        } catch (IOException e) {
                            throw new RuntimeException(e.getMessage());
                        }
                    })
                );
            }
        } catch (UnknownHostException uhe) {
            throw new RuntimeException(UNRESOLVED_IP.formatted(ipAddress, uhe.getMessage()));
        } catch (IOException ioe) {
            throw new RuntimeException(ioe.getMessage());
        }
    }
}
