const Analytics = require('analytics-node')

const processCourseEnrollment = event => {
    console.log('Processing a course enrollment event.')
    if (event.properties.context && event.properties.context.referer) {      
        writeToSegment({
            userId: event.properties.user_id,
            event: 'redisu.course.enrollment.activated', // was edx.course.enrollment.activated
            properties: {
                referer: event.properties.context.referer,
                ...event.properties
            }
        }, event.writeKey)
    } else {
        throw 'event.properties.context.referer is required'
    }
}

const processCertificateCreated = event => {
    console.log('Processing a certificate created event.')
}

const processProblemCheck = event => {
    console.log('Processing a problem check event.')
    // Problematic columns 
}

const writeToSegment = (event, writeKey) => {
    console.log('Writing event to Segment:')
    console.log(event)

    // Segment recommend flushAt: 1 for decvelopment, but 
    // as we are using Lambda functions it should stay here
    // all the time because 
    const segmentClient = new Analytics(writeKey, { flushAt: 1 })
    segmentClient.track(event)
}

exports.handler = async (event) => {
    if (event && event.event) {
        switch (event.event) {
            case 'edx.course.enrollment.activated':
                processCourseEnrollment(event)
                break
            case 'edx.certificate.created':
                processCertificateCreated(event)
                break
            case 'problem_check':
                processProblemCheck(event)
                break
            default:
                console.log(`Unknown event: ${event.event}`)
        }
    } else {
        console.log('Bad request!')
        throw 'event.event is required'
    }

    return {
        statusCode: 200,
        body: 'OK'
    }
}