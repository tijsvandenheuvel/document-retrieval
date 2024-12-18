import { defineStore } from 'pinia';
import { ref, type Ref } from 'vue'
import * as api from "../utils/api";

export interface Folder {
    folder:string;
    count: number;
    documents: Document[];
}

export interface Document {
    title: string;
    file_path: string;
    content: string;
}

export const useDocumentStore = defineStore('documentStore', () => {
    let documentList: Ref<Document[]> = ref([]);
    let folderStructure: Ref<Folder[]> = ref([]);
    let documentCount: Ref<number> = ref(0);

    function loadDocuments(callback?: (arg0: void) => void) {
        api.getAllDocuments((response: []) => {
            folderStructure.value = response
            if (callback) callback();
        });
    }
    function loadDocumentList(callback?: (arg0: void) => void) {
        api.getAllDocumentsList((response: []) => {
            documentList.value = response
            if (callback) callback();
        });
    }
    function loadDocumentCount() {
        api.getDocumentCount((response: number) => {documentCount.value = response})
    }

    return {
        documentList,
        folderStructure,
        documentCount,
        loadDocuments,
        loadDocumentList,
        loadDocumentCount
    }
});