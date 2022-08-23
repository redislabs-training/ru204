package com.redis.om.spring.example;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.DefaultApplicationArguments;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.annotation.Id;


import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import com.redis.om.spring.annotations.Document;
import com.redis.om.spring.annotations.EnableRedisDocumentRepositories;
import com.redis.om.spring.annotations.Indexed;
import com.redis.om.spring.annotations.Searchable;
import com.redis.om.spring.repository.RedisDocumentRepository;
import com.redis.om.spring.search.stream.EntityStream;
import com.redis.om.spring.serialization.gson.GsonBuidlerFactory;

import io.redisearch.aggregation.SortedField.SortOrder;
import lombok.Data;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@SpringBootApplication
@EnableRedisDocumentRepositories(basePackages = "com.redis.om.spring.example")
public class ExampleApplication {

  private final Log logger = LogFactory.getLog(ExampleApplication.class);

  private static final Gson gson = GsonBuidlerFactory.getBuilder().setPrettyPrinting().create();

  @Value("${project.root}")
  private String projectRoot;

  @Bean
  CommandLineRunner loadTestData( //
      BookRepository repository, //
      EntityStream entityStream, //
      @Value("${project.root}/../../../data/books") String dataFolder //
  ) throws IOException {
    return args -> {
      var appArgs = new DefaultApplicationArguments(args);

      //
      // Data Loading
      //
      if (appArgs.containsOption("load") || args.length == 0) {
        // Delete all books from the database
        repository.deleteAll();

        // Read JSON data file names
        List<File> jsonFiles = Files //
            .list(Paths.get(dataFolder))//
            .map(Path::toFile).filter(File::isFile)
            .filter(f -> com.google.common.io.Files.getFileExtension(f.getName()).equals("json"))
            .collect(Collectors.toList());

        // Load each JSON data file and create a Book model
        List<Book> books = new ArrayList<Book>();
        jsonFiles.forEach(file -> {
          logger.info(String.format("Loading %s", file));
          try {
            books.add(gson.fromJson(Files.readString(file.toPath()), Book.class));
          } catch (IOException e) {
            logger.error(e.getMessage());
          }
        });
        repository.saveAll(books);
      }

      //
      // Searching
      //
      if (appArgs.containsOption("search") || args.length == 0) {
        // Search for books written by Stephen King... returns a list
        // of Book objects.
        List<Book> resultSet;

        resultSet = entityStream.of(Book.class) //
            .filter(Book$.AUTHOR.eq("Stephen King")) //
            .collect(Collectors.toList());

        printResults("Stephen King Books", resultSet);

        // Search for books with 'Star' in the title that are over 500
        // pages long, order by length.
        resultSet = entityStream.of(Book.class) //
            .filter(Book$.TITLE.containing("Star")) //
            .filter(Book$.PAGES.gt(500)) //
            .sorted(Book$.PAGES, SortOrder.ASC) //
            .collect(Collectors.toList());

        printResults("Star in title, >500 pages", resultSet);

        // Search for books with 'Star' but not 'War' in the title, and
        // which don't have 'space' in the description.
        resultSet = entityStream.of(Book.class) //
            .filter(Book$.TITLE.containing("Star")) //
            .filter(Book$.TITLE.notContaining("War")) //
            .filter(Book$.DESCRIPTION.containing("space")) //
            .collect(Collectors.toList());

        printResults("'Star' and not 'War' in title, no 'space' in description", resultSet);

        // Search for books by Robert Heinlein published between 1959 and 1973,
        // sort by year of publication descending.
        resultSet = entityStream.of(Book.class) //
            .filter(Book$.AUTHOR.eq("Robert A. Heinlein")) //
            .filter(Book$.YEAR_PUBLISHED.between(1959, 1973)) //
            .sorted(Book$.YEAR_PUBLISHED, SortOrder.DESC) //
            .collect(Collectors.toList());

        printResults("Robert Heinlein books published x to y", resultSet);
      }
    };
  }

  // Utility function to output matching Book objects.
  void printResults(String queryDescription, List<Book> resultSet) {
      logger.info("👉 " + queryDescription);
      resultSet.forEach(book -> logger.info(book));
      logger.info("-----");
  }

  public static void main(String[] args) {
    SpringApplication.run(ExampleApplication.class, args);
  }

}

// This class models the embedded "metrics" object.
@Data
@RequiredArgsConstructor(staticName = "of")
class Metrics {
  @NonNull @SerializedName(value = "rating_votes")
  private Integer ratingVotes;
  @NonNull
  private Double score;
}

// This class models the "inventory" array of objects.
@Data
@RequiredArgsConstructor(staticName = "of")
class InventoryItem {
  @NonNull
  private String status;
  @NonNull @SerializedName(value = "stock_id")
  private String stockId;
}

// This class models a book.
// Extra configuration to specify how to generate key
// names when saving an instance of the model in Redis.
@Data
@RequiredArgsConstructor(staticName = "of")
@Document
class Book {
  @Indexed @Id
  private String id;
  @Indexed @NonNull
  private String author;
  @Searchable @NonNull
  private String description;
  @NonNull
  private List<String> editions;
  @Indexed @NonNull
  private List<String> genres;
  @Indexed @NonNull
  private Integer pages;
  @Searchable @NonNull
  private String title;
  @NonNull
  private URL url;
  @NonNull
  @Indexed
  private Integer year_published;
  @NonNull
  private Metrics metrics;

  private List<InventoryItem> inventory;

  @Override
  public String toString() {
    return String.format("%s by %s %s pages, published %s.", title, author, pages, year_published);
  }
}

interface BookRepository extends RedisDocumentRepository<Book, String> {
}
