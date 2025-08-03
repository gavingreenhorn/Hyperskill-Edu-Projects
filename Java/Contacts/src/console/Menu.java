package console;

import java.util.List;
import java.util.Scanner;

import contacts.StorageCaretaker;
import utils.*;
import models.Contacts;
import static models.Contacts.*;

public class Menu {
    private final StorageCaretaker caretaker;
    private Contacts contacts;

    public Menu(StorageCaretaker caretaker) {
        this.caretaker = caretaker;
    }

    public void run() {
        contacts = caretaker.getContacts();
        ContactBuilder builder;
        try (Scanner sc = new Scanner(System.in)) {
            boolean loop = true;
            while (loop) {
                System.out.printf(Prompts.ROOT_MENU, Actions.getRootMenuActions());
                switch (sc.nextLine()) {
                    case Actions.EXIT -> loop = false;
                    case Actions.ADD -> {
                        try {
                            System.out.printf(Prompts.CONTACT_TYPE, ContactType.getContactTypes());
                            builder = contacts.getBuilder(sc.nextLine());
                            switch (builder) {
                                case PersonBuilder personBuilder -> {
                                    System.out.println("Enter the name: ");
                                    personBuilder.setName(sc.nextLine());
                                    System.out.println("Enter the surname: ");
                                    personBuilder.setSurname(sc.nextLine());
                                    System.out.println("Enter the birth date: ");
                                    personBuilder.setBirthDate(sc.nextLine());
                                    System.out.println("Enter the gender (M, F): ");
                                    personBuilder.setGender(sc.nextLine());
                                }
                                case OrganizationBuilder organizationBuilder -> {
                                    System.out.println("Enter the organization name: ");
                                    organizationBuilder.setName(sc.nextLine());
                                    System.out.println("Enter the address: ");
                                    organizationBuilder.setAddress(sc.nextLine());
                                }
                            }
                            System.out.println(Prompts.NUMBER);
                            builder.setPhoneNumber(sc.nextLine());
                            contacts.addContact(builder.build());
                            System.out.println(Messages.RECORD_ADDED);
                            caretaker.saveState();
                        } catch (IllegalArgumentException ex) {
                            System.out.println(ex.getMessage());
                        }

                    }
                    case Actions.SEARCH -> runSearch(sc);
                    case Actions.LIST -> runList(sc);
                    case Actions.COUNT ->
                        System.out.println(Messages.CONTACT_COUNT.formatted(contacts.getContactCount()));
                    default -> throw new IllegalArgumentException(Errors.UNSUPPORTED);
                }
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void runRecordMenu(Contact contact, Scanner sc) {
        String action;
        boolean run = true;
        while (run) {
            System.out.printf(Prompts.RECORD_MENU, Actions.getRecordMenuActions());
            action = sc.nextLine();
            switch (action) {
                case Actions.EDIT -> {
                    System.out.printf(Prompts.EDIT, contact.getContactFields());
                    String fieldName = sc.nextLine();
                    System.out.printf("Enter %s: ", fieldName);
                    String fieldValue = sc.nextLine();
                    try {
                        contacts.editContact(contact, fieldName, fieldValue);
                        caretaker.saveState();
                        System.out.println(Messages.SAVED);
                        contacts.printContactCard(contact);
                    }
                    catch (IllegalArgumentException ex) {
                        System.out.println(ex.getMessage());
                    }
                }
                case Actions.DELETE -> {
                    contacts.deleteContact(contact);
                    System.out.println(Messages.DELETED);
                }
                case Actions.MENU -> run = false;
                default -> throw new IllegalArgumentException(Errors.UNSUPPORTED);
            }
        }
    }

    private int resolveIndex(String action, int count) {
        try {
            int idx = Integer.parseInt(action);
            if (idx != 0 && idx > count) {
                throw new RuntimeException(Errors.NOT_IN_CONTACTS.formatted(idx, contacts.getContactCount()));
            }
            return idx - 1;
        }
        catch (NumberFormatException nfe) {
            throw new RuntimeException(Errors.INVALID_NUMBER.formatted(action, contacts.getContactCount()));
        }
    }

    private void runListMenu(Scanner sc) {
        System.out.println(Prompts.LIST_MENU);
        String action = sc.nextLine();
        if (action.equals(Actions.BACK)) {
            return;
        }
        Contact contact = contacts.getContact(resolveIndex(action, contacts.getContactCount()));
        contacts.printContactCard(contact);
        runRecordMenu(contact, sc);
    }

    private void runSearchMenu(List<Contact> found, Scanner sc) {
        System.out.print(Prompts.SEARCH_MENU);
        String action = sc.nextLine();
        switch (action) {
            case Actions.BACK -> {}
            case Actions.AGAIN -> runSearch(sc);
            default -> {
                Contact contact = found.get(resolveIndex(action, found.size()));
                contacts.printContactCard(contact);
                runRecordMenu(contact, sc);
            }
        }
    }

    private void runSearch(Scanner sc) {
        System.out.println(Prompts.QUERY);
        String inputPattern = sc.nextLine();
        List<Contact> found = contacts.filterContacts(inputPattern);
        if (found.isEmpty()) {
            System.out.println(Messages.NONE_FOUND.formatted(inputPattern));
            return;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < found.size(); i++) {
            sb.append("%s. %s\n".formatted(i+1, found.get(i)));
        }
        System.out.println(sb.toString().trim());
        runSearchMenu(found, sc);
    }

    private void runList(Scanner sc) {
        if (contacts.getContactCount() > 0) {
            System.out.println(contacts);
            runListMenu(sc);
        }
        else {
            System.out.println(Messages.CONTACT_COUNT.formatted("no"));
        }
    }
}
