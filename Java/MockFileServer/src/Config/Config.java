package Config;

import java.nio.file.Path;

public class Config {
    public static final String EXIT_CODE = "ABANDON ALL SHIPS";
    public static final String SERVER_DIR = "/server/data/";
    public static final String CLIENT_DIR = "/client/data/";
    public static final String FILE_MAP_NAME = "filemap.txt";
    public static final String IP_ADDRESS = "127.0.0.1";
    public static final int PORT = 12345;

    public static Path getFileMapPath() {
        return Path.of(System.getProperty("user.dir"), "src", SERVER_DIR, FILE_MAP_NAME);
    }

    public static Path getAbsoluteSaveDir(String dir) {
        return Path.of(System.getProperty("user.dir"), "src", dir);
    }
}
