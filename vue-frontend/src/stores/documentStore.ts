// import { defineStore } from 'pinia';

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