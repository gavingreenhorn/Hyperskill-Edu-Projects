package contacts;

import utils.Constants;
import console.Menu;

import java.io.*;
import java.nio.file.Path;

public class App {
    private File storage = null;

    App() {}

    App(String filepath) {
        storage = Path.of(System.getProperty("user.dir"), "src", filepath).toFile();
        if (!storage.exists()) {
            storage = new File(Constants.DEFAULT_STORAGE_NAME);
        }
    }

    public void roll() {
        Menu menu = new Menu(new StorageCaretaker(storage));
        menu.run();
    }
}
