package models;

import utils.Contact;
import utils.ContactType;
import utils.Errors;

import java.io.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import static java.util.regex.Pattern.CASE_INSENSITIVE;

public class Contacts {
    private final List<Contact> contactList;
    private PersonBuilder personBuilderInstance = null;
    private OrganizationBuilder organizationBuilderInstance = null;

    public Contacts() {
        contactList = new ArrayList<>();
    }

    public Contacts(State state) {
        contactList = state.getContactList();
    }

    @Override
    public String toString() {
        int limit = Math.min(contactList.size(), 10);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < limit; i++) {
            sb.append("%s. %s\n".formatted(i+1, contactList.get(i)));
        }
        return sb.toString().trim();
    }

    public State getState() {
        return new State(new ArrayList<>(contactList));
    }

    private PersonBuilder getPersonBuilderInstance() {
        if (personBuilderInstance == null) {
            personBuilderInstance = new PersonBuilder();
        }
        return personBuilderInstance;
    }

    private OrganizationBuilder getOrganizationBuilderInstance() {
        if (organizationBuilderInstance == null) {
            organizationBuilderInstance = new OrganizationBuilder();
        }
        return organizationBuilderInstance;
    }

    public ContactBuilderImpl getBuilder(String of) {
        return switch (of) {
            case ContactType.ORG -> getOrganizationBuilderInstance();
            case ContactType.PERSON -> getPersonBuilderInstance();
            default -> throw new IllegalArgumentException(Errors.NO_SUCH_BUILDER.formatted(of));
        };
    }

    public int getContactCount() {
        return contactList.size();
    }

    public void addContact(Contact contact) {
        contactList.add(contact);
    }

    public Contact getContact(int index) {
        return contactList.get(index);
    }

    public List<Contact> filterContacts(String input) {
        Pattern pattern = Pattern.compile(input, CASE_INSENSITIVE);
        return contactList.stream().filter(x -> pattern.matcher(((ContactImpl)x).getSearchableData()).find()).toList();
    }

    public void editContact(Contact contact, String fieldName, Object newValue) {
        if (fieldName.equals("birth") && !((String)newValue).isBlank()) {
            newValue = LocalDate.parse((CharSequence)newValue);
        }
        ((ContactImpl)contact).editField(fieldName, newValue);
    }

    public void printContactCard(Contact contact) {
        System.out.println(((ContactImpl)contact).getContactCard());
    }

    public void deleteContact(Contact contact) {
        contactList.remove(contact);
    }

    public static class State implements Serializable {
        @Serial
        private static final long serialVersionUID = 1L;
        private final List<Contact> contactList;

        public State(List<Contact> contactList) {
            this.contactList = contactList;
        }

        private List<Contact> getContactList() {
            return new ArrayList<>(contactList);
        }
    }

    public sealed interface ContactBuilder
        permits Contacts.ContactBuilderImpl {
        void setName(String name);
        void setPhoneNumber(String phoneNumber);
        Contact build();
    }

    abstract static sealed class ContactBuilderImpl implements ContactBuilder {
        protected ContactImpl contact;

        ContactBuilderImpl() {
            reset();
        }

        abstract void reset();

        public void setName(String name) {
            this.contact.setName(name);
        }

        public void setPhoneNumber(String name) {
            this.contact.setPhoneNumber(name);
        }

        public Contact build() {
            Contact contact = this.contact;
            reset();
            return contact;
        }
    }

    static public final class PersonBuilder extends ContactBuilderImpl {
        void reset() {
            contact = new Person();
        }

        public void setSurname(String name) {
            ((Person)this.contact).setSurname(name);
        }

        public void setGender(String gender) {
            if (!gender.isBlank()) {
                ((Person)this.contact).setGender(gender.charAt(0));
            }
        }

        public void setBirthDate(String dateString) {
            LocalDate date = null;
            if (!dateString.isBlank()) {
                date = LocalDate.parse(dateString);
            }
            ((Person)this.contact).setBirthDate(date);
        }
    }

    static public final class OrganizationBuilder extends ContactBuilderImpl {
        void reset() {
            contact = new Organization();
        }

        public void setAddress(String address) {
            ((Organization)this.contact).setAddress(address);
        }
    }
}
