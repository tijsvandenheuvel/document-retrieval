<template>
    <div class="segment-button">
      <div
        class="segment-options"
        :style="`--segments: ${options.length}; --active-index: ${activeIndex}`"
      >
        <div
          class="segment-slider"
          :style="`--slider-left: ${activeIndex * 100 / options.length}%;`"
        ></div>
        <button
          v-for="(option, index) in options"
          :key="index"
          class="segment-option"
          :class="{ active: activeIndex === index }"
          @click="handleSelection(index)"
        >
          {{ option }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  // Props for options and default selection
  const props = defineProps({
    options: {
      type: Array as () => string[],
      required: true,
    },
    modelValue: {
      type: String,
      default: '',
    },
  });
  
  const activeIndex = ref(props.options.indexOf(props.modelValue));
  
  // Emit the selected value on change
  const emit = defineEmits(['update:modelValue']);
  const handleSelection = (index: number) => {
    activeIndex.value = index;
    emit('update:modelValue', props.options[index]);
  };
  </script>
  
  <style scoped>
  .segment-button {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    width: 100%;
  }
  
  .segment-options {
    display: grid;
    grid-template-columns: repeat(var(--segments), 1fr);
    position: relative;
    width: 100%;
    max-width: 400px;
    height: 50px;
    background: #f3f3f3;
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .segment-slider {
    position: absolute;
    top: 0;
    left: var(--slider-left);
    width: calc(100% / var(--segments));
    height: 100%;
    background: #4caf50;
    border-radius: 25px;
    transition: all 0.3s ease-in-out;
  }
  
  .segment-option {
    position: relative;
    z-index: 2;
    border: none;
    outline: none;
    background: transparent;
    font-size: 16px;
    font-weight: 600;
    color: #666;
    cursor: pointer;
    transition: color 0.3s ease-in-out;
  }
  
  .segment-option.active {
    color: white;
  }
  
  .segment-option:hover {
    color: #333;
  }
  </style>