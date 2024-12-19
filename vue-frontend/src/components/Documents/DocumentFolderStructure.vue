<template>
    <div class="document-folder-structure">

        <ul class="folder-list" v-for="folder in folders">

            <DocumentFolder :folder="folder" :theme="'light'"></DocumentFolder>

        </ul>

    </div>
</template>

<script setup lang="ts">
import DocumentFolder from "../Documents/DocumentFolder.vue";
import { toRefs } from 'vue';
// import { ref, toRefs, watch, type Ref } from 'vue';

const props = defineProps<{
    folders: any[]
}>()

const { folders } = toRefs(props);

</script>

<style scoped>

.folder-list {
    list-style-type: none;
    padding: 0;
    margin: 0 10px;
}

</style>