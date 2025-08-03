package Models;

import java.util.Base64;

public class Response {
    public final int statusCode;
    public final String content;

    public Response(int statusCode) {
        this.statusCode = statusCode;
        this.content = null;
    }

    public Response(int statusCode, String content) {
        this.statusCode = statusCode;
        this.content = content;
    }

    public Response(int statusCode, byte[] content) {
        this.statusCode = statusCode;
        this.content = Base64.getEncoder().encodeToString(content);
    }

    @Override
    public String toString() {
        return content != null ? "%s %s".formatted(statusCode, content) : String.valueOf(statusCode);
    }
}