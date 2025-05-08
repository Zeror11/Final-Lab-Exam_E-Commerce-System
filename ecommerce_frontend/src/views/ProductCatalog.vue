<template>
  <div class="container mt-4">
    <h2>Product Catalog</h2>

    <!-- Success Alert -->
    <transition name="fade">
      <div
        v-if="showAlert"
        class="alert alert-success alert-dismissible fade show"
        role="alert"
      >
        <strong>Success!</strong> Product added to cart.
      </div>
    </transition>

    <!-- Search Input -->
    <div class="mb-3">
      <input
        v-model="search"
        @input="fetchProducts"
        class="form-control"
        placeholder="Search products..."
      />
    </div>

    <!-- Product Cards -->
    <div class="row">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="col-md-4 mb-4"
      >
        <div class="card h-100 shadow-sm">
          <img
            :src="product.image"
            class="card-img-top"
            alt="product"
            style="object-fit: cover; height: 200px"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p><strong>₱{{ product.price }}</strong></p>
            <p>
              <strong>Stock:</strong>
              <span
                :class="{
                  'text-danger': product.stock === 0,
                  'text-success': product.stock > 0
                }"
              >
                {{ product.stock }}
              </span>
            </p>
            <span
              class="badge bg-danger mb-2"
              v-if="product.stock === 0"
            >Out of stock</span>

            <!-- Buttons in Single Line -->
            <div class="d-flex gap-2 mt-auto">
              <!-- Add to Cart -->
              <button
                class="btn flex-fill"
                :class="product.stock > 0 ? 'btn-success' : 'btn-secondary'"
                @click="addToCart(product)"
                :disabled="product.stock <= 0 || !authStore.user || authStore.user.role !== 'customer'"
              >
                {{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
              </button>

              <!-- Admin Buttons -->
              <template v-if="authStore.user && authStore.user.role === 'employee'">
                <router-link
                  :to="{ name: 'EditProduct', params: { id: product.id } }"
                  class="btn btn-warning btn-sm flex-fill"
                >
                  Edit
                </router-link>

                <button
                  type="button"
                  class="btn btn-danger btn-sm flex-fill"
                  @click="deleteProduct(product.id)"
                >
                  Delete
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'

const products = ref([])
const search = ref('')
const showAlert = ref(false)
const cartStore = useCartStore()
const authStore = useAuthStore()

const fetchProducts = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/products/')
    products.value = res.data
  } catch (err) {
    console.error('Failed to fetch products:', err)
  }
}

onMounted(fetchProducts)

const filteredProducts = computed(() =>
  products.value.filter((p) =>
    p.name.toLowerCase().includes(search.value.toLowerCase())
  )
)

const addToCart = async (product) => {
  if (product.stock > 0) {
    try {
      const res = await axios.post(
        `http://localhost:8000/api/products/${product.id}/decrease-stock/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        }
      )

      product.stock = res.data.stock
      cartStore.addToCart(product)

      showAlert.value = true
      setTimeout(() => {
        showAlert.value = false
      }, 2000)
    } catch (error) {
      console.error('Stock update failed:', error)
      alert('Unable to add to cart. Product might be out of stock.')
    }
  }
}

const deleteProduct = async (id) => {
  const confirm = await Swal.fire({
    title: 'Are you sure?',
    text: 'This action cannot be undone!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel'
  })

  if (confirm.isConfirmed) {
    try {
      await axios.delete(`http://localhost:8000/api/products/${id}/`, {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      })

      await Swal.fire('Deleted!', 'Product has been deleted.', 'success')
      fetchProducts() // refresh list
    } catch (error) {
      if (error.response?.data?.error === 'Cannot delete product already ordered.') {
        Swal.fire('Error', 'Product was already ordered and cannot be deleted.', 'error')
      } else {
        Swal.fire('Error', 'Failed to delete product.', 'error')
      }
      console.error(error)
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
