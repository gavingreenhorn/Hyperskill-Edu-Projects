package contacts;

import models.Contacts;

import java.io.*;

public class StorageCaretaker {
    File file;
    Contacts contacts;

    public StorageCaretaker(File file) {
        this.file = file;
    }

    public Contacts getContacts() {
        if (contacts == null) {
            if (file == null) {
                contacts = new Contacts();
            } else {
                try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(file))) {
                    contacts = new Contacts((Contacts.State)ois.readObject());
                } catch (IOException | ClassNotFoundException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return contacts;
    }

    public void saveState() {
        if (file != null) {
            try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(file))) {
                oos.writeObject(getContacts().getState());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
}

