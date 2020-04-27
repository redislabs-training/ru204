const Router = require('./router')

// Modify request URL to point to the desired origin URL.
function modifyRequest(request, updatedDomain) {
    const targetDomain = updatedDomain || STATIC_HOST
    const beginDomain = request.url.indexOf('://')
    const endDomain = 1 + request.url.indexOf('/', beginDomain + 3)
    const newUrl = `${request.url.substring(0, beginDomain)}://${targetDomain}/${request.url.substring(endDomain)}`

    return new Request(new URL(newUrl), request)    
}

// Map each type of HTTP verb for the supplied URI pattern
// to the static site if originHost is unset, or to the Tahoe
// site that originHost points to if it is set.
function mapURIPattern(router, pattern, originHost) {
    const action = (req) => {
        // If there is a . after the last / in url then 
        // this is a file request and we don't redirect it.
        let redirectWithSlash = false

        if (! originHost && ! req.url.endsWith('/')) {
            // Only consider static URLs for redirect to / 
            // version.  But not those that are file requests...
            // File requests have a . in the path.
            const u = new URL(req.url)
            if (u.pathname.indexOf('.') === -1) {
                redirectWithSlash = true
            }
        }

        if (redirectWithSlash) {
            return Response.redirect(new URL(`${req.url}/`), 301)
        }    

        return fetch(modifyRequest(req, originHost))
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
    // This is an exception to the static site pages must end with / rule.
    if (request.url.endsWith('/courses') || request.url.endsWith('/courses/')) {
        // Always redirect /courses to /#courses and serve page
        // from the static site.
        return await Response.redirect(new URL(`https://${TAHOE_HOST}/#courses`), 301)
    }

    const r = new Router()
   
    // This is the Tahoe host.
    const originHost = TAHOE_HOST

    // These should always come from the static site.
    mapURIPattern(r, '.*/sitemap.xml')
    mapURIPattern(r, '.*/robots.txt')

    // Always override /courses unless the URL contains 'course-v1'
    // this is an edX about page.
    if (request.url.indexOf('course-v1') == -1) {
        mapURIPattern(r, '.*/courses/.*')
    }

    // Always override /certification
    mapURIPattern(r, '.*/certification.*')

    // Always override /certifications
    mapURIPattern(r, '.*/certifications.*')
    
    // Always override /assets, this is where static site assets
    // live, to not conflict with anything in Tahoe.
    mapURIPattern(r, '.*/assets/.*')

    // site.webmanifest is always on static.
    mapURIPattern(r, '/site.webmanifest')
   
    // Always override /
    mapURIPattern(r, '/')

    // Send everything else to origin.
    mapURIPattern(r, '.*', originHost)

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