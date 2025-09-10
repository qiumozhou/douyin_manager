import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import VideoManagement from '../views/VideoManagement.vue'
import AIGeneration from '../views/AIGeneration.vue'
import DouyinPublish from '../views/DouyinPublish.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/videos',
    name: 'VideoManagement',
    component: VideoManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/ai',
    name: 'AIGeneration',
    component: AIGeneration,
    meta: { requiresAuth: true }
  },
  {
    path: '/douyin',
    name: 'DouyinPublish',
    component: DouyinPublish,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router 