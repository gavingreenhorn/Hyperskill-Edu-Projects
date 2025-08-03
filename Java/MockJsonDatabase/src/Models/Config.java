package Models;

import java.nio.file.Path;

public interface Config {
    String BASE_DIR = System.getProperty("user.dir");
    Path CLIENT_INPUT_DIR = Path.of(BASE_DIR, "/src/client/data/");
    Path DB_LOCAL_PATH = Path.of(BASE_DIR, "/src/server/data/db.json");
    String IP_ADDRESS = "127.0.0.1";
    String OK_STATUS = "OK";
    String ERROR_STATUS = "ERROR";
    String NO_SUCH_KEY_REASON = "No such key";
    int PORT = 12345;
}
