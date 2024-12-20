<template>
    <div class="document-list">

        <div class="controls">
            <SearchBar placeholder="Search documents..." @update:query="searchQuery = $event" />
            <SortSelector :options="sortOptions" @update:sort="sortOption = $event" />
            <FiltersControl :fileTypes="fileTypeOptions" @update:filters="filters = $event" />
        </div>

        <ul class="folder-contents">
            <DocumentItem v-for="document in filteredAndSortedDocuments" :key="document.file_path" :document="document"
                :theme="'dark'" />
        </ul>

    </div>
</template>

<script setup lang="ts">
import { computed, ref, } from 'vue'; //toRefs
import { type Document } from '../../stores/documentStore';
import DocumentItem from "../Documents/DocumentItem.vue";
import SearchBar from "../shared/SearchBar.vue";
import SortSelector from "../shared/SortSelector.vue";
import FiltersControl from "../shared/FiltersControl.vue";

const props = defineProps<{
    list: Document[]
}>()

const searchQuery = ref("");
const sortOption = ref("default");
const fileTypeOptions = ['pdf', 'docx', 'xlsx', 'other'];

const filters = ref({
    notEmpty: true,
    onlyEmpty: true,
    fileTypes: [...fileTypeOptions],
});

// Sorting options
const sortOptions = [
    { label: "Sort by Default", value: "default" },
    { label: "Sort by Title Up", value: "title up" },
    { label: "Sort by Title Down", value: "title down" },
];

// Computed filtered and sorted documents
const filteredAndSortedDocuments = computed(() => {
    let filtered = props.list;


    // Apply search filter
    filtered = filtered.filter((document) =>
        document.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    );

    // Apply file type filter
    if (filters.value.fileTypes.length > 0) {
        filtered = filtered.filter((document) => {
            const predefinedFileTypes = fileTypeOptions.filter(type => type !== 'other');
            const isPredefined = predefinedFileTypes.includes(document.fileType);

            if (filters.value.fileTypes.includes('other')) {
                // Include documents that are not in predefined file types
                return (
                    (!isPredefined && filters.value.fileTypes.includes('other')) ||
                    (isPredefined && filters.value.fileTypes.includes(document.fileType))
                );
            }

            // Otherwise, include only the selected predefined file types
            return filters.value.fileTypes.includes(document.fileType);
        });
    } else {
        return [];
    }

    // Apply content filter
    if (!filters.value.notEmpty) {
        filtered = filtered.filter((document) => document.isEmpty);
    }
    if (!filters.value.onlyEmpty) {
        filtered = filtered.filter((document) => !document.isEmpty);
    }

    // Apply sorting
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
    padding-left: 30px;
    margin: 0;
}

.controls {
    display: flex;
    /* border: solid #ccc 1px; */
    justify-content: center;
    align-items: center;
}
</style>