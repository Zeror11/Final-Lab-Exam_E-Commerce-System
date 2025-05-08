<template>
  <div class="container mt-4">
    <h2 class="mb-3">📦 Order History</h2>

    <div v-if="loading" class="alert alert-info">Loading order history...</div>
    <div v-else-if="orders.length === 0">
      <div class="alert alert-warning">No orders found.</div>
    </div>
    <div v-else>
      <div v-for="order in paginatedOrders" :key="order.id" class="order-card mb-4">
        <h4>Order ID: <span class="text-primary fw-semibold">#{{ order.id }}</span></h4>
        <p>Status: <span class="status-complete">Complete Order</span></p>
        
        <table class="table table-striped mt-3">
          <thead class="table-light">
            <tr>
              <th>Product</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.product">
              <td>{{ item.product_name }}</td>
              <td>{{ item.quantity }}</td>
              <td>₱{{ item.price }}</td>
              <td>₱{{ item.quantity * item.price }}</td>
            </tr>
          </tbody>
        </table>

        <p class="fw-bold fs-5">Total: ₱{{ getOrderTotal(order) }}</p>
      </div>

      <div class="d-flex justify-content-between align-items-center mt-3">
        <!-- Pagination controls -->
        <div>
          <button
            class="btn btn-outline-secondary"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            Previous
          </button>
          <span class="mx-3">{{ currentPage }} / {{ pageCount }}</span>
          <button
            class="btn btn-outline-secondary"
            :disabled="currentPage === pageCount"
            @click="currentPage++"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <router-link to="/" class="btn btn-primary mt-3">
      🛍 Go Back to Catalog
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const orders = ref([])  // Store all orders
const loading = ref(true)
const currentPage = ref(1)
const itemsPerPage = 5

// Fetch all orders for the current user
const fetchOrderHistory = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/orders/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    // Filter orders by the logged-in user
    const userOrders = res.data.filter(o => o.customer === authStore.user.id)
    orders.value = userOrders
  } catch (err) {
    console.error('Failed to fetch order history:', err)
  } finally {
    loading.value = false
  }
}

// Calculate the total price for each order
const getOrderTotal = (order) => {
  return order.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
}

// Pagination logic
const pageCount = computed(() => {
  if (!orders.value || orders.value.length === 0) return 1
  return Math.ceil(orders.value.length / itemsPerPage)
})

const paginatedOrders = computed(() => {
  if (!orders.value) return []
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return orders.value.slice(start, end)
})

onMounted(fetchOrderHistory)
</script>

<style scoped>
.order-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #f9f9f9;
}

.order-card h4 {
  font-size: 1.2rem;
}

.order-card table {
  width: 100%;
}

.order-card table th,
.order-card table td {
  text-align: center;
}

.order-card table th {
  background-color: #f1f1f1;
}

.order-card .btn-outline-secondary {
  margin-top: 5px;
}

/* Highlight the Complete Order status */
.status-complete {
  background-color: #28a745;  /* Green background */
  color: white;
  padding: 4px 8px;
  border-radius: 5px;
  font-weight: bold;
}
</style>
