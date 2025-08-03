package client;

import Config.Config;
import Models.StatusCode;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    private static final String INPUT_ERROR = "Invalid input supplied:";
    private static final String INVALID_RESPONSE = "Incorrect response format: %s";
    private static final String ALLOWED_ACTIONS = "1 - get a file, 2 - save a file, 3 - delete a file";
    private static final String GET_BY_OPTIONS = "1 - name, 2 - id";
    private static final String ACTION_PROMPT = "Enter action (%s): ".formatted(ALLOWED_ACTIONS);
    private static final String GET_BY_PROMPT = "Do you want to %s the file by name or by id (%s): ".formatted("get", GET_BY_OPTIONS);
    private static final String DELETE_BY_PROMPT = "Do you want to %s the file by name or by id (%s): ".formatted("delete", GET_BY_OPTIONS);
    private static final String LOCAL_FILE_PROMPT = "Enter name of the file: ";
    private static final String SAVE_NAME_PROMPT = "Enter name of the file to be saved on server: ";
    private static final String INVALID_INPUT = "%s allowed actions: %s".formatted(INPUT_ERROR, ALLOWED_ACTIONS);
    private static final String INVALID_OPTION = "%s allowed options: %s".formatted(INPUT_ERROR, GET_BY_OPTIONS);
    private static final String FILE_NOT_FOUND = "The response says that this file is not found!";
    private static final String FILE_DELETED = "The response says that this file was deleted successfully!";
    private static final String FILE_DOWNLOADED = "The file was downloaded! Specify a name for it: ";
    private static final String FILE_SAVED_SERVER = "Response says that file is saved! ID = %s";
    private static final String FILE_SAVED_CLIENT = "File saved on the hard drive!";
    private static final String FILE_SAVE_FORBIDDEN = "The response says that creating the file was forbidden!";
    String ipAddress;
    int port;

    private static void sendBytes(byte[] payload, DataOutputStream output) {
        try {
            output.writeInt(payload.length);
            output.write(payload);
        }
        catch (IOException ie) {
            throw new RuntimeException(ie.getMessage());
        }
    }

    private static int resolveInput(String input) {
        if (input.equals("exit"))
            return 0;
        else if (input.isEmpty() || !input.matches("[123]"))
            throw new IllegalArgumentException(INVALID_INPUT);
        else return Integer.parseInt(input);
    }

    private static int resolveIdOption(String input) {
        if (input.isEmpty() || !input.matches("[12]"))
            throw new IllegalArgumentException(INVALID_OPTION);
        return Integer.parseInt(input);
    }

    private static String resolvePayload(String method, int option, String identifier) {
        return switch (option) {
            case 1 -> "%s BY_NAME %s".formatted(method, identifier);
            case 2 -> "%s BY_ID %s".formatted(method, identifier);
            default -> throw new IllegalStateException("Unexpected get option");
        };
    }

    public Client(String ipAddress, int port) {
        this.ipAddress = ipAddress;
        this.port = port;
    }

    public void run() {
        try (
                Scanner sc = new Scanner(System.in);
                Socket socket = new Socket(InetAddress.getByName(ipAddress), port);
                DataInputStream input = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                DataOutputStream output = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()))
        ) {
            System.out.print(ACTION_PROMPT);
            int actionCode = resolveInput(sc.nextLine());
            switch (actionCode) {
                case 0 -> output.writeUTF(Config.EXIT_CODE);
                case 1 -> {
                    System.out.print(GET_BY_PROMPT);
                    int get_option = resolveIdOption(sc.nextLine());
                    System.out.printf("Enter %s: ", get_option == 1 ? "name" : "id");
                    String identifier = sc.nextLine();
                    String payload = resolvePayload("GET", get_option, identifier);
                    output.writeUTF(payload);
                }
                case 2 -> {
                    System.out.print(LOCAL_FILE_PROMPT);
                    String local_name = sc.nextLine();
                    System.out.print(SAVE_NAME_PROMPT);
                    String server_name = sc.nextLine();
                    if (server_name.isBlank()) server_name = local_name;
                    output.writeUTF("PUT %s".formatted(server_name));
                    sendBytes(new ClientFileHandler(local_name).readBytes(), output);
                }
                case 3 -> {
                    System.out.print(DELETE_BY_PROMPT);
                    int get_option = resolveIdOption(sc.nextLine());
                    System.out.printf("Enter %s: ", get_option == 1 ? "name" : "id");
                    String identifier = sc.nextLine();
                    String payload = resolvePayload("DELETE", get_option, identifier);
                    output.writeUTF(payload);
                }
            }
            output.flush();
            System.out.println("The request was sent.");
            if (actionCode == 0) return;
            String response = input.readUTF();
            switch (actionCode) {
                case 1 -> {
                    if (response.equals(String.valueOf(StatusCode.NotFound))) {
                        System.out.println(FILE_NOT_FOUND);
                    }
                    else {
                        System.out.println(FILE_DOWNLOADED);
                        String name = sc.nextLine();
                        new ClientFileHandler(name).write(response.split(" ")[1]);
                        System.out.println(FILE_SAVED_CLIENT);
                    }
                }
                case 2 -> {
                    if (response.equals(String.valueOf(StatusCode.GTFO))) {
                        System.out.println(FILE_SAVE_FORBIDDEN);
                    }
                    else {
                        String[] responseParts = response.split(" ");
                        if (responseParts.length != 2 || Integer.parseInt(responseParts[0]) != StatusCode.OK) {
                            throw new IllegalStateException(INVALID_RESPONSE.formatted(response));
                        }
                        System.out.println(FILE_SAVED_SERVER.formatted(responseParts[1]));
                    }
                }
                case 3 -> System.out.println(Integer.parseInt(response) == StatusCode.OK
                        ? FILE_DELETED
                        : FILE_NOT_FOUND);
            }
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
