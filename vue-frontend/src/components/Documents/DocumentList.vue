<template>
    <div class="document-list">

        <div class="controls">
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
        </div>

        <ul class="folder-contents">

            <DocumentItem
                v-for="document in filteredAndSortedDocuments"
                :key="document.file_path"
                :document="document"
                :theme="'dark'"
            />

        </ul>

    </div>
</template>

<script setup lang="ts">
import { computed, ref,toRefs } from 'vue';
import { type Document } from '../../stores/documentStore';
import DocumentItem from "../Documents/DocumentItem.vue";

const props = defineProps<{
    list: Document[]
}>()

const { list } = toRefs(props);

const searchQuery = ref("");
const sortOption = ref("default"); 

const filteredAndSortedDocuments = computed(() => {
    // Filter documents by search query
    const filtered = props.list.filter((document) =>
        document.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    );

    // Sort documents based on the selected sorting option
    if (sortOption.value === "title up") {
        return filtered.sort((a, b) => a.title.localeCompare(b.title));
    } else if (sortOption.value === "title down") {
        return filtered.sort((a, b) => b.title.localeCompare(a.title));
    } 
    // else if (sortOption.value === "date") {
    //     return filtered.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    // }
    return filtered;
});

</script>

<style scoped>

.folder-contents {
    /* padding: 15px; */
    padding-left: 30px;
    margin: 0;
}

</style>