package Models;

import java.lang.reflect.Type;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.gson.*;
import com.google.gson.annotations.JsonAdapter;

@JsonAdapter(RequestAdapter.class)
public class Request {
    private static final Pattern VALID_REQUEST_PATTERN = Pattern.compile("^" +
        "(?<command>set|get|delete)" +
        " (?<key>\\p{Alnum}+)" +
        "(?: (?<value>.+))?"
    );
    private final Command command;
    private final String key;
    private final String value;

    public Request(String type, String key, String value) {
        this.command = Command.fromName(type);
        this.key = key;
        this.value = value;
    }

    public Request(String input) {
        Matcher matcher = VALID_REQUEST_PATTERN.matcher(input);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("Invalid input string: %s".formatted(input));
        }
        this.command = Command.fromName(matcher.group("command"));
        this.key = matcher.group("key");
        this.value = command == Command.SET ? matcher.group("value") : null;
    }

    public Command getCommand() {
        return command;
    }

    public String getKey() {
        return key;
    }

    public String getValue() {
        return value;
    }
}

class RequestAdapter implements JsonSerializer<Request>, JsonDeserializer<Request> {
    @Override
    public JsonElement serialize(Request request, Type typeOfSrc, JsonSerializationContext context) {
        JsonObject jason = new JsonObject();
        Command command = request.getCommand();
        jason.add("type", context.serialize(command));
        if (command == Command.EXIT) {
            return jason;
        }
        jason.addProperty("key", request.getKey());
        if (command == Command.SET && request.getValue() != null) {
            jason.addProperty("value", request.getValue());
        }
        return jason;
    }

    @Override
    public Request deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context)
        throws JsonParseException {
        JsonObject jason = json.getAsJsonObject();
        return new Request(
            jason.get("type").getAsString(),
            jason.has("key") ? jason.get("key").getAsString() : null,
            jason.has("value") ? jason.get("value").getAsString() : null
        );
    }
}