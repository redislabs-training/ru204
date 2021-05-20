# Cloudflare Workers for Redis University

To work with this code you need a Cloudflare account that can access Redis University.  If you don't have one, ask Simon Prickett or Kyle Banker.

## Overview

This is a [Cloudflare Worker](https://workers.cloudflare.com/) that acts as a proxy to route URLs so that some paths are served from a different underlying origin than others.

The aim of is to serve the Redis University home page and other URL paths from a static site origin to improve SEO, page load speed and design while keeping the rest of Redis University served from Appsembler.

To do this, we needed to set a DNS CNAME for `university.redislabs.com` to point to Cloudflare (`university.redislabs.com.cdn.cloudflare.net`).  We had to do this as we aren't moving all of `redislabs.com` to pass through Cloudflare.  Mapping only a subdomain to Cloudflare is a feature that requires a Cloudflare business account, so we have obtained one of those.

The static site that will be served on some URLs is in a repo in the RedisLabs Training organization.  This static site is contained in three GitHub repos as follows:

* [Site source (Jekyll)](https://github.com/redislabs-training/redis-university-static-site).
* [Stage environment built copy](https://github.com/redislabs-training/redis-university-static-site-stage) - GitHub pages is enabled here and this serves as the stage copy of the site.
* [Production environment built copy](https://github.com/redislabs-training/redis-university-static-site-prod) - GitHub pages is enabled here and this serves as the production copy of the site.

## Routing Logic

When a request comes into `university.redislabs.com` in production or `stage-university.redislabs.com`, the following happens:

* The request goes to Cloudflare.
* Cloudflare checks to see if the request URL matches a set of patterns that we want to serve a static site page for, rather than an Appsembler origin page.  Cloudflare uses patterns listed in the file `wrangler.toml` in this repo for this purpose.  There are separate sets of URLs listed for stage and production, the paths are the same for both but the hostnames differ.
* If the request URL does not match one of these patterns, Cloudflare sends the request to the origin (Appsembler) and Appsembler generates the page and it's returned to the client via Cloudflare.
* If the request URL des match one of these patterns, Cloudflare instead runs a worker (serverless Node.js function) to decide what to do.  This is where our code in this repo comes into play.

### Router Workflow

The worker logic works like this:

* We have a general rule for the static site that all URLs that aren't file names need to end in /, and there should be a 301 redirect if not.  Example `university.redislabs.com/courses/ru101` should be redirected to `university.redislabs.com/courses/ru101/`.  There's an exception to this, `/courses` needs to go to `/#courses` so that is dealt with first.
* All other URLs get mapped to the same URL but with the front end `university.redislabs.com` replaced with the static site domain... so `university.redislabs.com/courses/ru101/` would be mapped to `redislabs-training.github.io/redis-university-static-site-prod/courses/ru101` for example.
* The router then requests the page from the remapped URL, and returns whatever comes back from GitHub pages for that URL. 
* If the remapped URL returns a 404 from the GitHub pages site, then the router requests the 404 page from GitHub pages and returns that instead.

To better understand how the code in `index.js` works, see the [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/).  The file `router.js` is provided as part of a [router template example](https://developers.cloudflare.com/workers/templates/pages/router) by Cloudflare and has not been modified for use with Redis University.

## Tooling

To work with Cloudflare Workers, you'll want to install [wrangler](https://github.com/cloudflare/wrangler) which is their CLI to manage and deploy Workers.  Install this globally using npm (instructions on Wrangler's GitHub page).

Once installed, run `wrangler config` and it will ask you for an API token.  You will need to set up an API token on Cloudflare with permissions as follows:

* All accounts - Workers KV Storage:Edit, Workers Scripts:Edit, Account Settings:Read
* All zones - Workers Routes:Edit
* All users - User Details:Read

Once you have that token, supply it to wrangler and that will authenticate you with our Cloudflare environment.

## Configuration

Some configuration items need to be set in `wranger.toml`.  These are:

* `zone_id` - Cloudflare zone ID, you can get this from your Cloudflare dashboard.  This is already set with values for the Redis Labs account.
* `account_id` - Cloudflare account ID, you can get this from your Cloudflare dashboard.  This is already set with values for the Redis Labs account.
* `name` - The name that Cloudflare will use for the worker on the Cloudflare dashboard.  With the provided config values, this will be `redisu-stage-router` for stage and `redisu-router` for production.
* `routes` - Array of route patterns that the worker needs to run on.  These routes should between them encompass all possible URLs that the static site needs to show up at, including URLs needed for the static site images, icons, etc.  Read about routes [here](https://developers.cloudflare.com/workers/about/routes/) (Matching Behavior section).  Note that these are set per environment.
* `vars` - Environment variables that the worker needs.  Note that these are set per environment.  Right now these are `TAHOE_HOST` - the origin URL for Appsembler (which is the same as the front end URL for Cloudflare) and `STATIC_HOST` which is the origin URL for the static site on GitHub pages.

## Testing 

**This doesn't work well in our use case, so it is recommended to test in stage.**

To test your Worker logic without deploying to a real domain, use the command:

```
$ wrangler preview --watch
```

This will give you a URL to visit where you can use the test tooling to try your logic against requests to a dummy domain without deploying to Cloudflare / a real domain.  Any changes you make to the Worker logic will be deployed to this test environment on save.

You can share the test URL with others, regardless of whether you are still running wrangler.

## Build

Before deployment, build your code:

```
$ wrangler build
```

This process is the same for both the stage and production environments.

## Deployment

Once you are ready, you can publish your code by running one of the following commands depending on which environment you are deploying to:

```
$ wrangler publish --env stage
```

```
$ wrangler publish --env production
```

This will upload it to Cloudflare, put it live and you should see your worker listed in the "Workers" tab on your Cloudflare dashboard.  Note that if you do this for production, you have immediately changed production so be careful!

Once you have deployed, your worker will show up on the "Workers" tab in the Cloudflare dashboard.