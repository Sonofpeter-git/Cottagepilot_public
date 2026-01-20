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

        // Find noteclass
        const noteClass = notes.value.find(n => n.id === classId)
        if (!noteClass) return

        // Backup for rollback
        const originalNotes = JSON.parse(JSON.stringify(notes.value))

        try {
            // Check if it's actually an Array or an Object at runtime
            if (Array.isArray(noteClass.notes)) {
            // 1. Handle as Array
            noteClass.notes = noteClass.notes.filter((n: any) => n.id !== noteId)
            } else if (noteClass.notes && typeof noteClass.notes === 'object') {
            // 2. Handle as Dictionary
            delete (noteClass.notes as any)[noteId]
            }

            // Call API to delete note
            await noteService.deleteNote(classId, noteId)
        } catch (err) {
            //Rollback if server fails
            notes.value = originalNotes
            error.value = err instanceof Error ? err.message : 'Failed to remove note'
        } finally {
            loading.value = false
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