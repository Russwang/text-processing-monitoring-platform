import org.junit.jupiter.api.Test;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import static org.junit.jupiter.api.Assertions.*;

public class PalindromeCountTest {
    @Test
    public void testEncodedQueryThroughHttpHandler() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/palindromecount", new PalindromeCount.PalindromeHandler());
        server.start();
        try {
            String text = "Madam & noon + wow";
            String url = "http://127.0.0.1:" + server.getAddress().getPort()
                + "/palindromecount?text=" + URLEncoder.encode(text, StandardCharsets.UTF_8);
            HttpResponse<String> response = HttpClient.newHttpClient().send(
                HttpRequest.newBuilder(URI.create(url)).GET().build(), HttpResponse.BodyHandlers.ofString());
            assertEquals(200, response.statusCode());
            assertTrue(response.headers().firstValue("Content-Type").orElse("").contains("application/json"));
            assertEquals("{\"answer\": 3}", response.body());
        } finally {
            server.stop(0);
        }
    }

    @Test
    public void testPunctuationAndSingleLetters() {
        assertEquals(0, PalindromeCount.countPalindromes("a I !"));
        assertEquals(2, PalindromeCount.countPalindromes("Noon, level!"));
    }

    @Test
    public void testCountPalindromes() {
        assertEquals(3, PalindromeCount.countPalindromes("Madam Arora teaches malayalam"));
        assertEquals(0, PalindromeCount.countPalindromes("No palindromes here"));
        assertEquals(1, PalindromeCount.countPalindromes("Wow"));
        assertEquals(0, PalindromeCount.countPalindromes(""));
        assertEquals(0, PalindromeCount.countPalindromes(null));
    }
}
