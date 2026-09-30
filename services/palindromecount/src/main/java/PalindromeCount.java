import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

public class PalindromeCount {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(9000), 0);
        server.createContext("/palindromecount", new PalindromeHandler());
        server.setExecutor(null); // creates a default executor
        System.out.println("Server is listening on port 9000...");
        server.start();
    }

    static class PalindromeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {

            // Set CORS headers
            exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
            exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, OPTIONS");
            exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type");

            // Handle OPTIONS request (preflight)
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1); // No content for OPTIONS
                return;
            }

            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                String response = "Only GET method is supported";
                exchange.sendResponseHeaders(405, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
                return;
            }

            String query = exchange.getRequestURI().getRawQuery();
            String inputText = getQueryParam(query, "text");

            if (inputText == null || inputText.isEmpty()) {
                String response = "palindromecount is running";
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
                return;
            }

            int palindromeCount = countPalindromes(inputText);

            String response = "{\"answer\": " + palindromeCount + "}";
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
            exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }

        private String getQueryParam(String query, String param) {
            if (query == null || query.isEmpty()) {
                return null;
            }
            return java.util.Arrays.stream(query.split("&"))
                    .map(kv -> kv.split("=", 2))
                    .filter(kv -> kv.length == 2 && kv[0].equals(param))
                    .map(kv -> URLDecoder.decode(kv[1], StandardCharsets.UTF_8))
                    .findFirst()
                    .orElse(null);
        }
    }

    public static int countPalindromes(String input) {
    if (input == null || input.isEmpty()) {
        return 0;
    }

    String[] words = input.trim().split("[^a-zA-Z]+");
    int count = 0;
    for (String word : words) {
        if (isPalindrome(word)) {
            count++;
        }
    }
    return count;
}

    private static boolean isPalindrome(String word) {
        String cleanWord = word.replaceAll("[^a-zA-Z]", "").toLowerCase();
        int len = cleanWord.length();
        if (len == 1 || len == 0) return false;
        for (int i = 0; i < len / 2; i++) {
            if (cleanWord.charAt(i) != cleanWord.charAt(len - 1 - i)) {
                return false;
            }
        }
        return true;
    }
}
