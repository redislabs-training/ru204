//const Analytics = require('analytics-node')
const request = require('request')

const processCourseEnrollment = (event, callback) => {
    console.log('Processing a course enrollment event.')
    let eventProps = {}

    if (event.properties.context && event.properties.context.referer) {   
        // Refactor to add referer at the top level.
        eventProps = {
            referer: event.properties.context.referer,
            ...event.properties
        }
    } else {
        // Make sure events get through so send it anyway...
        eventProps = event.properties
    }

    writeToSegment({
        userId: event.userId,
        event: 'redisu.course.enrollment.activated',  // was edx.course.enrollment.activated
        properties: eventProps
    }, process.env.SEGMENT_WRITE_KEY, callback)
}

const processCertificateCreated = (event, callback) => {
    console.log('Processing a certificate created event.')
    respondOK(callback)
}

const processProblemCheck = (event, callback) => {
    console.log('Processing a problem check event.')
    console.log(event)

    const eventProps = event.properties
    
    // TODO Fix problematic object key names

    // Generate a redisu.problem_check event...
    writeToSegment({
        userId: event.userId,
        event: 'redisu.problem_check',  // was problem_check
        properties: eventProps
    }, process.env.SEGMENT_WRITE_KEY, callback)
}

const processRedisUCourseEnrollment = (event, callback) => {
    console.log(`Received a "${event.event}" event:`)
    console.log(event)
    respondOK(callback)
}

const processRedisUProblemCheck = (event, callback) => {
    console.log(`Received a "${event.event}" event:`)
    console.log(event)
    respondOK(callback)
}

const writeToSegment = (event, writeKey, callback) => {
    // Clean up problematic fields.
    delete event.writeKey // Leaving this here causes Segment to ignore the Authorization header!

    console.log('Writing event to Segment:')
    console.log(event)

    const encodedCredentials = Buffer.from(`${writeKey}:`).toString('base64')

    request({
        url: 'https://api.segment.io/v1/track',
        headers: {
            Authorization: `Basic ${encodedCredentials}`,
            'cache-control': 'no-cache',
            'Content-Type': 'application/json'
        },
        body: event,
        json: true,
        method: 'POST'
    }, (err, response, body) => {
        if (! response || response.statusCode !== 200 || err) {
            throw err
        } else {
            console.log('Posted to Segment, response body:')
            console.log(body)
            respondOK(callback)
        }
    })

    // Segment recommend flushAt: 1 for development, but 
    // as we are using Lambda functions it should stay here
    // all the time because 
    // const segmentClient = new Analytics(writeKey, { flushAt: 1, flushInterval: .000000000001 })
    // segmentClient.track(event)
    // segmentClient.flush((err) => {
    //     if (err) {
    //         console.log('Error posting to Segment:')
    //         console.log(err)
    //         if (callback) {
    //             callback(err)
    //         }
    //     } else {
    //         console.log(`Posted to Segment.`)
    //         respondOK(callback)
    //     }
    // })
}

const respondOK = callback => {
    callback(null, {
        statusCode: 200,
        body: 'OK'
    })
}

exports.handler = (event, context, callback) => {
    if (event && event.event) {
        switch (event.event) {
            case 'edx.course.enrollment.activated':
                processCourseEnrollment(event, callback)
                break
            case 'edx.certificate.created':
                processCertificateCreated(event, callback)
                break
            case 'problem_check':
                processProblemCheck(event, callback)
                break
            // Temporary while we prove this out...
            case 'redisu.course.enrollment.activated':
                processRedisUCourseEnrollment(event, callback)
                break
            // Temporary while we prove this out...
            case 'redisu.problem_check':
                processRedisUProblemCheck(event, callback)
                break
            default:
                console.log(`Unknown event: ${event.event}`)
                respondOK(callback)
        }
    } else {
        console.log('Bad request!')
        throw 'event.event is required'
    }
}