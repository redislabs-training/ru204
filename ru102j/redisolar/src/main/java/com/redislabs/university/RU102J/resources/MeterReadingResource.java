package com.redislabs.university.RU102J.resources;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

@Path("/metrics")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class MeterReadingResource {

    public MeterReadingResource() {

    }

    @POST
    public void create() {}
}
