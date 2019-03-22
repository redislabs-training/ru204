package com.redislabs.university.RU102J.dao;

import com.redislabs.university.RU102J.HostPort;
import com.redislabs.university.RU102J.TestKeyManager;
import com.redislabs.university.RU102J.api.Site;
import org.junit.*;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import static org.junit.Assert.assertEquals;

public class SiteRedisDaoTest {

    private static JedisPool jedisPool;
    private static Jedis jedis;
    private static TestKeyManager keyManager;
    private Set<Site> sites;

    @BeforeClass
    public static void setUp() throws Exception {
        jedisPool = new JedisPool(HostPort.getRedisHost(), HostPort.getRedisPort());
        jedis = new Jedis(HostPort.getRedisHost(), HostPort.getRedisPort());
        keyManager = new TestKeyManager("test");
    }

    @AfterClass
    public static void tearDown() {
        jedisPool.destroy();
        jedis.close();
    }

    @After
    public void flush() {
        keyManager.deleteKeys(jedis);
    }

    @Before
    public void generateData() {
        sites = new HashSet<>();
        sites.add(new Site(1, 4.5, 3, "123 Willow St.",
                "Oakland", "CA", "94577" ));
        sites.add(new Site(2, 3.0, 2, "456 Maple St.",
                 "Oakland", "CA", "94577" ));
        sites.add(new Site(3, 4.0, 3, "789 Oak St.",
                 "Oakland", "CA", "94577" ));
    }

    /**
     * Challenge #0 Part 1. This challenge is explained in
     * Chapter 1.9: How to Solve a Sample Challenge
     */
    @Test
    public void findByIdWithExistingSite() {
        SiteRedisDao dao = new SiteRedisDao(jedisPool);
        Site site = new Site(4, 5.5, 4, "910 Pine St.",
                "Oakland", "CA", "94577");
        dao.insert(site);
        Site storedSite = dao.findById(4L);
        assertThat(storedSite, is(site));
    }

    /**
     * Challenge #0 Part 2. This challenge is explained in
     * Chapter 1.9: How to Solve a Sample Challenge
     */
    @Test
    public void findByIdWithMissingSite() {
        SiteRedisDao dao = new SiteRedisDao(jedisPool);
        assertThat(dao.findById(4L), is(nullValue()));
    }

    /**
     * Challenge #1 Part 1. Use this test case to
     * implement the challenge in Chapter 1.11.
     */
    @Test
    public void findAllWithMultipleSites() {
        SiteRedisDao dao = new SiteRedisDao(jedisPool);
        // Insert all sites
        for (Site site : sites) {
            dao.insert(site);
        }

        assertEquals(dao.findAll(), sites);
    }

    /**
     * Challenge #1 Part 2. Use this test case to
     * implement the challenge in Chapter 1.11.
     */
    @Test
    public void findAllWithEmptySites() {
        SiteRedisDao dao = new SiteRedisDao(jedisPool);
        assertThat(dao.findAll(), is(empty()));
    }

    @Test
    public void insert() {
    }

    @Test
    public void findAll1() {
    }

    @Test
    public void findAllGeo() {
    }

    @Test
    public void findByGeo1() {
    }

    @Test
    public void findById1() {
    }

    @Test
    public void insert1() {
    }
}