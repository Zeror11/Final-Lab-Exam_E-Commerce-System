<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Add New Product</h2>

    <div class="animate__animated animate__fadeIn">
      <form @submit.prevent="submitProduct" enctype="multipart/form-data">
        <div class="mb-3">
          <label class="form-label">Product Name</label>
          <input v-model="form.name" type="text" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" required></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">Price</label>
          <input v-model="form.price" type="number" class="form-control" step="0.01" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Stock</label>
          <input v-model="form.stock" type="number" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Product Image</label>
          <input type="file" class="form-control" @change="handleFileUpload" accept="image/*" required />
        </div>

        <button type="submit" class="btn btn-primary w-100 shadow-sm hover-shadow">Add Product</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const form = ref({
  name: '',
  description: '',
  price: '',
  stock: '',
})
const imageFile = ref(null)

const handleFileUpload = (e) => {
  imageFile.value = e.target.files[0]
}

const submitProduct = async () => {
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('price', form.value.price)
    formData.append('stock', form.value.stock)
    formData.append('image', imageFile.value)

    await axios.post('http://localhost:8000/api/products/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${auth.token}`,
      },
    })

    await Swal.fire({
      icon: 'success',
      title: 'Product Added!',
      text: 'Your new product has been successfully added.',
      confirmButtonColor: '#3085d6',
    })

    router.push('/')
  } catch (err) {
    console.error(err)
    Swal.fire({
      icon: 'error',
      title: 'Oops!',
      text: 'Failed to add product. Please try again.',
      confirmButtonColor: '#d33',
    })
  }
}
</script>

<style scoped>
.animate__fadeIn {
  animation: fadeIn 1s ease-in-out;
}

.hover-shadow:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

form {
  max-width: 600px;
  margin: 0 auto;
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style>
