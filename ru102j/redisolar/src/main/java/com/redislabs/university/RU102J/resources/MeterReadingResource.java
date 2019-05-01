package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.dao.CapacityDao;
import com.redislabs.university.RU102J.dao.FeedDao;
import com.redislabs.university.RU102J.dao.MetricDao;
import com.redislabs.university.RU102J.dao.SiteDao;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/meterReading")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class MeterReadingResource {

    private final SiteDao siteDao;
    private final MetricDao metricDao;
    private final CapacityDao capacityDao;
    private final FeedDao feedDao;

    public MeterReadingResource(SiteDao siteDao, MetricDao metricDao, CapacityDao capacityDao,
                                FeedDao feedDao) {
        this.siteDao = siteDao;
        this.metricDao = metricDao;
        this.capacityDao = capacityDao;
        this.feedDao = feedDao;
    }

    @POST
    public Response add(MeterReading reading) {
        siteDao.update(reading);
        capacityDao.update(reading);
        metricDao.insert(reading);
        feedDao.insert(reading);

        return Response.accepted().build();
    }
}
