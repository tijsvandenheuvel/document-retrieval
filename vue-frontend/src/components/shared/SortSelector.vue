<template>
  <div class="sort-selector">
    <button class="sort-button" @click="toggleDropdown">
      {{ selectedOption.label }}
    </button>
    <ul v-if="dropdownOpen" class="sort-options">
      <li
        v-for="option in options"
        :key="option.value"
        @click="selectOption(option)"
        :class="{ selected: option.value === selectedOption.value }"
      >
        {{ option.label }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";

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

// Reactive state
const selectedOption = ref<SortOption>({ label: "Sort by Default", value: "default" });
const dropdownOpen = ref(false);

// Toggle the dropdown menu
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

// Handle option selection
const selectOption = (option: SortOption) => {
  selectedOption.value = option;
  dropdownOpen.value = false; // Close the dropdown
  emit("update:sort", option.value);
};
</script>

<style scoped>
.sort-selector {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: start;

  /* TODO: do proper flex spacing */
  margin-right: 10px; 

  width: 170px;
}

.sort-button {
  width: 100%;
  padding: 8px 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  /* background-color: #fff; */
  cursor: pointer;
  text-align: left;
  transition: border-color 0.2s, background-color 0.2s;
  background-color: inherit;
  height: 43px;
}

.sort-button:hover {
  border-color: #999;
  background-color: #333;
}

.sort-options {
  position: absolute;
  top: 50px;
  left: 0;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  /* background-color: #fff; */
  z-index: 1000;
  padding: 0;
  margin: 0;
  list-style: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sort-options li {
  padding: 8px 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sort-options li:hover {
  background-color: #333;
}

.sort-options li.selected {
  font-weight: bold;
  background-color: #555;
}
</style>