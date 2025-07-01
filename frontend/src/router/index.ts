import { createRouter, createWebHashHistory } from 'vue-router'
import AuthService from '../services/service.auth'

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
    },
    {
      path: '/posts',
      name: 'Posts',
      component: () => import('../views/ViewPosts.vue')
    },
    {
      path: '/posts/create',
      name: 'CreatePost',
      component: () => import('../views/ViewCreatePost.vue')
    },
    {
      path: '/posts/:id',
      name: 'PostDetail',
      component: () => import('../views/ViewPostDetail.vue')
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: () => import('../views/ViewStatistics.vue')
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('token')

  const loginValid = await AuthService.me()
    .then((response) => {
      if (response.status === 200) {
        localStorage.setItem('user', JSON.stringify(response.data))
        return true
      } else {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        return false
      }
    })
    .catch(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      return false
    })

  // trying to access a restricted page + not logged in
  // redirect to login page
  if ((authRequired && !loggedIn) || (authRequired && !loginValid)) {
    next('/login')
  } else {
    next()
  }
})

export default router
