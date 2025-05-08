<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-success bg-gradient shadow-sm">
    <div class="container">
      <router-link to="/" class="navbar-brand text-white fw-bold d-flex align-items-center">
        🍉 Fruity Store
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Customer Menu -->
          <li class="nav-item" v-if="auth.isAuthenticated && auth.user && !auth.user.is_staff">
            <router-link to="/order-history" class="nav-link text-white">🧾 Order History</router-link>
          </li>
          <li class="nav-item" v-if="auth.isAuthenticated && auth.user && !auth.user.is_staff">
            <router-link to="/cart" class="nav-link text-white">🛒 Cart</router-link>
          </li>

          <!-- Employee Menu -->
          <li class="nav-item" v-if="auth.isAuthenticated && auth.user && auth.user.is_staff">
            <router-link to="/admin" class="nav-link text-white">📊 Admin Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="auth.isAuthenticated && auth.user && auth.user.is_staff">
            <router-link to="/add-product" class="nav-link text-white">➕ Add Product</router-link>
          </li>
        </ul>

        <ul class="navbar-nav ms-auto">
          <!-- Guest -->
          <li class="nav-item" v-if="!auth.isAuthenticated">
            <router-link to="/login" class="nav-link text-white">🔐 Login</router-link>
          </li>
          <li class="nav-item" v-if="!auth.isAuthenticated">
            <router-link to="/register" class="nav-link text-white">📝 Register</router-link>
          </li>

          <!-- Logged-in -->
          <li class="nav-item" v-if="auth.isAuthenticated">
            <a href="#" class="nav-link text-white" @click.prevent="handleLogout">🚪 Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const handleLogout = () => {
      auth.logout()
      router.push('/login')
    }

    return {
      auth,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 5px;
  transition: all 0.2s ease-in-out;
}
</style>
