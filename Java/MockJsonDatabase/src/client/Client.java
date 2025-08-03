package client;

import Models.Config;
import Models.Request;
import com.google.gson.Gson;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

public class Client {
    Args jarg;
    String ipAddress;
    int port;

    public Client(Args args) {
        this.jarg = args;
        this.ipAddress = Config.IP_ADDRESS;
        this.port = Config.PORT;
    }

    private void sendRequest(DataOutputStream output, Request request, String payload) throws IOException {
        System.out.println("Sent: %s".formatted(payload));
        output.writeUTF(payload);
        output.flush();
    }

    private String readLocalFile(String filename) throws IOException {
        return Files.readString(
            Config.CLIENT_INPUT_DIR.resolve(filename),
            StandardCharsets.UTF_8
        );
    }

    public void run() {
        try (
            Socket socket = new Socket(InetAddress.getByName(ipAddress), port);
            DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
            DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()))
        ) {
            System.out.println("Client started!");
            Gson gson = new Gson();
            Request request = jarg.in != null
                ? gson.fromJson(readLocalFile(jarg.in), Request.class)
                : new Request(jarg.type, jarg.key, jarg.value);
            sendRequest(output, request, gson.toJson(request));
            String response = input.readUTF();
            System.out.println("Received: %s".formatted(response));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
