package com.redis.university.ru204;

import redis.clients.jedis.UnifiedJedis;
import redis.clients.jedis.json.Path2;

import java.util.List;

import org.json.JSONArray;

import com.google.gson.Gson;

public class App 
{
    private final static String BOOK_KEY = "ru204:book:3";
    private static final Gson GSON = new Gson();
    private static final Object BOOK = GSON.fromJson(
        "{" +
        "   'author': 'Redis University'," +
        "   'id': 3," +
        "   'description': 'This is a fictional book used to demonstrate RedisJSON!'," +
        "   'editions': [" +
        "     'english'," +
        "     'french'" +
        "    ]," +
        "    'genres': [" +
        "      'education'," +
        "      'technology'" +
        "   ]," +
        "   'inventory': [" +
        "     {" +
        "       'status': 'available'," +
        "       'stock_id': '3_1'" +
        "     }," +
        "     {" +
        "       'status': 'on_loan'," +
        "       'stock_id': '3_2'" +
        "     }" +
        "   ]," +
        "   'metrics': {" +
        "     'rating_votes': 12," +
        "     'score': 2.3" +
        "   }," +
        "   'pages': 1000," +
        "   'title': 'Up and Running with RedisJSON'," +
        "   'url': 'https://university.redis.com/courses/ru204/'," +
        "   'year_published': 2022" +
        "  }"
        , Object.class);

    public static void main( String[] args )
    {
        // TODO try env vars for REDIS_URL
        UnifiedJedis r = new UnifiedJedis("redis://localhost:6379");

        // Delete any previous data at our book's key
        r.del(BOOK_KEY);

        // Store the book in Redis at key ru204:book:3...
        // Response will be: OK
        String strResponse = r.jsonSet(BOOK_KEY, Path2.ROOT_PATH, GSON.toJson(BOOK));
        System.out.println("Book stored: " + strResponse);

        // Let's get the author and score for this book...
        // Response will be:
        // {"$.metrics.score":2.3,"$.author":"Redis University"}
        Object objResponse = r.jsonGet(BOOK_KEY, Path2.of("$.author"), Path2.of("$.metrics.score"));

        System.out.println("Author and score:");
        System.out.println(objResponse);

        // Add one to the number of rating_votes:
        // Response will be: void
        // Requires Jedis 4.3? Might have to use executeCommand meantime?
        JSONArray arrResponse = r.jsonNumIncrBy(BOOK_KEY, Path2.of("$.metrics.rating_votes"), 1d);
        System.out.println("rating_votes incremented to " + arrResponse.getDouble(0));

        // Add another copy of the book to the inventory.
        // Response will be: 3 (new size of the inventory array)
        Object newInventoryItem = GSON.fromJson("{'status': 'available', 'stock_id': '3_3'}", Object.class);
        List<Long> arrAppendResponse = r.jsonArrAppend(BOOK_KEY, Path2.of("$.inventory"), GSON.toJson(newInventoryItem));
        System.out.println("There are now " + arrAppendResponse.get(0) + " copies of the book in the inventory.");

        // Disconnect from Redis.
        r.close();
    }
}
