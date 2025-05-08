import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProductCatalog from '@/views/ProductCatalog.vue'
import Cart from '@/views/Cart.vue'
import Checkout from '@/views/Checkout.vue'
import OrderSummary from '@/views/OrderSummary.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AddProduct from '@/views/AddProduct.vue' // ✅ Import AddProduct view

import { useAuthStore } from '@/store/auth'

const routes = [
  { path: '/', name: 'Catalog', component: ProductCatalog },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/cart', name: 'Cart', component: Cart },
  { path: '/checkout', name: 'Checkout', component: Checkout, meta: { requiresAuth: true } },
  { path: '/summary', name: 'Summary', component: OrderSummary, meta: { requiresAuth: true } },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true, isEmployee: true } },
  { path: '/add-product', name: 'AddProduct', component: AddProduct, meta: { requiresAuth: true, isEmployee: true } }, // ✅ New route
  {path: '/admin/edit/:id', name: 'EditProduct', component: () => import('@/views/EditProduct.vue'), meta: { requiresAuth: true }},
  {path: '/order-history',name: 'OrderHistory', component: () => import('@/views/OrderHistory.vue')}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.isEmployee && authStore.user?.role !== 'employee') {
    next('/')
  } else {
    next()
  }
})

export default router
