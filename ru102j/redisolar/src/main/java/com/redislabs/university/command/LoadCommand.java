package com.redislabs.university.command;

import com.redislabs.university.core.DataLoader;
import io.dropwizard.cli.Command;
import io.dropwizard.setup.Bootstrap;
import net.sourceforge.argparse4j.inf.Namespace;
import net.sourceforge.argparse4j.inf.Subparser;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class LoadCommand extends Command {
    public LoadCommand() {
        super("load", "Load the specified JSON file into Redis.");
    }

    @Override
    public void configure(Subparser subparser) {
        subparser.addArgument("--filename")
                .dest("filename")
                .type(String.class)
                .required(false)
                .help("The filename containing the JSON to load. If not specified, " +
                        "will load the sites.json file bundled with this JAR.");

        subparser.addArgument("--host")
                .dest("host")
                .type(String.class)
                .required(false)
                .setDefault("localhost")
                .help("The host of the Redis server to connect to");

        subparser.addArgument("--port")
                .dest("port")
                .type(Integer.class)
                .required(false)
                .setDefault(6379)
                .help("The port of the Redis server to connect to");
    }

    @Override
    public void run(Bootstrap<?> bootstrap, Namespace namespace) throws Exception {
        JedisPool jedisPool = new JedisPool(new JedisPoolConfig(),
                (String)namespace.get("host"), (Integer)namespace.get("port"));
        DataLoader loader = new DataLoader(jedisPool);
        loader.load();
        System.exit(0);
    }
}
