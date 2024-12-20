<template>
    <input
      v-model="searchQuery"
      type="text"
      :placeholder="placeholder"
      class="search-bar"
      @input="onSearch"
    />
  </template>
  
  <script setup lang="ts">
  import { ref, defineEmits } from 'vue';
  
  // Props
  defineProps({
    placeholder: {
      type: String,
      default: "Search...",
    },
  });
  
  // Emits event
  const emit = defineEmits(["update:query"]);
  
  // Reactive search query
  const searchQuery = ref("");
  
  // Emit search query on input
  const onSearch = () => {
    emit("update:query", searchQuery.value);
  };
  </script>
  
  <style scoped>
  .search-bar {
    width: 50%;
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>