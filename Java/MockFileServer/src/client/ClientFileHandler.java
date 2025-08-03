package client;

import Config.Config;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;

public class ClientFileHandler {

    private final Path path;

    ClientFileHandler(String filename) {
        this.path = Config.getAbsoluteSaveDir(Config.CLIENT_DIR).resolve(filename);
    }

    public byte[] readBytes() {
        try (BufferedInputStream stream = new BufferedInputStream(new FileInputStream(path.toAbsolutePath().toString()))) {
            return stream.readAllBytes();
        }
        catch (IOException ie) {
            throw new RuntimeException(ie.getMessage());
        }
    }

    public void write(String encoded) {
        try (BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream(path.toFile()))) {
            //System.out.println(encoded);
            stream.write(Base64.getDecoder().decode(encoded));
            stream.flush();
            System.out.println(Files.readString(path));
        }
        catch (IOException ie) {
            throw new RuntimeException(ie.getMessage());
        }
    }
}
