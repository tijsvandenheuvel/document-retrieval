<template>
    <div class="documents">

        <h1 class="page-title">{{ documentStore.documentCount }} Documents in OpenSearch</h1>

        <!-- <button>folders</button><button>list</button> -->

        <SegmentButton :options="['Folders', 'List']" v-model="selectedOption"/>

        <div> <h2> {{selectedOption}}</h2></div>

        <DocumentFolderStructure :folders="documentStore.folderStructure"></DocumentFolderStructure>

        <div v-if="isLoading2"><h2>Loading list...</h2></div>
        <div v-if="isLoading1"><h2>Loading folders...</h2></div>

    </div>
</template>

<script setup lang="ts">
import DocumentFolderStructure from "../components/Documents/DocumentFolderStructure.vue";
// import DocumentList from "../components/Documents/DocumentList.vue";
import { ref, onMounted } from 'vue';
import SegmentButton from '../components/ui/SegmentButton.vue';

import { useDocumentStore } from '../stores/documentStore';
const documentStore = useDocumentStore();

const isLoading1 = ref(true);
const isLoading2 = ref(true);

const selectedOption = ref('Folders');

onMounted(() => {
    documentStore.loadDocumentCount();

    documentStore.loadDocuments(()=>{
        isLoading1.value = false;
    });

    documentStore.loadDocumentList(()=>{
        isLoading2.value = false;
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