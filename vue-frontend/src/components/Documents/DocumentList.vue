<template>
    <div class="document-list">

        <!-- <div class="controls">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Search documents..."
                class="search-bar"
            />
            <select v-model="sortOption" class="sort-select">
                <option value="default">Sort by default</option>
                <option value="title up">Sort by Title up</option>
                <option value="title down">Sort by Title down</option>
            </select>
        </div> -->

        <div class="controls">
            <SearchBar placeholder="Search documents..." @update:query="searchQuery = $event" />
            <SortSelector :options="sortOptions" @update:sort="sortOption = $event" />
        </div>

        <ul class="folder-contents">
            <DocumentItem v-for="document in filteredAndSortedDocuments" :key="document.file_path" :document="document" :theme="'dark'" />
        </ul>

    </div>
</template>

<script setup lang="ts">
import { computed, ref, } from 'vue'; //toRefs
import { type Document } from '../../stores/documentStore';
import DocumentItem from "../Documents/DocumentItem.vue";
import SearchBar from "../shared/SearchBar.vue";
import SortSelector from "../shared/SortSelector.vue";

const props = defineProps<{
    list: Document[]
}>()

// const { list } = toRefs(props);

const searchQuery = ref("");
const sortOption = ref("default");

// Sorting options
const sortOptions = [
  { label: "Sort by Default", value: "default" },
  { label: "Sort by Title Up", value: "title up" },
  { label: "Sort by Title Down", value: "title down" },
];

// Computed filtered and sorted documents
const filteredAndSortedDocuments = computed(() => {
  const filtered = props.list.filter((document) =>
    document.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  if (sortOption.value === "title up") {
    return filtered.sort((a, b) => a.title.localeCompare(b.title));
  } else if (sortOption.value === "title down") {
    return filtered.sort((a, b) => b.title.localeCompare(a.title));
  }

  return filtered;
});

</script>

<style scoped>
.folder-contents {
    /* padding: 15px; */
    padding-left: 30px;
    margin: 0;
}

/* .search-bar {
    width: 50%;
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.sort-select {
    padding: 10px;
    border-radius: 5px;
} */
</style>