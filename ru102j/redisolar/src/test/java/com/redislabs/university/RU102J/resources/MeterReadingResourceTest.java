package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.dao.CapacityDao;
import com.redislabs.university.RU102J.dao.FeedDao;
import com.redislabs.university.RU102J.dao.MetricDao;
import com.redislabs.university.RU102J.dao.SiteDao;
import io.dropwizard.testing.junit.ResourceTestRule;
import org.junit.After;
import org.junit.Before;
import org.junit.ClassRule;
import org.junit.Test;
import static org.mockito.Mockito.*;

import static org.junit.Assert.*;

public class MeterReadingResourceTest {
    private static final SiteDao siteDao = mock(SiteDao.class);
    private static final MetricDao metricDao = mock(MetricDao.class);
    private static final CapacityDao capacityDao = mock(CapacityDao.class);
    private static final FeedDao feedDao = mock(FeedDao.class);

    @ClassRule
    public static final ResourceTestRule resources = ResourceTestRule.builder()
            .addResource(new MeterReadingResource(siteDao, metricDao, capacityDao, feedDao))
            .build();

    @Before
    public void setup() {
    }

    @After
    public void tearDown(){
        reset(siteDao);
        reset(metricDao);
        reset(capacityDao);
    }

    @Test
    public void testInsertMeterReading() {
    }
}