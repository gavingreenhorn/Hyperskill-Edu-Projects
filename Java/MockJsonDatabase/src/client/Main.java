package client;

import com.beust.jcommander.JCommander;

public class Main {
    public static void main(String[] args) {
        Args jarg = new Args();
        JCommander.newBuilder()
            .addObject(jarg)
            .build()
            .parse(args);
        Client client = new Client(jarg);
        client.run();
    }
}
