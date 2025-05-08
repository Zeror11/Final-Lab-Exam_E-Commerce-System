<template>
  <li class="list-group-item d-flex justify-content-between align-items-center bg-light shadow-sm rounded mb-2 cart-item">
    <div>
      <span class="fw-bold text-success">{{ item.product.name }}</span>
      <span class="text-muted">× {{ item.quantity }}</span>
    </div>
    <span class="badge bg-success rounded-pill fs-6">
      ₱{{ (item.product.price * item.quantity).toFixed(2) }}
    </span>
  </li>
</template>

<script>
export default {
  props: {
    item: Object
  }
}
</script>

<style scoped>
.cart-item {
  transition: transform 0.2s ease;
}

.cart-item:hover {
  transform: scale(1.01);
}
</style>
