# RU204 Redis OM Java/Spring Example

The following example demonstrates data modeling with RedisJSON and the [Redis OM for Java (Spring)](https://github.com/redis/redis-om-spring) client.

## Prerequisites

* You'll need [Java 11](https://sdkman.io/sdks) or higher installed.
* You will need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to set the `REDIS_URL` environment variable to point at your instance before running the code.  If you need help with the format for this, check out the [Redis URI scheme specification](https://www.iana.org/assignments/uri-schemes/prov/redis).

## Run the Code

Ensure that your Redis Stack instance is running, and that you have set the `REDIS_URL` environment variable if necessary.  Example:

```bash
export REDIS_URL=redis://user:password@host:port
```

Now, run the code with the Maven wrapper provided:

```bash
./mvnw clean spring-boot:run
```

## View the Code

The code is contained in [`ExampleApplication.java`](.src/main/java/com/redis/om/spring/example/ExampleApplication.java).
