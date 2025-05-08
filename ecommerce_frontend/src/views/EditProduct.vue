<template>
  <div class="container mt-4">
    <h2>Edit Product</h2>

    <form @submit.prevent="updateProduct" enctype="multipart/form-data">
      <div class="mb-3">
        <label>Name</label>
        <input v-model="form.name" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label>Description</label>
        <textarea v-model="form.description" class="form-control" required></textarea>
      </div>

      <div class="mb-3">
        <label>Price</label>
        <input v-model="form.price" type="number" class="form-control" required />
      </div>

      <div class="mb-3">
        <label>Stock</label>
        <input v-model="form.stock" type="number" class="form-control" required />
      </div>

      <div class="mb-3">
        <label>Current Image</label><br />
        <img :src="form.image" alt="Current Product Image" class="img-thumbnail" width="200" v-if="form.image" />
      </div>

      <div class="mb-3">
        <label>Change Image (optional)</label>
        <input type="file" class="form-control" @change="handleFileUpload" accept="image/*" />
      </div>

      <button type="submit" class="btn btn-primary">Update Product</button>
      <router-link to="/" class="btn btn-secondary ms-2">Cancel</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Swal from 'sweetalert2'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  name: '',
  description: '',
  price: '',
  stock: '',
  image: ''
})

const newImageFile = ref(null)

const fetchProduct = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/products/${route.params.id}/`)
    form.value = res.data
  } catch (error) {
    Swal.fire('Error', 'Failed to load product', 'error')
    console.error(error)
  }
}

const handleFileUpload = (e) => {
  newImageFile.value = e.target.files[0]
}

const updateProduct = async () => {
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('price', form.value.price)
    formData.append('stock', form.value.stock)

    if (newImageFile.value) {
      formData.append('image', newImageFile.value)
    }

    await axios.patch(`http://localhost:8000/api/products/${route.params.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${authStore.token}`
      }
    })

    await Swal.fire('Updated!', 'Product updated successfully.', 'success')
    router.push('/')
  } catch (error) {
    Swal.fire('Error', 'Failed to update product', 'error')
    console.error(error)
  }
}


onMounted(fetchProduct)
</script>

<style scoped>
.img-thumbnail {
  margin-bottom: 10px;
}
</style>
