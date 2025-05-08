<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center text-primary">📦 Order Summary</h2>

    <div v-if="loading" class="alert alert-info text-center">Loading order details...</div>
    <div v-else-if="!order">
      <div class="alert alert-warning text-center">No recent order found.</div>
    </div>
    <div v-else>
      <p class="text-center mb-4">
        Thank you for your order, <strong>{{ authStore.user.username }}</strong>!
      </p>
      <div class="order-details">
        <p class="text-center">
          <span class="fw-semibold text-primary fs-4">Order ID: #{{ order.id }}</span>
        </p>

        <table class="table table-hover mt-3">
          <thead class="table-dark">
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

        <p class="fw-bold fs-5 text-center mt-3">Total: ₱{{ total }}</p>
      </div>
    </div>

    <div class="d-flex justify-content-center mt-4">
      <router-link to="/" class="btn btn-primary px-4 py-2 rounded-pill shadow-sm">
        🛍 Go Back to Catalog
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const order = ref(null)
const loading = ref(true)

const fetchLatestOrder = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/orders/`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    const userOrders = res.data.filter(o => o.customer === authStore.user.id)
    const latestOrder = userOrders[userOrders.length - 1] || null
    order.value = latestOrder

    if (latestOrder) {
      Swal.fire({
        title: 'Order Confirmed!',
        text: `Order #${latestOrder.id} was placed successfully.`,
        icon: 'success',
        timer: 3000,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
      })
    }
  } catch (err) {
    console.error('Failed to fetch orders:', err)
    Swal.fire('Error', 'Failed to load your order summary.', 'error')
  } finally {
    loading.value = false
  }
}

const total = computed(() => {
  if (!order.value) return 0
  return order.value.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
})

onMounted(fetchLatestOrder)
</script>

<style scoped>
.order-details {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}

.table-dark th {
  background-color: #343a40;
  color: white;
}

.table td,
.table th {
  text-align: center;
  vertical-align: middle;
}

.text-center {
  text-align: center;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.shadow-sm {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mt-4 {
  margin-top: 1.5rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.px-4 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.rounded-pill {
  border-radius: 50px;
}
</style>
