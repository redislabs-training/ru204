const Analytics = require('analytics-node')

const processCourseEnrollment = (event, callback) => {
    console.log('Processing a course enrollment event.')
    if (event.properties.context && event.properties.context.referer) {      
        writeToSegment({
            userId: event.userId,
            event: 'redisu.course.enrollment.activated', // was edx.course.enrollment.activated
            properties: {
                referer: event.properties.context.referer,
                ...event.properties
            }
        }, process.env.SEGMENT_WRITE_KEY, callback)
    } else {
        throw 'event.properties.context.referer is required'
    }
}

const processCertificateCreated = (event, callback) => {
    console.log('Processing a certificate created event.')
    respondOK(callback)
}

const processProblemCheck = (event, callback) => {
    console.log('Processing a problem check event.')
    // Problematic columns 
    respondOK(callback)
}

const processRedisUCourseEnrollment = (event, callback) => {
    console.log(`Received a "${event.event}" event:`)
    console.log(event)
    respondOK(callback)
}

const writeToSegment = (event, writeKey, callback) => {
    console.log('Writing event to Segment:')
    console.log(event)

    // Segment recommend flushAt: 1 for development, but 
    // as we are using Lambda functions it should stay here
    // all the time because 
    const segmentClient = new Analytics(writeKey, { flushAt: 1, flushInterval: .000000000001 })
    segmentClient.track(event)
    segmentClient.flush((err) => {
        if (err) {
            console.log('Error posting to Segment:')
            console.log(err)
            if (callback) {
                callback(err)
            }
        } else {
            console.log(`Posted to Segment.`)
            respondOK(callback)
        }
    })
}

const respondOK = callback => {
    callback(null, {
        statusCode: 200,
        body: 'OK'
    })
}

exports.handler = async (event, context, callback) => {
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
            default:
                console.log(`Unknown event: ${event.event}`)
                respondOK(callback)
        }
    } else {
        console.log('Bad request!')
        throw 'event.event is required'
    }
}