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
    let selectedOption: Ref<'Folders'|'List'> = ref('Folders');

    function loadDocuments(callback?: (arg0: void) => void) {
        api.getAllDocuments((response: []) => {
            folderStructure.value = response

            //destructure into list
            let list: Document[] = [];
            for(let i = 0; i<folderStructure.value.length; i++) {
                list.push(...folderStructure.value[i].documents);
            }

            documentList.value = list;

            if (callback) callback();
        });
    }
    function loadDocumentCount() {
        api.getDocumentCount((response: number) => {documentCount.value = response})
    }

    function setSelectedOption(option: string) {
        selectedOption.value = option as 'Folders' | 'List';
    }

    return {
        documentList,
        folderStructure,
        documentCount,
        loadDocuments,
        loadDocumentCount,
        selectedOption,
        setSelectedOption,
    }
});