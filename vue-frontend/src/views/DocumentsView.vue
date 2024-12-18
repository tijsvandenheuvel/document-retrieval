<template>
    <div class="documents">

        <h1 class="page-title">{{ documentStore.documentCount }} Documents in OpenSearch</h1>

        <DocumentFolderStructure :folders="documentStore.folderStructure"></DocumentFolderStructure>

        <div v-if="isLoading"><h2>Loading...</h2></div>

    </div>
</template>

<script setup lang="ts">
import DocumentFolderStructure from "../components/Documents/DocumentFolderStructure.vue";
// import DocumentList from "../components/Documents/DocumentList.vue";
import { ref, onMounted } from 'vue';

import { useDocumentStore } from '../stores/documentStore';
const documentStore = useDocumentStore();

const isLoading = ref(true);

onMounted(() => {
    documentStore.loadDocumentCount();

    documentStore.loadDocuments(()=>{
        isLoading.value = false;
    });
})

</script>

<style scoped>

/* .container {
    display: flex;
    flex-wrap: wrap;
    margin: 0 auto;
    padding: 10px;
    background: #fff;
    min-height: 100vh;
}

.document-container {
    flex-direction: column;
} */

</style>