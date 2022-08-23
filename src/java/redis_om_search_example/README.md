# RU204 Redis OM Java/Spring Example

The following example demonstrates data modeling with RedisJSON and the [Redis OM for Java (Spring)](https://github.com/redis/redis-om-spring) client.

## Prerequisites

* You'll need [Java 11](https://sdkman.io/sdks) or higher installed.
* You will need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to edit the [`application.properties`](./src/main/resources/application.properties) file (in `src/main/resources`) and provide the host, port and, if necessary, password for your Redis Stack instance.

## Delete Everything in Redis

Delete any data currently in Redis, using the following command in `redis-cli` or the CLI in RedisInsight:

```
FLUSHDB
```

## Run the Code

Ensure that your Redis Stack instance is running, and that you have edited the [`application.properties`](./src/main/resources/application.properties) file (in `src/main/resources`) if you aren't running Redis Stack at localhost:6379.  Example:

```
spring.redis.host=somehost.somedomain.com
spring.redis.port=9999
spring.redis.password=superSecretShhhh9823
```

## Load the Sample Data

```bash
./mvnw clean spring-boot:run -Dspring-boot.run.arguments="--load"
```

## Run the Sample Queries

```bash
./mvnw clean spring-boot:run -Dspring-boot.run.arguments="--search"
```

## View the Code

The code is contained in [`ExampleApplication.java`](./src/main/java/com/redis/om/spring/example/ExampleApplication.java).
