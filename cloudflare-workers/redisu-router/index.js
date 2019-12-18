const Router = require('./router')

function modifyRequest(request, updatedDomain) {
    const targetDomain = updatedDomain || 'simonprickett.dev'
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
   
    const originHost = 'redisu-staging.tahoe.appsembler.com'
    const cookies = request.headers.get('Cookie')

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

    r.delete('.*', req => fetch(modifyRequest(req, originHost)))
    r.get('.*', req => fetch(modifyRequest(req, originHost)))
    r.head('.*', req => fetch(modifyRequest(req, originHost)))
    r.options('.*', req => fetch(modifyRequest(req, originHost)))
    r.patch('.*', req => fetch(modifyRequest(req, originHost)))
    r.post('.*', req => fetch(modifyRequest(req, originHost)))
    r.put('.*', req => fetch(modifyRequest(req, originHost)))

    return await r.route(request)
}