import axios from 'axios'

export default axios.create({
  baseURL: process.env.apiEndPoint,
  timeout: 10000,
  proxy: true
})
