package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.ValueUnit;
import com.redislabs.university.RU102J.dao.DayMinuteMetricDao;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/metrics")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class Metrics {

    private final DayMinuteMetricDao dayMetricDao;

    public Metrics(DayMinuteMetricDao dayMetricDao) {
        this.dayMetricDao = dayMetricDao;
    }

    @GET
    @Path("/{siteId}")
    public Response getSiteMetrics(@PathParam("siteId") Long siteId) {
        return Response.ok(dayMetricDao.getMeasurements(siteId, ValueUnit.KWHGenerated))
                .header("Access-Control-Allow-Origin", "*")
                .build();
    }
}
