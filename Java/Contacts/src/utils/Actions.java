package utils;

public interface Actions {
    String EXIT = "exit";
    String ADD = "add";
    String EDIT = "edit";
    String DELETE = "delete";
    String SEARCH = "search";
    String LIST = "list";
    String COUNT = "count";
    String MENU = "menu";
    String BACK = "back";
    String AGAIN = "again";

    static String getRootMenuActions() {
        return String.join(", ", ADD, LIST, SEARCH, COUNT, EXIT);
    }

    static String getRecordMenuActions() {
        return String.join(", ", EDIT, DELETE, MENU);
    }
}
