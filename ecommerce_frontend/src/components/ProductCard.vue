<template>
  <div class="card h-100 border-0 shadow-sm product-card">
    <img :src="product.image" class="card-img-top rounded-top" alt="Product" />
    <div class="card-body text-center bg-light">
      <h5 class="card-title text-success fw-bold">{{ product.name }}</h5>
      <p class="card-text text-muted">₱{{ product.price.toFixed(2) }}</p>
      <router-link :to="`/product/${product.id}`" class="btn btn-success btn-sm">
        🍍 View Details
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    product: Object
  }
}
</script>

<style scoped>
.product-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 15px;
}

.product-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 128, 0, 0.2);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
