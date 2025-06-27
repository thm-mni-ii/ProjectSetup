import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/ViewHome.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/ViewLogin.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('../views/ViewRegister.vue')
    }
  ]
})

export default router
