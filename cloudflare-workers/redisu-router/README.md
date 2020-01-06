# Cloudflare Workers Experiment

This is a [Cloudflare Worker](https://workers.cloudflare.com/) that acts as a proxy to route URLs so that some paths are served from a different underlying origin than others.

The aim of this experiment is to see if we can serve the home page and other URL paths for Redis University from a static site origin to improve SEO, page load speed and design while keeping the rest of Redis University served from Appsembler.

To do this we'd need to proxy everything through here, point `university.redislabs.com` at Cloudflare, update the DNS servers that currently have `university.redislabs.com`, then stand up a static site for the other pages elsewhere (S3, GitHub pages for example.  I have been experimenting with GitHub pages and the Jekyll static site generator).

We have the additional complication that when a user is logged into Appsembler and they go to `university.redislabs.com`, Appsembler detects they are logged in through their cookies sent with the request and redirects them to the dashboard page.  The code in the Cloudflare Worker here aims to address that by looking for the cookie that edX sets when the user logs in.

Other complications we may have with moving to using this model would be:

* Moving the SSL for `university.redislabs.com` to Cloudflare?  Experiments indicate not a problem as the SSL has been working fine in my test setup.
* Virtual Labs are also on `university.redislabs.com` URLs so traffic for those would also be affected / proxied through Cloudflare - not a problem as such I think just means more hits on the Cloudflare worker code than if virtual labs could be handled on another URL - we will never want to proxy / make routing decisions for a virtual lab URL.
* Ensuring any uptime checks that Appsembler have work agaist the new URL that the Appsembler site is on, not against `university.redislabs.com`

Currently this is all configured to work on Simon's personal Cloudflare acccount and handle all requests to [`http://testinstance.crudworks.org`](http://testinstance.crudworks.org).

The logic that's run against each request right now looks like this:

* Requests for `/` are proxied to the same path on a different domain (`staticsite.crudworks.org` - representing our static site - currently implemented using GitHub pages and the Jekyll static site generator), unless a specific cookie is set to a specific value, in which case they go to the origin:
  * If the cookie `exdloggedin` is set to `true` (this is the cookie that edX sets once the user has logged in and has a session active with edX), then the code assumes that the user has an Appsembler session and proxies the request through to origin (which is the Redis U staging edX instance).
  * If the cookie is not set, the code assumes that this is not a logged in Appsembler session and proxies the request to the static site and the static site's home page will be seen.
* Requests for anything in `/staticassets` are proxied to the same path on a different domain, simulating the need we will have to have some path to store images / CSS / JS  for the static site we want to build that isn't on Appsembler.  So, for example `http://testinstance.crudworks.org/staticassets/images/logo.png` will really come from `http://staticsite.crudworks.org/staticassets/images/logo.png`.
* The static site is also used to serve all `/courses` and `/certifications` URLs, allowing us to serve static pages describing each course etc.
* All pages on the static site need to have the canonical URL set to `testinstance.crudworks.org`.
* Requests for all other URLs are proxied to the origin (which would be Appsembler).  We would need more of these paths for any URL structure that we want to have in the static site.

## Tooling

To work with Cloudflare Workers, you'll want to install [wrangler](https://github.com/cloudflare/wrangler) which is their CLI to manage and deploy Workers.

## Configuration

Some configuration items need to be set in `wranger.toml`.  These are:

* `route` - which route(s) to apply to (e.g. `test.crudworks.org/*`).
* `zone_id` - Cloudflare zone ID, you can get this from your Cloudflare dashboard.
* `account_id` - Cloudflare account ID, you can get this from your Cloudflare dashboard.

## Testing 

To test your Worker logic without deploying to a real domain, use the command:

```
$ wrangler preview --watch
```

This will give you a URL to visit where you can use the test tooling to try your logic against requests to a dummy domain without deploying to Cloudflare / a real domain.  Any changes you make to the Worker logic will be deployed to this test environment on save.

Note that the `Cookies` header is protected and won't work in this environment.  So to do meaningful testing you'll beed to build / deploy the code.

You can share the test URL with others, regardless of whether you are still running wrangler.

## Build

Before deployment, build your code:

```
$ wrangler build
```

## Deployment

Once you are ready, you can publish your code by running the following command:

```
$ wrangler publish
```

This will upload it to Cloudflare, put it live and you should see your worker listed in the "Workers" tab on your Cloudflare dashboard.