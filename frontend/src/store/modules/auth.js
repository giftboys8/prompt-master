import axios from '@/plugins/axios'

const state = {
  user: null,
  isAuthenticated: false
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
    state.isAuthenticated = !!user
  }
}

const actions = {
  async register({ commit }, userData) {
    try {
      const response = await axios.post('/api/auth/register/', userData)
      commit('SET_USER', response.data)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '注册失败')
    }
  },

  async login({ commit }, credentials) {
    try {
      const response = await axios.post('/api/auth/login/', credentials)
      commit('SET_USER', response.data.user)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '登录失败')
    }
  },

  async logout({ commit }) {
    try {
      await axios.post('/api/auth/logout/')
      commit('SET_USER', null)
    } catch (error) {
      console.error('登出失败:', error)
      throw error
    }
  },

  async fetchUser({ commit }) {
    try {
      const response = await axios.get('/api/auth/user/')
      commit('SET_USER', response.data)
      return response.data
    } catch (error) {
      commit('SET_USER', null)
      throw error
    }
  }
}

const getters = {
  user: state => state.user,
  isAuthenticated: state => state.isAuthenticated
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}