package com.redislabs.university.RU102J.resources;

import com.redislabs.university.RU102J.api.Site;
import com.redislabs.university.RU102J.dao.SiteDao;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/sites")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class Sites {

    private final SiteDao siteDao;

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
