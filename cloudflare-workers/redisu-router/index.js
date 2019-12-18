const Router = require('./router')

function replaceDomain(urlToReplace) {
    const beginDomain = urlToReplace.indexOf('://')
    const endDomain = 1 + urlToReplace.indexOf('/', beginDomain + 3)

    return `${urlToReplace.substring(0, beginDomain)}://simonprickett.dev/${urlToReplace.substring(endDomain)}`
}

addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const r = new Router()

    // TODO check the headers to see what to do with / depending 
    // on whether the user is logged in or not...
    console.log('HEADERS:')
    console.log(request.headers)
    
    const cookies = request.headers.get('Cookie')

    r.delete('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.get('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.head('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.options('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.patch('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.post('.*/assets/.*', req => fetch(replaceDomain(req.url)))
    r.post('/', req => fetch(replaceDomain(req.url)))
    r.put('.*/assets/.*', req => fetch(replaceDomain(req.url)))

    // If not logged in, override homepage else send to origin.
    if (cookies && cookies.indexOf('_ga=GA1.2.2027235534.1575393409') == -1) {
        r.delete('/', req => fetch(replaceDomain(req.url)))
        r.get('/', req => fetch(replaceDomain(req.url)))
        r.head('/', req => fetch(replaceDomain(req.url)))
        r.options('/', req => fetch(replaceDomain(req.url)))
        r.patch('/', req => fetch(replaceDomain(req.url)))
        r.put('/', req => fetch(replaceDomain(req.url)))        
    }

    // Send everything else to the original origin...
    r.delete('.*', req => fetch(req))
    r.get('.*', req => fetch(req))
    r.head('.*', req => fetch(req))
    r.options('.*', req => fetch(req))
    r.patch('.*', req => fetch(req))
    r.post('.*', req => fetch(req))
    r.put('.*', req => fetch(req))
    
    return await r.route(request)
}