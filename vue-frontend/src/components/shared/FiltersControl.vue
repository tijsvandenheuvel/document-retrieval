<template>
    <div class="filters-control">
        <fieldset>
            <legend>Content</legend>
            <label>
                <input type="checkbox" v-model="filters.notEmpty" /> Not Empty
            </label>
            <label>
                <input type="checkbox" v-model="filters.onlyEmpty" /> Only Empty
            </label>
        </fieldset>
        <fieldset>
            <legend>File Type</legend>
            <label v-for="type in fileTypes" :key="type">
                <input type="checkbox" :value="type" v-model="filters.fileTypes" /> {{ type }}
            </label>
        </fieldset>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch } from "vue";

// Props
const props = defineProps({
    fileTypes: {
        type: Array as () => string[],
        default: () => ["pdf", "docx", "xlsx", "other"], // Default file types
    },
});

// Emit event to update filters
const emit = defineEmits(["update:filters"]);

// Filters state (initially all checked)
const filters = ref({
  notEmpty: true,
  onlyEmpty: true,
  fileTypes: props.fileTypes, // Initially all file types are checked
});

// Watch filters and emit changes
watch(
    filters,
    (newFilters) => {
        emit("update:filters", newFilters);
    },
    { deep: true }
);
</script>

<style scoped>
.filters-control {
    display: flex;
    gap: 10px;
    width: 350px;
}

fieldset {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    text-align: left;
}

legend {
    font-weight: bold;
    padding: 0 5px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-size: 14px;
}

input[type="checkbox"] {
    margin-right: 5px;
}
</style>