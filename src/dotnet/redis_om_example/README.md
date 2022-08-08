# RU204 Redis OM .NET Example

The following example demonstrates data modeling with RedisJSON and the [Redis OM .NET](https://github.com/redis/redis-om-dotnet) Client.

## Prerequisites

* You'll need the [.NET 6 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0) or later installed.
* You will need an instance of Redis Stack.  See the [setup instructions](/README.md) in the README at the root of this repo.
* If you are running your Redis Stack instance in the cloud or somewhere that isn't localhost:6379, you'll need to set the `REDIS_OM_URL` environment variable to a valid StackExchange.Redis [connection string](https://stackexchange.github.io/StackExchange.Redis/Configuration#basic-configuration-strings). 

## How to Run the App

After the prerequisites are met, simply run `dotnet run` from this directory.

## Where is the Code?

The Model code for this example is spread across [`Book.cs`](./Book.cs), [`InventoryItem.cs`](./InventoryItem.cs), [`Metrics.cs`](./Metrics.cs), the actual logic for creating and inserting the model into Redis is performed in [`Program.cs`](Program.cs).