// src/store/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: state => !!state.token,
  },
  actions: {
    async login(username, password) {
      const res = await axios.post('http://localhost:8000/api/login/', { username, password })
      this.token = res.data.access
      localStorage.setItem('token', this.token)
      await this.fetchUser()
    },
    async fetchUser() {
      const res = await axios.get('http://localhost:8000/api/user/', {
        headers: { Authorization: `Bearer ${this.token}` },
      })
      this.user = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})
