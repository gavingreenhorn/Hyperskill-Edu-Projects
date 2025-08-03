package server;
import Config.Config;

import java.io.*;
import java.nio.file.Path;
import java.util.Map;

public class ServerFileHandler {
    private byte[] content;
    private final Path savePath;
    private Integer id;
    private File target;
    private final Storage fileMapping;

    public ServerFileHandler() {
        this.savePath = Config.getAbsoluteSaveDir(Config.SERVER_DIR);
        this.fileMapping = Storage.load();
        this.target = null;
    }

    public void setTarget(String fileName) {
        this.target = savePath.resolve(fileName).toFile();
    }

    public void setTarget(int id) {
        this.id = id;
        this.target = fileMapping.containsKey(id) ? savePath.resolve(fileMapping.get(id)).toFile() : null;
    }

    public boolean put(byte[] content) throws IOException {
        if (target.exists()) {
            return false;
        }
        try (FileOutputStream fos = new FileOutputStream(target)) {
            fos.write(content);
            this.id = fileMapping.add(target.getName());
            return true;
        }
    }

    public boolean get() {
        if (target == null || !target.exists()) {
            return false;
        }
        try (BufferedInputStream stream = new BufferedInputStream(new FileInputStream(target))) {
            content = stream.readAllBytes();
        }
        catch (IOException ie) {
            throw new RuntimeException(ie.getMessage());
        }
        return true;
    }

    public boolean del() {
        if (!target.exists()) {
            return false;
        }
        for (Map.Entry<Integer, String> kv : fileMapping.entrySet()) {
            if (kv.getValue().equals(target.getName())) {
                fileMapping.removeEntry(kv.getKey());
            }
        }
        return target.delete();
    }

    public byte[] getContent() {
        return content != null ? content : null;
    }

    public String getId() {
        return id != null ? String.valueOf(id) : null;
    }
}
