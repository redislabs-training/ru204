import config from './config.js'
import axios from 'axios'
import pkg from 'pg'
import express from 'express'
import cors from 'cors'

const { Client } = pkg
const lms = new Client(config.LMSDB)
lms.connect()

const cors_options = { methods: ["GET", "POST"]};
const app = express()
const ruRegexMatcher = /RU[0-9]{0,3}[A-Z]{0,2}/g
let username

app.use(express.json())

/* fetch username from Redshift */
const getUserName = async (user_id) => {
  const response = await lms.query({
    text:  `SELECT context_username
            FROM javascript.edx_certificate_created 
            WHERE user_id=$1::text`,
    values: [user_id],
    rowMode: 'array',
  })
  const username = response.rows[0][0]
  return username
}

/* check lms for completed courses and ensure necessary classes are completed */
const checkEligibility = async (user_id) => {
  let response;
  try{                 
    /* fetch all completed courses */
    response = await lms.query({
      text:  `SELECT label, context_username
              FROM javascript.edx_certificate_created 
              WHERE user_id=$1::text`,
      values: [user_id],
      rowMode: 'array',
    })
  } catch (e) {
    console.error('Error Occurred Fetching Data from Redshift: ', e);
    return {
      success: false,
      message: `Error from Redshift: ${e.message}`
    }
  }
    console.log(response)
    if (response.rows.length === 0) {
      return {
        success: false,
        message: 'No courses have been completed.',
        reason: 'none completed'
      }
    }
    username = response.rows[0][1]
    /* strip course versions and flattens response */
    const rawCourses = response.rows
                        .map(course => course[0]
                          .match(ruRegexMatcher))
                          .flat()                          
    /* deduplicate completed course rows */
    const courses = [...new Set(rawCourses)]
    /* check for presence of RU101, RU202, and an 'elective' class */
    const ru101Completed = courses.splice(courses.indexOf('RU101'), 1).length === 1
    const ru202Completed = courses.splice(courses.indexOf('RU202'), 1).length === 1
    const electives = courses.flat()
    return {
            'success': true,
            'RU101': ru101Completed,
            'RU202': ru202Completed,
            'electives': electives,
          }
}

/* enroll student into current Exam */
const enrollStudentWithAppsembler = async (username) => {

  const enrollmentEndpoint = `${config.TAHOEENDPOINT}enrollments/`
  let newestExamCourse
  try {
    newestExamCourse = await getNewestExamCourse()
  } catch(e) {
    console.error('Enroll student with newest course error: ', e.mesage)
    return {
      success: false,
      message: e.message
    }
  }

  /* Payload: 
    'action': we are enrolling the user in a course
    'email_learners': sends an email to user when enrolled
    'courses': we pull the newest Exam course from our Appsembler instance
    'identifiers': username or email-address of the user */
  const payload = {
    'action': 'enroll',
    'email_learners': true,
    'courses': [ await getNewestExamCourse() ],
    'identifiers': [ username ]
  }
  const headers = {
    'Authorization': config.APPSEMBLER_TOKEN,
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache'
  }

  try {
    const enrollRes = await axios.post(
      enrollmentEndpoint, 
      payload, 
      { headers: headers })
    return {success: true}
  } catch(e) {
    console.error('Enrollment Error: ', e.mesage)
    return {
      success: false,
      message: e.message
    }
  }
}

/* polls Appsembler for most recent Exam course based on version number */
const getNewestExamCourse = async () => {
  let newestExamCourse
  try {
    newestExamCourse= await axios.get(`${config.TAHOEENDPOINT}courses/?number=DEVELOPER-CERTIFICATION-EXAM-1`, { 
      headers: { Authorization: config.APPSEMBLER_TOKEN }
    })
  } catch(e) {
    console.error('getNewestExamCourse Error: ', e.mesage)
  }
  if(newestExamCourse.data.results.length === 0){
    throw new Error('No developer certification exam courses found')
  }
  const course_id = newestExamCourse
                      .data
                      .results[newestExamCourse.data.results.length-2]
                      .id
  return course_id
}

app.options('*', cors(cors_options))

app.get('/check-availability', cors(cors_options), async (req, res) => {
  const user_id = req.query.user_id
  if(!user_id || user_id === 'undefined') {
    res.json({ error: 'user_id is undefined or unavailable', user_id: user_id })
  }
  if(user_id){
    const eligibility = await checkEligibility(user_id)
    res.json(eligibility)
  } 
})

app.post('/enroll-student', cors(cors_options), async (req, res) => {
  
  const user_id = req.body.user_id
  const username = await getUserName(user_id)
  const enrollRes =  await enrollStudentWithAppsembler(username)
  res.json(enrollRes)

})

app.get('/healthcheck', async (req, res) =>  {
  // TODO: send back stats on current exam course, port, etc.
  const current_exam = await getNewestExamCourse()
  res.json({ status: 'Healthy', current_exam: current_exam})
})

app.listen(`${config.PORT}`, function(){
  console.log(`App listening at port ${config.PORT}`)
})
