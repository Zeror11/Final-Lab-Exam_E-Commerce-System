<!-- src/views/AdminMonitorView.vue -->
<template>
  <div class="container mt-4">
    <h2>Checkout Monitoring</h2>

    <div class="mb-3 row">
      <label class="col-sm-2 col-form-label">Filter by Date:</label>
      <div class="col-sm-4">
        <input type="date" v-model="filterDate" class="form-control" @change="fetchTransactions" />
      </div>
    </div>

    <table class="table table-bordered" v-if="transactions.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer</th>
          <th>Transaction Date</th>
          <th>Total Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tx in transactions" :key="tx.id">
          <td>{{ tx.id }}</td>
          <td>{{ tx.order_customer_username }}</td>
          <td>{{ formatDate(tx.transaction_date) }}</td>
          <td>₱{{ tx.total_amount }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else>
      <p>No transactions found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const transactions = ref([])
const filterDate = ref('')

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}

async function fetchTransactions() {
  if (!auth.user || auth.user.role !== 'employee') {
    alert('Access denied. Only employees can view this page.')
    return router.push('/')
  }

  try {
    const res = await axios.get('http://localhost:8000/api/checkouts/', {
      headers: {
        Authorization: `Bearer ${auth.token}`
      },
      params: filterDate.value ? { date: filterDate.value } : {}
    })
    transactions.value = res.data
  } catch (err) {
    console.error(err)
    alert('Failed to load transactions.')
  }
}

onMounted(fetchTransactions)
</script>
