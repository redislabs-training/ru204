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

    // Always override /courses
    r.delete('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.get('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.head('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.options('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.post('.*/courses/.*', req => fetch(modifyRequest(req)))
    r.put('.*/courses/.*', req => fetch(modifyRequest(req)))

    // Always override /certifications
    r.delete('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.get('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.head('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.options('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.post('.*/certifications/.*', req => fetch(modifyRequest(req)))
    r.put('.*/certifications/.*', req => fetch(modifyRequest(req)))
    
    // Always override /staticassets, this is where CSS/JS/images for
    // the static site live, to not conflict with anything in Tahoe.
    r.delete('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.get('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.head('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.options('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.patch('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.post('.*/staticassets/.*', req => fetch(modifyRequest(req)))
    r.put('.*/staticassets/.*', req => fetch(modifyRequest(req)))

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