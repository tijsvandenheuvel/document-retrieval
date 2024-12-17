<template>
    <div class="document-item">

        <div class="document-header">

            <a href="#" @click.prevent="toggleCard">{{ document.title }}</a>

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

                <!-- TODO rewrite open file with vue functionality -->
                <a href="javascript:void(0);" onclick="openFile('{{ doc.file_path | escape_single_quotes }}')">Open
                    File</a>

                <!-- TODO rewrite download file with vue functionality -->
                <a href="javascript:void(0);"
                    onclick="downloadFile('{{ doc.file_path | escape_single_quotes }}')">Download
                    File</a>

            </div>
        </div>


    </div>
</template>

<script setup lang="ts">
import { type Document } from '../../stores/documentStore';
import { ref, toRefs } from 'vue';
// import { ref, toRefs, watch, type Ref } from 'vue'

const props = defineProps<{
    document: Document
}>()

const { document } = toRefs(props);

const isOpen = ref(false);

const toggleCard = () => {
    isOpen.value = !isOpen.value;
}

</script>

<style scoped>

.document-header{
    text-align: left;
    /* border: solid ; */
}

.document-item {
    /* margin-bottom: 10px; */
    color: #000;
    /* display: flex; */
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

.dci-r{
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
</style>