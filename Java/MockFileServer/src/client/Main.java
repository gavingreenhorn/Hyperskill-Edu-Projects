package client;

import Config.Config;

public class Main {
    public static void main(String[] args) {
        Client client = new Client(Config.IP_ADDRESS, Config.PORT);
        client.run();
    }
}
