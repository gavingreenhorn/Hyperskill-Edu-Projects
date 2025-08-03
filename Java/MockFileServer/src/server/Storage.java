package server;

import Config.Config;

import java.io.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class Storage extends ConcurrentHashMap<Integer, String> implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private static final AtomicInteger nextKey = new AtomicInteger(0);

    public static synchronized Storage load() {
        File map = Config.getFileMapPath().toFile();
        if (map.exists()) {
            try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(map))) {
                return (Storage)ois.readObject();
            } catch (IOException | ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
        else return new Storage();
    }

    public synchronized int add(String path) {
        super.put(nextKey.get(), path);
        save();
        return nextKey.getAndIncrement();
    }

    public synchronized void removeEntry(int key) {
        save();
        super.remove(key);
    }

    private synchronized void save() {
        File map = Config.getFileMapPath().toFile();
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(map))) {
            oos.writeObject(this);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
