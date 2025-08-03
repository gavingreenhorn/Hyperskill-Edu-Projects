package server;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileHandler {
    private static final String SAVE_DIR = "/server/data/";
    private String content;
    private final Path path;

    public FileHandler(String filename) {
        this.path = Path.of(System.getProperty("user.dir"), "src", SAVE_DIR, filename);
    }

    public String getContent() {
        return content;
    }

    public boolean put(String content) throws IOException {
        if (Files.exists(path)) {
            return false;
        }
        Files.createDirectories(path.getParent());
        Files.createFile(path.toAbsolutePath());
        Files.writeString(path, content, StandardCharsets.UTF_8);
        return true;
    }

    public boolean get() throws IOException {
        if (!Files.exists(path)) {
            return false;
        }
        content = Files.readString(path, StandardCharsets.UTF_8);
        return true;
    }

    public boolean del() throws IOException {
        return Files.deleteIfExists(path);
    }
}
