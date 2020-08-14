const Router = require('./router')

// Modify request URL to point to the desired origin URL.
function modifyRequest(request) {
    const beginDomain = request.url.indexOf('://')
    const endDomain = 1 + request.url.indexOf('/', beginDomain + 3)
    const newUrl = `${request.url.substring(0, beginDomain)}://${STATIC_HOST}/${request.url.substring(endDomain)}`

    return new Request(new URL(newUrl), request)    
}

// Map each type of HTTP verb for the supplied 
// URI pattern to the static site.
function mapURIPattern(router, pattern) {
    const action = (req) => {
        // If there is a . after the last / in url then 
        // this is a file request and we don't redirect it.
        const u = new URL(req.url)

        if (! u.pathname.endsWith('/')) {
            // If there is no . after the last slash in the 
            // path then redirect to a version of this URL
            // with a slash on the end of the path, and account
            // for request parameters.
            if (! (u.pathname.lastIndexOf('.') >= u.pathname.lastIndexOf('/'))) {
                return Response.redirect(`${u.protocol}//${u.hostname}${u.pathname}/${u.search}`)
            }
        }

        // Otherwise get the page from the static site origin.
        return fetch(modifyRequest(req))
    }

    router.delete(pattern, action)
    router.get(pattern, action)
    router.head(pattern, action)
    router.options(pattern, action)
    router.patch(pattern, action)
    router.post(pattern, action)
    router.put(pattern, action)
}

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const u = new URL(request.url)

    // This is an exception to the static site pages must end with / rule.
    if (u.pathname.endsWith('/courses') || u.pathname.endsWith('/courses/')) {
        // Always redirect /courses to /#courses and serve page
        // from the static site.
        return await Response.redirect(new URL(`https://${TAHOE_HOST}/#courses${u.search}`), 301)
    }

    const r = new Router()
   
    // Everything maps to the static site.
    mapURIPattern(r, '.*.')

    const response = await r.route(request)

    if (response.status === 404) {
        const fourZeroFour = await fetch(`https://${STATIC_HOST}/404/`)
        const pageText = await fourZeroFour.text()
        return new Response(pageText, {
            status: 404,
            headers: {
                'content-type': 'text/html'
            }
        }) 
    }

    return response
}