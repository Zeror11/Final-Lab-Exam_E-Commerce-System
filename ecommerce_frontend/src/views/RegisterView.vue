<template>
  <div class="container mt-5 animate__animated animate__fadeInUp">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-lg rounded">
          <div class="card-body">
            <h3 class="card-title text-center text-success mb-4">🍊 Create Your FruityMart Account</h3>

            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  v-model="form.username"
                  class="form-control"
                  placeholder="Choose a username"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  placeholder="Choose a secure password"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Account Type</label>
                <select v-model="role" class="form-select" required>
                  <option value="customer">Customer</option>
                  <option value="employee">Employee</option>
                </select>
              </div>

              <button class="btn btn-success w-100">Register</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({ username: '', password: '' })
const role = ref('customer')

async function submit() {
  const payload = {
    ...form.value,
    is_customer: role.value === 'customer',
    is_employee: role.value === 'employee',
  }
  await axios.post('http://localhost:8000/api/register/', payload)
  router.push('/login')
}
</script>

<style>
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';
</style>
