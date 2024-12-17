<template>
    <div class="document-folder">

        <div class="folder-header" @click="toggleFolder">
            📁 {{ folder.folder }} ({{ folder.count }} documents)
        </div>

        <ul
            v-if="isOpen" class="folder-contents" v-for="document in folder.documents">

            <DocumentItem :document="document"></DocumentItem>

        </ul>

    </div>
</template>

<script setup lang="ts">
import DocumentItem from "../Documents/DocumentItem.vue";
import { type Folder } from '../../stores/documentStore';
import { ref, toRefs } from 'vue';
// import { ref, toRefs, watch, type Ref } from 'vue';

const props = defineProps<{
    folder: Folder
}>()

const { folder } = toRefs(props);

const isOpen = ref(false);

const toggleFolder = () => {
    isOpen.value = !isOpen.value;
    // console.log(`Folder "${folder.value.folder}" is now ${isOpen.value ? 'open' : 'closed'}`);
};


</script>

<style scoped>

.document-folder {
    background: #f9f9f9;
    margin: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.folder-header {
    font-weight: bold;
    cursor: pointer;
    /* border: solid red; */
    padding: 15px;
    color: #000;
    display: flex;
}

.folder-header:hover {
    background-color: #f0f0f0;
}

.folder-contents {
    /* display: none; */

    padding: 15px;
    padding-left: 30px;
}

</style>