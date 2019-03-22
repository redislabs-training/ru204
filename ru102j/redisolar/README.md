# redisolar

How to start the redisolar application
---

1. Run `mvn clean install` to build your application
1. Start application with `java -jar target/redisolar-1.0-SNAPSHOT.jar server config.yml`
1. To check that your application is running enter url `http://localhost:8080`

Tests
---

To run all tests:

```
mvn test
```

To run a specific test:

```
mvn test -Dtest=JedisBasicsTest
```

Health Check
---

To see your applications health enter url `http://localhost:8081/healthcheck`
