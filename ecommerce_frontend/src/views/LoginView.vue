<template>
  <div class="container mt-5">
    <div
      class="row justify-content-center animate__animated"
      :class="{ 'animate__shakeX': error, 'animate__fadeInUp': !error }"
    >
      <div class="col-md-6">
        <div class="card shadow-lg rounded">
          <div class="card-body">
            <h3 class="card-title text-center text-success mb-4">🍎 Welcome Back to FruityMart</h3>
            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  v-model="username"
                  class="form-control"
                  placeholder="Enter your username"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <button class="btn btn-success w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Login
              </button>
            </form>
            <div v-if="error" class="mt-3 text-danger text-center fw-bold">
              {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()
const authStore = useAuthStore()

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = 'Invalid credentials'
  } finally {
    loading.value = false
  }
}
</script>

<style>
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';
</style>
