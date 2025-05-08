<template>
  <div class="container mt-4">
    <h2>Order History</h2>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex justify-content-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- No Orders Message -->
    <div v-else-if="orders.length === 0">
      <p class="text-center">No past orders found.</p>
    </div>

    <!-- Order List -->
    <div v-else>
      <div v-for="order in orders" :key="order.id" class="card mb-3 shadow-sm">
        <div class="card-header bg-primary text-white">
          <strong>Order #{{ order.id }}</strong> — {{ formatDate(order.date_ordered) }}
        </div>
        <ul class="list-group list-group-flush">
          <li
            v-for="item in order.items"
            :key="item.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <strong>{{ item.product_name }}</strong> — ₱{{ item.price }} × {{ item.quantity }}
            </div>
            <strong>₱{{ (item.price * item.quantity).toFixed(2) }}</strong>
          </li>
          <li class="list-group-item text-end fw-bold">
            <span>Total:</span> ₱{{ order.total.toFixed(2) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const orders = ref([])
const loading = ref(true)
const authStore = useAuthStore()

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/orders/history/', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    orders.value = res.data
  } catch (err) {
    console.error('Failed to load order history:', err)
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}
</script>

<style scoped>
.card {
  border: none;
}
.card-header {
  font-size: 1.1rem;
  background-color: #007bff;
}
.card-header strong {
  color: white;
}
.list-group-item {
  font-size: 0.9rem;
}
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
