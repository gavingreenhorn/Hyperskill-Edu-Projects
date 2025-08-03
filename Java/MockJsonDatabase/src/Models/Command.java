package Models;

import com.google.gson.annotations.SerializedName;

import java.util.Map;

public enum Command {
    @SerializedName(Commands.GET)
    GET(
        Commands.GET,
        (data, key, args) -> {
            String value = data.get(key);
            return value != null
                ? new Response(Config.OK_STATUS, value)
                : new Response(Config.ERROR_STATUS, Config.NO_SUCH_KEY_REASON);
        }
    ),
    @SerializedName(Commands.SET)
    SET(
        Commands.SET,
        (data, key, args) -> {
            if (args.length == 0) throw new IllegalArgumentException("SET command requires a value");
            data.put(key, args[0]);
            return new Response(Config.OK_STATUS);
        }
    ),
    @SerializedName(Commands.DELETE)
    DELETE(
        Commands.DELETE,
        (data, key, args) -> {
            return data.remove(key) != null
                ? new Response(Config.OK_STATUS)
                : new Response(Config.ERROR_STATUS, Config.NO_SUCH_KEY_REASON);
        }
    ),
    @SerializedName(Commands.EXIT)
    EXIT(
        Commands.EXIT,
        (data, key, args) -> new Response("exit")
    );

    private final String name;
    private final CommandExecutor executor;

    Command(String name, CommandExecutor executor) {
        this.name = name;
        this.executor = executor;
    }

    @FunctionalInterface
    interface CommandExecutor {
        Response execute(Map<String, String> data, String key, String... args);
    }

    public Response execute(Map<String, String> data, String key, String... args) {
        return executor.execute(data, key, args);
    }

    public static Command fromName(String name) {
        for (Command command : values()) {
            if (command.name.equals(name)) {
                return command;
            }
        }
        return null;
    }
}