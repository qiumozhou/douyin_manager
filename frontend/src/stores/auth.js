import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, register, getMe } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const loginUser = async (credentials) => {
    loading.value = true
    try {
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      
      const response = await login(formData)
      setToken(response.data.access_token)
      await fetchUserInfo()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || '登录失败' }
    } finally {
      loading.value = false
    }
  }

  const registerUser = async (userData) => {
    loading.value = true
    try {
      await register(userData)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || '注册失败' }
    } finally {
      loading.value = false
    }
  }

  const fetchUserInfo = async () => {
    try {
      const response = await getMe()
      setUser(response.data)
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    loading,
    loginUser,
    registerUser,
    fetchUserInfo,
    logout
  }
}) 