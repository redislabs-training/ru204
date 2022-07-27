package com.redis.university.ru204;

import redis.clients.jedis.UnifiedJedis;
import redis.clients.jedis.json.Path2;

import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import org.json.JSONArray;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class App
{
    private final static String BOOK_KEY = "ru204:book:99999";
    private static final Gson GSON = new Gson();

    public static void main( String[] args ) throws IOException
    {
        Reader reader = Files.newBufferedReader(Paths.get("src/main/resources/data/Book.json"));
        JsonObject book = new Gson().fromJson(reader, JsonObject.class);

        // Connect to Redis
        UnifiedJedis r = new UnifiedJedis(System.getenv().getOrDefault("REDIS_URL", "redis://localhost:6379"));

        // Delete any previous data at our book's key
        r.del(BOOK_KEY);

        // Store the book in Redis at key ru204:book:3...
        // Response will be: OK
        String strResponse = r.jsonSet(BOOK_KEY, book);
        System.out.println("Book stored: " + strResponse);

        // Let's get the author and score for this book...
        // Response will be:
        // {"$.metrics.score":[2.3],"$.author":["Redis University"]}
        Object objResponse = r.jsonGet(BOOK_KEY, Path2.of("$.author"), Path2.of("$.metrics.score"));

        System.out.println("Author and score:");
        System.out.println(objResponse);

        // Add one to the number of rating_votes:
        // Response will be: void
        // Requires Jedis 4.3? Might have to use executeCommand meantime?
        JSONArray arrResponse = r.jsonNumIncrBy(BOOK_KEY, Path2.of("$.metrics.rating_votes"), 1d);
        System.out.println("rating_votes incremented to " + arrResponse.getInt(0));

        // Add another copy of the book to the inventory.
        // Response will be: 3 (new size of the inventory array)
        JsonObject newInventoryItem = GSON.fromJson("{'status': 'available', 'stock_id': '99999_3'}", JsonObject.class);
        List<Long> arrAppendResponse = r.jsonArrAppend(BOOK_KEY, Path2.of("$.inventory"), newInventoryItem);
        System.out.println("There are now " + arrAppendResponse.get(0) + " copies of the book in the inventory.");

        // Disconnect from Redis.
        r.close();
    }
}
