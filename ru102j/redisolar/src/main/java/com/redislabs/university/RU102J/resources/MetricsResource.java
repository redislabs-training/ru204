package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.Measurement;
import com.redislabs.university.RU102J.api.Plot;
import com.redislabs.university.RU102J.api.ValueUnit;
import com.redislabs.university.RU102J.dao.MetricDao;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.ArrayList;
import java.util.List;

@Path("/metrics")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class MetricsResource {

    private static final Integer defaultMetricCount = 120;

    private final MetricDao metricDao;

    public MetricsResource(MetricDao dayMetricDao) {
        this.metricDao = dayMetricDao;
    }

    @GET
    @Path("/{siteId}")
    public Response getSiteMetrics(@PathParam("siteId") Long siteId,
                                   @PathParam("count") Integer count) {
        List<Plot> plots = new ArrayList<>();
        if (count == null) {
            count = defaultMetricCount;
        }
        // Get kWhGenerated measurements
        List<Measurement> generated = metricDao.getRecent(siteId, ValueUnit.WHGenerated, count);
        plots.add(new Plot("Watt-Hours Generated", generated));

        // Get kWhUsed measurements
        List<Measurement> used = metricDao.getRecent(siteId, ValueUnit.WHUsed, count);
        plots.add(new Plot("Watt-Hours Used", used));

        return Response.ok(plots)
                .header("Access-Control-Allow-Origin", "*")
                .build();
    }
}
