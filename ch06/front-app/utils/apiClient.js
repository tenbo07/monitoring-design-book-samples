import axios from '~/plugins/axios'

export default {
  getAllTasks: () => {
    return axios.get('/tasks')
  },
  postNewTask: (payload) => {
    console.log(payload)
    return axios.post('/tasks', payload)
  },
  updateTaskStatus: (payload) => {
    return axios.put('/tasks', payload)
  },
  deleteTask: (payload) => {
    return axios.delete('/tasks', {data: payload})
  }
}
