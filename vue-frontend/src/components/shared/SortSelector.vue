<template>
    <select v-model="sortOption" class="sort-select" @change="onSortChange">
        <option v-for="option in options" :key="option.value" :value="option.value">
            {{ option.label }}
        </option>
    </select>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue';

interface SortOption {
    label: string; // Label displayed in the dropdown
    value: string; // Value for sorting logic
}

// Props
defineProps<{
  options: SortOption[]; // Array of SortOption objects
}>();

// Emits event
const emit = defineEmits(["update:sort"]);

// Reactive sort option
const sortOption = ref("default");

// Emit selected sort option
const onSortChange = () => {
    emit("update:sort", sortOption.value);
};
</script>

<style scoped>
.sort-select {
    padding: 10px;
    border-radius: 5px;
}
</style>