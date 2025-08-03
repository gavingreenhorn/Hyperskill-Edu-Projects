package server;

import Config.Config;

public class Main {
    public static void main(String[] args) {
        FileServer server = new FileServer(Config.PORT);
        server.run();
    }
}