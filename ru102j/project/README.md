# redisolar

How to start the redisolar application
---

1. Run `mvn package` to build your application
2. Start application with `java -jar target/redisolar-1.0.jar server config.yml`
3. To check that your application is running enter url `http://[HOST]:8081`. If you're
running on localhost, HOST will be "localhost".

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

To see your applications health enter url `http://localhost:8084/healthcheck`
