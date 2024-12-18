<template>
    <div class="document-list">

        <h1>document list</h1>

        <ul class="folder-contents" v-for="document in list">

            <DocumentItem :document="document"></DocumentItem>

        </ul>

    </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue';
import { type Document } from '../../stores/documentStore';
import DocumentItem from "../Documents/DocumentItem.vue";

const props = defineProps<{
    list: Document[]
}>()

const { list } = toRefs(props);

</script>

<style scoped>

.folder-contents {
    padding: 15px;
    padding-left: 30px;
}

</style>