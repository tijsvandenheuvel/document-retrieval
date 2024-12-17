<template>
    <div class="documents">

        <h1 class="page-title">{{ numberOfDocuments }} Documents in OpenSearch</h1>

        <DocumentFolderStructure :folders="folders"></DocumentFolderStructure>

        <!-- <DocumentList></DocumentList> -->

        <!-- <ul class="folder-list" v-for="folder in folders">
            <li class="folder">
                <div class="folder-header" @click="toggleFolder('folder-{{ loop.index }}')">
                    📁 {{ folder.folder }} ({{ folder.count }} documents)
                </div>
                <ul id="folder-{{ loop.index }}" class="folder-contents" v-for="doc in folder.documents">
                    <li class="document-item">
                        <div class="document-header">
                            <a href="#" @click="toggleCard('card-{{ doc.unique_id }}')">{{ doc.title }}</a>
                        </div>
                        <div id="card-{{ doc.unique_id }}" class="document-card">
                            <p><strong>Title:</strong> {{ doc.title }}</p>
                            <p><strong>File Path:</strong> {{ doc.file_path }}</p>
                            <p><strong>Snippet:</strong> {{ doc.content }}</p>
                            <div class="actions">
                                <a href="javascript:void(0);"
                                    onclick="openFile('{{ doc.file_path | escape_single_quotes }}')">Open File</a>
                                <a href="javascript:void(0);"
                                    onclick="downloadFile('{{ doc.file_path | escape_single_quotes }}')">Download
                                    File</a>
                            </div>
                        </div>
                    </li>
                </ul>
            </li>
        </ul> -->

    </div>
</template>

<script setup lang="ts">
import DocumentFolderStructure from "../components/Documents/DocumentFolderStructure.vue";
// import DocumentList from "../components/Documents/DocumentList.vue";
import { ref, onMounted, type Ref } from 'vue';
import * as api from "../utils/api";


let numberOfDocuments: Ref<number> = ref(0);
let folders: Ref<any[]> = ref([]);

const getNumberOfDocuments  = () => {

}

const getDocuments  = () => {
    api.getAllDocuments((response: []) => {folders.value = response});

}


onMounted(() => {
    getNumberOfDocuments();
    getDocuments();
})

// const toggleCard = (id: string) => {
//     var card = document.getElementById(id);
//     if(card != null){
//         if (card.style.display !== "block") {
//         card.style.display = "block";
//     } else {
//         card.style.display = "none";
//     }
// }
//     }

// const toggleFolder = (folderId: string) => {
//     const folder = document.getElementById(folderId);
//     if(folder != null){
//         folder.style.display = folder.style.display !== 'block' ? 'block' : 'none';
//     }
// }

</script>

<style scoped>

.container {
    display: flex;
    /* flex-wrap: wrap; */
    margin: 0 auto;
    padding: 10px;
    background: #fff;
    min-height: 100vh;
}

.document-container {
    flex-direction: column;
}

/* .folder-list {
    list-style-type: none;
    padding: 0;
    margin: 0 10px;
} */

/* .folder {
    background: #f9f9f9;
    margin: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
} */

/* .folder-header {
    font-weight: bold;
    cursor: pointer;
    padding: 15px;
    color: #000;
    display: flex;
} */

/* .folder-header:hover {
    background-color: #f0f0f0;
} */

/* .folder-contents {
    display: none;

    padding: 15px;
    padding-left: 30px;
} */

/* .document-item {
    margin-bottom: 10px;
    color: #000;
} */

/* .document-card {
    margin-top: 10px;
    padding: 10px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    display: none;
} */

/* .actions a {
    margin-right: 10px;
    color: #007bff;
    text-decoration: none;
}

.actions a:hover {
    text-decoration: underline;
} */
</style>