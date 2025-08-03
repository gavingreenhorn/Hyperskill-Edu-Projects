package Models;

import com.google.gson.*;
import com.google.gson.annotations.JsonAdapter;

import java.lang.reflect.Type;
import java.util.Base64;

@JsonAdapter(ResponseAdapter.class)
public class Response {
    public final String statusCode;
    public final String content;

    public Response(String statusCode) {
        this.statusCode = statusCode;
        this.content = null;
    }

    public Response(String statusCode, String content) {
        this.statusCode = statusCode;
        this.content = content;
    }

    public Response(String statusCode, byte[] content) {
        this.statusCode = statusCode;
        this.content = Base64.getEncoder().encodeToString(content);
    }

    public String getStatusCode() {
        return statusCode;
    }

    public String getContent() {
        return content;
    }

    @Override
    public String toString() {
        return content != null
            ? "%s %s".formatted(statusCode, content)
            : statusCode;
    }
}

class ResponseAdapter implements JsonSerializer<Response> {
    @Override
    public JsonElement serialize(Response request, Type typeOfSrc, JsonSerializationContext context) {
        JsonObject jason = new JsonObject();
        jason.addProperty("response", request.getStatusCode());
        if (request.content != null) {
            jason.addProperty(
                request.getStatusCode().equals(Config.OK_STATUS)
                    ? "value"
                    : "reason",
                request.getContent()
            );
        }
        return jason;
    }
}