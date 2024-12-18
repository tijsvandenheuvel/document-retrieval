<template>
    <div class="documents">

        <h1 class="page-title">{{ numberOfDocuments }} Documents in OpenSearch</h1>

        <DocumentFolderStructure :folders="folders"></DocumentFolderStructure>

        <div v-if="isLoading"><h2>Loading...</h2></div>

    </div>
</template>

<script setup lang="ts">
import DocumentFolderStructure from "../components/Documents/DocumentFolderStructure.vue";
// import DocumentList from "../components/Documents/DocumentList.vue";
import { ref, onMounted, type Ref } from 'vue';
import * as api from "../utils/api";


let numberOfDocuments: Ref<number> = ref(0);
let folders: Ref<any[]> = ref([]);

const isLoading = ref(true);

// TODO call api  & handle data in pinia store

const getNumberOfDocuments  = () => {
    api.getDocumentCount((response: number) => {numberOfDocuments.value = response})
}

const getDocuments  = () => {
    api.getAllDocuments((response: []) => {
        isLoading.value = false;
        folders.value = response
    });
}


onMounted(() => {
    getNumberOfDocuments();
    getDocuments();
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