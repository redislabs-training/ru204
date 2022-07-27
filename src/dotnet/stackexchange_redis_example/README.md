# RU204 StackExchange.Redis Example

The following example demonstrates the execution of RedisJSON commands using the [StackExchange.Redis Client](https://github.com/stackexchange/StackExchange.Redis).

## Prerequisites

* You'll need the [.NET 6 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) or later installed
* You'll probably want to have an IDE for writing C# code, e.g. [Visual Studio](https://visualstudio.microsoft.com/), [JetBrains Rider](https://www.jetbrains.com/rider/), or [VS Code](https://code.visualstudio.com/)
* You will need an instance of Redis Stack running, this can be done locally with docker `docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack`, or by following one of the other [Redis Stack instillation guides](https://redis.io/docs/stack/get-started/install/), or of course via [Redis Cloud](https://app.redislabs.com/#/)
* If you are not running Redis Stack locally on port 6379, you will need to set the `REDIS_CONNECTION_STRING` environment variable to a valid StackExchange.Redis [connection string](https://stackexchange.github.io/StackExchange.Redis/Configuration#basic-configuration-strings)

## How to Run the App

After the prerequisites are met, all you need to do to run the app is to run the following command in your terminal, change directories into the StackExchange.Redis.Example directory and then run `dotnet run`.

## Where is the Code?

The code for this example is located in StackExchange.Redis.Example/Program.cs

