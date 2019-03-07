package com.redislabs.university.resources;

import com.redislabs.university.api.Site;
import com.redislabs.university.dao.SiteDao;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.concurrent.atomic.AtomicLong;

@Path("/sites")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class Sites {

    private final SiteDao siteDao;
    private AtomicLong counter;

    public Sites(SiteDao siteDao) {
        this.siteDao = siteDao;
    }

    @GET
    public Response getSites() {
        return Response.ok(siteDao.findAll())
                .header("Access-Control-Allow-Origin", "*")
                .build();
    }

    @GET
    @Path("/{id}")
    public Response getSite(@PathParam("id") Long id) {
        Site site = siteDao.findById(id);
        if (site == null) {
            return Response.noContent().status(404).build();
        } else {
            return Response.ok(site).header("Access-Control-Allow-Origin", "*").build();
        }
    }
}
