package utils;

public interface Errors {
    String UNSUPPORTED = "No such action defined";
    String INVALID_NUMBER = "Invalid option selected (%s): only numbers 1 to %d are accepted";
    String NOT_IN_CONTACTS = "Selected number is not in contacts: %d ∉ 1-%d";
    String NO_SUCH_BUILDER = "Unexpected builder class: %s";
    String NO_SUCH_FIELD = "No such field: %s";
    String WRONG_NUMBER = "Wrong phone number format!";
}
