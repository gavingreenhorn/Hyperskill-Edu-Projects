package server;

import Models.Config;

public class Main {
    public static void main(String[] args) {
        Server server = new Server(Config.IP_ADDRESS, Config.PORT);
        server.run();
    }
}
