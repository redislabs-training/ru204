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
  try{                 
    /* fetch all completed courses */
    const response = await lms.query({
      text:  `SELECT label, context_username
              FROM javascript.edx_certificate_created 
              WHERE user_id=$1::text`,
      values: [user_id],
      rowMode: 'array',
    })
    username = response.rows[0][1]
    /* strip course versions and flattens response */
    const rawCourses = response.rows
                        .map(course => course[0]
                          .match(ruRegexMatcher))
                          .flat()                          
    /* deduplicate completed course rows */
    const courses = [...new Set(rawCourses)]
    /* check for presence of RU101, RU202, and an 'elective' class */
    const ru101Elig = courses.splice(courses.indexOf('RU101'), 1).length === 1
    const ru202Elig = courses.splice(courses.indexOf('RU202'), 1).length === 1
    const electives = courses.flat()
    return {
            'RU101': ru101Elig,
            'RU202': ru202Elig,
            'electives': electives,
          }
  } catch (e) {
    console.error('Error Occurred Fetching Data from Redshift: ', e);
    return {
      success: false,
      message: `Unable to find user with id: ${user_id}`
    }
  }
}

/* enroll student into current Exam */
const enrollStudentWithAppsembler = async (username) => {

  const enrollmentEndpoint = `${config.TAHOEENDPOINT}enrollments/`

  const payload = {
      'action': 'enroll',
      'email_learners': true,
      'auto_enroll': true,
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
    console.error('Error: ', e)
    return {
      success: false,
      message: e.message
    }
  }
}

/* polls Appsembler for most recent Exam course based on version number */
const getNewestExamCourse = async () => {
  const newestExamCourse = await axios.get(`${config.TAHOEENDPOINT}courses/?number=DEVELOPER-CERTIFICATION-EXAM-1`, { headers: {
    Authorization: config.APPSEMBLER_TOKEN,
  }})
  const course_id = newestExamCourse
                      .data
                      .results[newestExamCourse.data.results.length-2]
                      .id
  return course_id
}

app.options('*', cors(cors_options))

app.get('/check-availability', cors(cors_options), async (req, res) => {
  const { user_id } = req.query
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
