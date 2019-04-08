package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.MeterReading;
import com.redislabs.university.RU102J.dao.CapacityDao;
import com.redislabs.university.RU102J.dao.MetricDao;
import com.redislabs.university.RU102J.dao.SiteDao;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/meter")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class MeterReadingResource {

    private final SiteDao siteDao;
    private final MetricDao metricDao;
    private final CapacityDao capacityDao;

    public MeterReadingResource(SiteDao siteDao, MetricDao metricDao, CapacityDao capacityDao) {
        this.siteDao = siteDao;
        this.metricDao = metricDao;
        this.capacityDao = capacityDao;
    }

    @POST
    public Response add(MeterReading reading) {
        siteDao.update(reading.getSiteId());
        metricDao.insert(reading);
        capacityDao.update(reading);
        return Response.accepted().build();
    }
}
