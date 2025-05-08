<template>
  <div class="container mt-4">
    <h2 class="mb-3">📦 Order Summary</h2>

    <div v-if="loading" class="alert alert-info">Loading order details...</div>
    <div v-else-if="!order">
      <div class="alert alert-warning">No recent order found.</div>
    </div>
    <div v-else>
      <p>
        Thank you for your order, <strong>{{ authStore.user.username }}</strong>!
      </p>
      <p>Order ID: <span class="text-primary fw-semibold">#{{ order.id }}</span></p>

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

      <p class="fw-bold fs-5">Total: ₱{{ total }}</p>
    </div>

    <router-link to="/" class="btn btn-primary mt-3">
      🛍 Go Back to Catalog
    </router-link>
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
