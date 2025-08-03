package utils;

public interface ContactType {
    String PERSON = "person";
    String ORG = "organization";

    static String getContactTypes() {
        return String.join(", ", PERSON, ORG);
    }
}
