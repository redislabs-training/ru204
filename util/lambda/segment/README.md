Addresses tickets EDU-314, EDU-202, EDU-217.  Provides an AWS Lambda function which receives edX events from Segment, and performs the following:

* `problem_check`: remaps fields that have GUID type IDs in them to not have those in, adds a new field `block_id` containing the problem block ID, pushes a new event back to Segment called a `redisu.problem_check` event.  `problem_check` events in Segment no longer go direct to Redshift, they go to this Lambda.  `redisu.problem_check` events do now go to Segment.
* `edx.course.enrollment.activated`: remaps field `context.referer` to the top level, breaks out any referer URL to add new fields for `mkt_tok`, `utm_source`, `utm_medium`, `utm_campaign`
* `edx.certificate.created`: remaps field `data.certificate_id` to the top level

The Lambda can also additionally serve as a debugging location for the new events it creates.  If Segement is configured to send any of the following events to it, the Lambda will simply log the payload:

* `redisu.problem_check`
* `redisu.certificate.created`
* `redisu.course.enrollment.activated`

When deploying this, the Lambda needs one environment variable set.  This is `SEGMENT_WRITE_KEY` which should contain the Segment write key that it uses to create new events.