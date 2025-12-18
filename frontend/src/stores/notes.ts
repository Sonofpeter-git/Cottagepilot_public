import { defineStore } from 'pinia'
import { ref } from 'vue'
import { noteService } from '../services/api'
import type { Note } from '../types'

export const useNoteStore = defineStore('notes', () => {
    const notes = ref<Note[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    const getNotesFromLocalStorage = () => {
        const storedNotes = localStorage.getItem('notes')
        if (storedNotes) {
            notes.value = JSON.parse(storedNotes)
        }
    }
    
    async function fetchNotes() {
        loading.value = true
        error.value = null
        try {
        notes.value = await noteService.getNotes()
        localStorage.setItem('notes', JSON.stringify(notes.value))
        return notes
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to fetch sensors'
        console.error(err)
        } finally {
        loading.value = false
        }
    }

    async function createNoteClass(newNoteClassName: string) {
        loading.value = true
        error.value = null
        try {
        await noteService.createNoteClass(newNoteClassName)
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to create new note class'
        console.error(err)
        } finally {
        loading.value = false
        fetchNotes()
        }
    }

    async function deleteNoteClass(classId: string) {
        loading.value = true
        error.value = null
        localStorage.setItem('notes', JSON.stringify(notes.value))
        try {
        await noteService.deleteNoteClass(classId)
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to delete note class'
        console.error(err)
        } finally {
        loading.value = false
        fetchNotes()
        }
    }


    async function addNote(ClassId: string, NewNote: string) {
        loading.value = true
        error.value = null
        try {
            await noteService.addNote(ClassId, NewNote)
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Failed to add new note'
            console.error(err)
        } finally {
            loading.value = false
            await fetchNotes()
        }
    }


    async function deleteNote(classId: string, noteId: string) {
        loading.value = true
        error.value = null
        localStorage.setItem('notes', JSON.stringify(notes.value))
        try {
        await noteService.deleteNote(classId, noteId)
        } catch (err) {
        error.value = err instanceof Error ? err.message : 'Failed to remove note'
        console.error(err)
        } finally {
        loading.value = false
        noteService.getNotes()
        }
    }

  return {
    notes,
    loading,
    error,
    getNotesFromLocalStorage,
    deleteNoteClass,
    deleteNote,
    addNote,
    fetchNotes,
    createNoteClass
  }
})