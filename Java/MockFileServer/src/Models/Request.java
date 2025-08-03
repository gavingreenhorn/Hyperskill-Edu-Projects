package Models;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Request {
    private static final Pattern OPERATION_PATTERN = Pattern.compile("^" +
            "(?<method>PUT|GET|DELETE)" +
            "(?: (?<by>BY_ID|BY_NAME))?" +
            " (?<id>.+)");
    public final String method;
    public final String by;
    public final String id;

    public Request(String input) {
        Matcher matcher = OPERATION_PATTERN.matcher(input);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("Invalid input string: %s".formatted(input));
        }
        this.method = matcher.group("method");
        boolean requiresIdentifierType = method.matches("GET|DELETE");
        this.by = requiresIdentifierType ? matcher.group("by") : null;
        this.id = matcher.group("id");
    }
}
