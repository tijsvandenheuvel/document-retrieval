<template>
    <div class="document-folder-structure">

        <div class="controls">
            <SearchBar placeholder="Search folders..." @update:query="searchQuery = $event" />
            <SortSelector :options="sortOptions" @update:sort="sortOption = $event" />
        </div>

        <ul class="folder-list" v-for="folder in filteredAndSortedFolders">
            <DocumentFolder :folder="folder" :theme="'light'"></DocumentFolder>
        </ul>

    </div>
</template>

<script setup lang="ts">
import DocumentFolder from "../Documents/DocumentFolder.vue";
import SearchBar from "../shared/SearchBar.vue";
import SortSelector from "../shared/SortSelector.vue";
import { ref, computed } from 'vue';
// import { ref, toRefs, watch, type Ref } from 'vue';

const props = defineProps<{
    folders: any[]
}>()

// const { folders } = toRefs(props);

const searchQuery = ref("");
const sortOption = ref("default");

// Sorting options
const sortOptions = [
  { label: "Sort by Default", value: "default" },
  { label: "Sort by Title Up", value: "title up" },
  { label: "Sort by Title Down", value: "title down" },
];


const filteredAndSortedFolders = computed(() => {
  const filtered = props.folders.filter((folder) =>
    folder.folder.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  if (sortOption.value === "title up") {
    return filtered.sort((a, b) => a.folder.localeCompare(b.folder));
  } else if (sortOption.value === "title down") {
    return filtered.sort((a, b) => b.folder.localeCompare(a.folder));
  }

  return filtered;
});

</script>

<style scoped>
.folder-list {
    list-style-type: none;
    padding: 0;
    margin: 0 10px;
}

.controls {
    display: flex;
    /* border: solid #ccc 1px; */
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}
</style>