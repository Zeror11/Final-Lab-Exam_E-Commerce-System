// src/store/cart.js
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cart')) || []
  }),
  actions: {
    addToCart(product) {
      const existing = this.items.find(item => item.id === product.id)
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({ ...product, quantity: 1 })
      }
    },

    removeFromCart(id) {
      const index = this.items.findIndex(item => item.id === id)
      if (index !== -1) this.items.splice(index, 1)
    },
    
    
    clearCart() {
      this.items = []
      this.save()
    },

    save() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    }
  }
})
