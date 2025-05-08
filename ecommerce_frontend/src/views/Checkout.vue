<template>
  <div class="container mt-4">
    <h2>Checkout</h2>
    <div v-if="cartItems.length === 0">Your cart is empty.</div>
    <div v-else>
      <ul class="list-group">
        <li v-for="item in cartItems" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ item.product.name }} (x{{ item.quantity }})
          <span>₱{{ (item.product.price * item.quantity).toFixed(2) }}</span>
        </li>
      </ul>
      <div class="mt-3">
        <strong>Total: ₱{{ totalPrice.toFixed(2) }}</strong>
      </div>
      <button class="btn btn-success mt-3" @click="submitCheckout">Confirm Checkout</button>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '@/store/cart'
import api from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const cartStore = useCartStore()
    const router = useRouter()

    const submitCheckout = async () => {
      try {
        const response = await api.post('/checkouts/', {
          order: cartStore.orderId
        })
        cartStore.clearCart()
        router.push('/summary')
      } catch (error) {
        alert('Checkout failed.')
        console.error(error)
      }
    }

    return {
      cartItems: cartStore.items,
      totalPrice: cartStore.totalPrice,
      submitCheckout
    }
  }
}
</script>
