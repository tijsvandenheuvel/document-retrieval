<template>
    <div class="document-item" :class="{'dark': theme == 'dark'}" @mouseover="isHovered = true" @mouseleave="isHovered = false">

        <div class="document-header">

            <a :class="{'empty': document.content.length == 0}" href="#" @click.prevent="toggleCard">{{ document.title }}</a>

        </div>

        <div class="document-card" v-if="isOpen">

            <div class="document-card-item">
                <span class="dci-l">Title:</span> <span class="dci-r">{{ document.title }}</span>
            </div>
            <div class="document-card-item">
                <span class="dci-l">File Path:</span> <span class="dci-r">{{ document.file_path }}</span>
            </div>
            <div class="document-card-item">
                <span class="dci-l">Snippet:</span> <span class="dci-r">{{ document.content }}</span>
            </div>

            <div class="actions">
                <button @click="openFile(document.file_path)">Open File</button>
                <button @click="downloadFile(document.file_path)">Download File</button>
            </div>
        </div>


    </div>
</template>

<script setup lang="ts">
import { type Document } from '../../stores/documentStore';
import { ref, toRefs } from 'vue';
// import { ref, toRefs, watch, type Ref } from 'vue'

const props = defineProps<{
    document: Document,
    theme: string,
}>()

const { document, theme } = toRefs(props);

const isOpen = ref(false);
const isHovered = ref(false);

const toggleCard = () => {
    isOpen.value = !isOpen.value;
}

function openFile(filePath: string) {
    const relative_file_path = filePath.split('documents/')[1];

    fetch(`http://localhost:5000/open/${relative_file_path}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`File is being opened: ${relative_file_path}`);
            } else {
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => alert(`Request failed: ${error}`));
}

function downloadFile(filePath: string) {
    const relative_file_path = filePath.split('documents/')[1];

    const link = window.document.createElement('a');
    link.href = `http://localhost:5000/download/${relative_file_path}`; // Endpoint for downloading the file
    const l = relative_file_path.split('/').pop(); // Optional: specify default name for download
    if (l) {
        link.download = l;
    }
    console.log(link)
    window.document.body.appendChild(link);
    link.click();
    window.document.body.removeChild(link);
}

</script>

<style scoped>
.document-header {
    text-align: left;
    /* border: solid ; */
}

.document-item {
    /* margin-bottom: 10px; */
    color: #000;
    /* display: flex; */
    padding: 5px;
    margin: 5px;
    background-color: #f9f9f9;
    transition: background-color 0.3s;
}

.document-item:hover {
    background-color: #f0f0f0;
}

.dark{
    background-color: #242424;
    /* color: #fff; */
}

.dark:hover{
    background-color: #333;
}

.document-card {
    /* border: solid green; */
    margin-top: 10px;
    padding: 10px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
    /* display: none; */
    /* color: #000; */
    display: flex;
    flex-direction: column;
    /* align-items: flex-start; */
}

.document-card-item {
    display: flex;
    justify-content: start;
}

.dci-l {
    font-weight: bold;
    width: 100px;
    float: left;
    /* border:solid red; */
    text-align: left;
}

.dci-r {
    text-align: left;
    /* border: solid green; */
    width: 100%;
}


.actions a {
    margin-right: 10px;
    color: #007bff;
    text-decoration: none;
}

.actions a:hover {
    text-decoration: underline;
}

.empty{
    color: crimson;
}

</style>