# RU204 StackExchange.Redis Example

The following example demonstrates the execution of RedisJSON commands using the [StackExchange.Redis Client](https://github.com/stackexchange/StackExchange.Redis).

## Prerequisites

* You'll need the [.NET 6 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) or later installed.
* You wll need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to set the `REDIS_CONNECTION_STRING` environment variable to a valid StackExchange.Redis [connection string](https://stackexchange.github.io/StackExchange.Redis/Configuration#basic-configuration-strings). 

## How to Run the App

After the prerequisites are met, all you need to do to run the app is to run the following commands in your terminal:

```bash
cd StackExchange.Redis.Example
dotnet run
```

## Where is the Code?

The code for this example is located in [`StackExchange.Redis.Example/Program.cs`](StackExchange.Redis.Example/Program.cs).

