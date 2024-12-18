<template>
    <div class="documents">

        <h1 class="page-title">{{ documentStore.documentCount }} Documents in OpenSearch</h1>

        <!-- <button>folders</button><button>list</button> -->

        <SegmentButton :options="['Folders', 'List']" v-model="selectedOption"/>

        <!-- <div> <h2> {{selectedOption}}</h2></div> -->

        <DocumentFolderStructure v-if="selectedOption == 'Folders'" :folders="documentStore.folderStructure"></DocumentFolderStructure>

        <DocumentList v-else-if="selectedOption == 'List'" :list="documentStore.documentList"/>

        <div v-if="isLoading"><h2>Loading documents...</h2></div>

    </div>
</template>

<script setup lang="ts">
import DocumentFolderStructure from "../components/Documents/DocumentFolderStructure.vue";
import DocumentList from "../components/Documents/DocumentList.vue";
import { ref, onMounted } from 'vue';
import SegmentButton from '../components/ui/SegmentButton.vue';

import { useDocumentStore } from '../stores/documentStore';
const documentStore = useDocumentStore();

const isLoading = ref(true);

const selectedOption = ref('Folders');

onMounted(() => {
    documentStore.loadDocumentCount();

    documentStore.loadDocuments(()=>{
        isLoading.value = false;
    });

})

</script>

<style scoped>

</style>