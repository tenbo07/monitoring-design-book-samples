import ApiClient from '~/utils/apiClient'

export const state = () => ({
  toDoList: [],
  inProgressList: [],
  doneList: []
})

export const mutations = {
  SET_TODO_LIST (state, toDoList) {
    state.toDoList = toDoList
  },
  SET_INPROGRESS_LIST (state, inProgressList) {
    state.inProgressList = inProgressList
  },
  SET_DONE_LIST (state, doneList) {
    state.doneList = doneList
  }
}

export const actions = {
  async fetchList({ commit }) {
    let res = ""
    try {
      res = await ApiClient.getAllTasks()
      commit("SET_TODO_LIST", res.data['todo'] || [])
      commit("SET_INPROGRESS_LIST", res.data['inprogress'] || [])
      commit("SET_DONE_LIST", res.data['done'] || [])
    } catch (error) {
      console.log(error)
      commit("SET_TODO_LIST", [])
      commit("SET_INPROGRESS_LIST", [])
      commit("SET_DONE_LIST", [])
    }
  },
  async postNewTask(context, payload) {
    let res = ""
    try {
      res = await ApiClient.postNewTask(payload)
    } catch (error) {
      console.log(error)
      throw error
    }
  },
  async updateTaskStatus(context, payload) {
    let res = ""
    try {
      res = await ApiClient.updateTaskStatus(payload)
    } catch (error) {
      console.log(error)
      throw error
    }
  },
  async deleteTask(context, payload) {
    let res = ""
    try {
      res = await ApiClient.deleteTask(payload)
    } catch (error) {
      console.log(error)
      throw error
    }
  }
}

export const getters = {
  toDoList(state) {
    return state.toDoList
  },
  inProgressList(state) {
    return state.inProgressList
  },
  doneList(state) {
    return state.doneList
  }
}
