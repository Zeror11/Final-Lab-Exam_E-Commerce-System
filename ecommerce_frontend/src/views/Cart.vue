<template>
  <div class="container mt-4">
    <h2 class="mb-4">🛒 Your Cart</h2>
    <div v-if="cartItems.length === 0" class="alert alert-info">
      Your cart is empty.
    </div>
    <div v-else>
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th>Product</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Subtotal</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartItems" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.quantity }}</td>
            <td>₱{{ item.price }}</td>
            <td>₱{{ item.quantity * item.price }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="confirmRemove(item)">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <p class="fw-bold fs-5">Total: ₱{{ total }}</p>

      <button class="btn btn-primary" @click="checkout" :disabled="loading">
        {{ loading ? 'Processing...' : 'Checkout' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)

const cartItems = computed(() => cartStore.items)
const total = computed(() =>
  cartItems.value.reduce((acc, item) => acc + item.price * item.quantity, 0)
)

async function confirmRemove(item) {
  const result = await Swal.fire({
    title: `Remove "${item.name}"?`,
    text: 'This will also restore the stock.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, remove it',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6'
  })

  if (result.isConfirmed) {
    await remove(item)
    Swal.fire('Removed!', `"${item.name}" was removed from your cart.`, 'success')
  }
}

async function remove(item) {
  try {
    await axios.post(
      `http://localhost:8000/api/products/${item.id}/increase-stock/`,
      { quantity: item.quantity },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    )
  } catch (err) {
    console.error('Failed to increase stock:', err)
  }

  cartStore.removeFromCart(item.id)
}

async function checkout() {
  if (!authStore.user || authStore.user.role !== 'customer') {
    Swal.fire('Access Denied', 'Only registered customers can checkout.', 'error')
    return
  }

  loading.value = true
  try {
    const orderRes = await axios.post(
      'http://localhost:8000/api/orders/',
      {
        customer: authStore.user.id,
        items: cartItems.value.map((item) => ({
          product: item.id,
          quantity: item.quantity
        }))
      },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )

    await axios.post(
      'http://localhost:8000/api/checkouts/',
      { order: orderRes.data.id },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )

    cartStore.clearCart()

    Swal.fire({
      title: 'Success!',
      text: 'Your order was placed successfully!',
      icon: 'success',
      confirmButtonText: 'OK'
    }).then(() => router.push('/summary'))
  } catch (error) {
    console.error(error)
    Swal.fire('Checkout Failed', 'Something went wrong during checkout.', 'error')
  } finally {
    loading.value = false
  }
}
</script>
