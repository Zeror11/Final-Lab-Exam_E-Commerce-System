<template>
  <div class="container mt-4" v-if="product">
    <div
      class="row justify-content-center animate__animated animate__fadeIn"
    >
      <div class="col-md-8">
        <!-- Product Card -->
        <div class="card shadow-lg rounded">
          <div class="card-body">
            <h2 class="card-title text-center text-success mb-4">{{ product.name }}</h2>
            <!-- Product Image -->
            <div class="text-center">
              <img :src="product.image" class="img-fluid mb-3" style="max-width: 300px;" />
            </div>
            <!-- Product Description -->
            <p class="text-muted">{{ product.description }}</p>
            <div class="d-flex justify-content-between align-items-center">
              <!-- Price -->
              <h4 class="fw-bold">₱{{ product.price }}</h4>
              <!-- Add to Cart Button -->
              <button
                class="btn btn-success"
                @click="addToCart"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/store/cart'
import api from '@/services/api'

export default {
  setup() {
    const route = useRoute()
    const cartStore = useCartStore()
    const productId = route.params.id
    const product = ref(null)
    const loading = ref(false)

    onMounted(async () => {
      const response = await api.get(`/products/${productId}/`)
      product.value = response.data
    })

    const addToCart = () => {
      loading.value = true
      cartStore.addItem(product.value)
      setTimeout(() => { loading.value = false }, 1000) // simulate loading
    }

    return { product, addToCart, loading }
  }
}
</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';
</style>
