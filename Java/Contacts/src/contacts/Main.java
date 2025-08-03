package contacts;

public class Main {
    public static void main(String[] args) {
        App app;
        if (args.length > 0 && !args[0].isBlank()) {
            app = new App(args[0]);
        }
        else {
            app = new App();
        }
        app.roll();
    }
}