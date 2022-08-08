package com.redis.om.spring.example;

import java.net.URL;
import java.util.List;
import java.util.Optional;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.annotation.Id;

import com.google.gson.Gson;
import com.redis.om.spring.annotations.Document;
import com.redis.om.spring.annotations.EnableRedisDocumentRepositories;
import com.redis.om.spring.repository.RedisDocumentRepository;
import com.redis.om.spring.serialization.gson.GsonBuidlerFactory;

import lombok.Data;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@SpringBootApplication
@EnableRedisDocumentRepositories(basePackages = "com.redis.om.spring.example")
public class ExampleApplication {

  private final Log logger = LogFactory.getLog(ExampleApplication.class);
  @Bean
  CommandLineRunner loadTestData(BookRepository repository) {
    return args -> {
      // Delete all books from the database
      repository.deleteAll();

      // Create an instance of the Book model.
      Book newBook = Book.of(
        "Redis Staff",
        "This is a book all about Redis.",
        List.of("redis", "tech", "computers"),
        1000,
        "Redis for Beginners",
        new URL("https://university.redis.com/courses/ru204/"),
        2022,
        Metrics.of(4000, 4.5)
      );
      // set inventory items
      newBook.setInventory(List.of(
        InventoryItem.of("on_loan", "999_1"), //
        InventoryItem.of("maintenance", "999_2") //
      ));

      // Save the book to Redis.
      repository.save(newBook);
      logger.info("Saved book in Redis.");

      // Get the locally generated ULID for this book.
      logger.info(String.format("new_book ULID: %s", newBook.getId()));

      // Retrieve the book from Redis.
      Optional<Book> maybeABook = repository.findById(newBook.getId());
      Book aBook = maybeABook.get();
      logger.info("Retrieved from Redis:");
      logger.info(aBook);

      // Update the author field and save it.
      repository.updateField(aBook, Book$.AUTHOR, "Redis University");

      // Retrive book after update
      Optional<Book> maybeTheSameBook = repository.findById(newBook.getId());
      Book theSameBook = maybeTheSameBook.get();
      logger.info("Retrieved from Redis after update:");
      logger.info(theSameBook);
    };
  }

	public static void main(String[] args) {
		SpringApplication.run(ExampleApplication.class, args);
	}

}

// This class models the embedded "metrics" object.
@Data
@RequiredArgsConstructor(staticName = "of")
class Metrics {
  @NonNull private Integer ratingVotes;
  @NonNull private Double score;
}

// This class models the "inventory" array of objects.
@Data
@RequiredArgsConstructor(staticName = "of")
class InventoryItem {
  @NonNull private String status;
  @NonNull private String stockId;
}

// This class models a book.
// Extra configuration to specify how to generate key
// names when saving an instance of the model in Redis.
@Data
@RequiredArgsConstructor(staticName = "of")
@Document
class Book {
  @Id private String id;
  @NonNull private String author;
  @NonNull private String description;
  @NonNull private List<String> genres;
  @NonNull private Integer pages;
  @NonNull private String title;
  @NonNull private URL url;
  @NonNull private Integer yearPublished;
  @NonNull private Metrics metrics;

  private List<InventoryItem> inventory;

  @Override
  public String toString() {
    return gson.toJson(this);
  }

  // used to print the object as a JSON document
  private static final Gson gson = GsonBuidlerFactory.getBuilder().setPrettyPrinting().create();
}

interface BookRepository extends RedisDocumentRepository<Book,String> {}
