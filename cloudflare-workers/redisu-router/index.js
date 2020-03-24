const Router = require('./router')

function modifyRequest(request, updatedDomain) {
    const targetDomain = updatedDomain || 'staticsite.crudworks.org'
    const beginDomain = request.url.indexOf('://')
    const endDomain = 1 + request.url.indexOf('/', beginDomain + 3)
    const newUrl = `${request.url.substring(0, beginDomain)}://${targetDomain}/${request.url.substring(endDomain)}`

    return new Request(new URL(newUrl), request)    
}

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const r = new Router()
   
    // This is the Tahoe host.
    const originHost = 'testinstance.crudworks.org'
    const cookies = request.headers.get('Cookie')

    // These should always come from the static site.
    r.delete('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.get('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.head('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.options('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.patch('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.post('.*/sitemap.xml', req => fetch(modifyRequest(req)))
    r.put('.*/sitemap.xml', req => fetch(modifyRequest(req)))

    r.delete('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.get('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.head('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.options('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.patch('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.post('.*/robots.txt', req => fetch(modifyRequest(req)))
    r.put('.*/robots.txt', req => fetch(modifyRequest(req)))    

    // Always override /courses unless the URL contains 'course-v1'
    // this is an edX about page.
    if (request.url.indexOf('course-v1') == -1) {
        r.delete('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.get('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.head('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.options('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.patch('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.post('.*/courses/.*', req => fetch(modifyRequest(req)))
        r.put('.*/courses/.*', req => fetch(modifyRequest(req)))
    }

    // Always override /certification
    r.delete('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.get('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.head('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.options('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.post('.*/certification/.*', req => fetch(modifyRequest(req)))
    r.put('.*/certification/.*', req => fetch(modifyRequest(req)))

    // Always override /certifications
    r.delete('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.get('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.head('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.options('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.post('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.put('.*/certifications/.*', req => fetch(modifyRequest(req)))
    
    // Always override /assets, this is where static site assets
    // live, to not conflict with anything in Tahoe.
    r.delete('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.get('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.head('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.options('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.post('.*/assets/.*', req => fetch(modifyRequest(req)))
    r.put('.*/assets/.*', req => fetch(modifyRequest(req)))

    // If not logged in, override homepage else send to origin.
    if (cookies && cookies.indexOf('edxloggedin=true') == -1) {
        r.delete('/', req => fetch(modifyRequest(req)))
        r.get('/', req => fetch(modifyRequest(req)))
        r.head('/', req => fetch(modifyRequest(req)))
        r.options('/', req => fetch(modifyRequest(req)))
        r.patch('/', req => fetch(modifyRequest(req)))
        r.put('/', req => fetch(modifyRequest(req)))      
        r.post('/', req => fetch(modifyRequest(req)))
    }

    // Send everything else to origin.
    r.delete('.*', req => fetch(modifyRequest(req, originHost)))
    r.get('.*', req => fetch(modifyRequest(req, originHost)))
    r.head('.*', req => fetch(modifyRequest(req, originHost)))
    r.options('.*', req => fetch(modifyRequest(req, originHost)))
    r.patch('.*', req => fetch(modifyRequest(req, originHost)))
    r.post('.*', req => fetch(modifyRequest(req, originHost)))
    r.put('.*', req => fetch(modifyRequest(req, originHost)))

    return await r.route(request)
}