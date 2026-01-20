<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-4xl">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-secondary mb-3">Notes</h1>
        <p class="text-secondary">Write down information to remember later.</p>
      </div>

      <div class="rounded-lg p-6 mb-8 rounded-md bg-popUpBg">
        <!-- Add new class -->
         <h1 class="text-2xl text-secondary mb-4">Create note group</h1>
        <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:gap-4"> 
          <input
            v-model="newClassName"
            type="text"
            placeholder="Enter new class name"
            class="rounded px-3 py-2 w-full sm:w-64 bg-popUpBg2 text-secondary placeholder-secondary/70 focus:outline-none focus:ring-2 focus:ring-secondary"
            @keyup.enter="addClass"
          />
          <button
            @click="addClass"
            class="mt13 sm:mt-0 text-extraNeutral px-4 py-2 rounded bg-secondary border-2 border-secondary hover:bg-transparent hover:text-secondary"
          >
            Add Group
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 rounded-md bg-popUpBg">
        <div
          v-for="(noteclass, index) in noteStore.notes"
          :key="index"
          class="glass-effect rounded-lg p-6"
        >
          <h2 class="text-xl font-semibold text-secondary mb-4">{{ noteclass.noteClassName }}</h2>

          <!-- Notes list -->
          <ul class="mb-4 list-disc list-inside text-secondary space-y-2">
            <li v-for="(noteDict) in noteclass.notes" :key="noteDict.id" class="flex items-center justify-between">
              <span class="border-b-2 border-secondary w-2/3">{{ noteDict.note }}</span>
              <button
                @click="deleteNote(noteclass.id, noteDict.id)"
                class="mt-3 sm:mt-0 ml-3 bg-highlight text-extraNeutral px-1 py-1 rounded border-2 border-highlight hover:bg-transparent hover:text-highlight"
              >
                Remove
              </button>
            </li>
          </ul>

          <!-- Add new note to this class -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:gap-4">
            <input
              v-model="newNote[noteclass.id]"
              type="text"
              placeholder="Enter new note"
              class="rounded px-3 py-2 w-full sm:w-64 bg-popUpBg2 text-secondary placeholder-gray focus:outline-none focus:ring-2 focus:ring-secondary"
              @keyup.enter="addNoteToClass(noteclass.id)"
            />
            <button
              @click="addNoteToClass(noteclass.id)"
              class="mt-3 sm:mt-0 text-extraNeutral px-4 py-2 rounded bg-secondary border-2 border-secondary hover:bg-transparent hover:text-secondary"
            >
              Add Note
            </button>
            <button
              @click="deleteNoteClass(noteclass.id)"
              class="mt-3 sm:mt-0 ml-3 bg-highlight text-extraNeutral px-4 py-2 rounded border-2 border-highlight hover:bg-transparent hover:text-highlight"
            >
              Remove group
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { reactive, ref, onMounted, onUnmounted } from 'vue'
  import { useNoteStore } from '../stores/notes'
  import { Note } from '../types'
  import type { WSMessage} from '../types/websocket';
  import { useAccountStore } from '../stores/account'

  const accountStore = useAccountStore()
  const noteStore = useNoteStore()
  const newNote = reactive<Record<string, string>>({})
  const newClassName = ref<string>('')


  async function addClass() {
    const name = newClassName.value?.trim()
    if (!name) {
      return
    }
    // Add new class with empty notes and newNote input
    await noteStore.createNoteClass(name)
    newClassName.value = ''
  }

  async function addNoteToClass(classId: string) {
    if (!newNote[classId] || newNote[classId].trim() === '') {
      return
    }
    await noteStore.addNote(classId, newNote[classId])

    newNote[classId] = ''
  }

  async function deleteNoteClass(classId: string) {
    noteStore.notes = noteStore.notes.filter((nc: Note) => nc.id !== classId);
    await noteStore.deleteNoteClass(classId)
    newNote[classId] = ''
  }

  async function deleteNote(classId: string, noteId: string) {
    await noteStore.deleteNote(classId, noteId)
  }

  // 1. Separate reactive states for different data streams
  let socket: WebSocket | null = null;

  const handleMessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data) as WSMessage;

      // 2. The Router: TypeScript now provides autocomplete for 'payload' 
      // based on which 'case' you are in!
      switch (data.type) {
          case 'sensor_update':
            break;
              
          case 'task_update':
              break;

          case 'note_update':
              noteStore.fetchNotes();
              break;  

          default:
              console.warn('Unknown message type received');
      }
  };

  const connect = () => {

      socket = new WebSocket(`wss://cloud.cottagepilot.fi/ws/unified/${accountStore.account?.access_to_cottage}/`);
      console.log('WebSocket connected🚀 ' + accountStore.account?.access_to_cottage);
      socket.onmessage = handleMessage;
      socket.onclose = () => {
          setTimeout(connect, 3000); // Reconnect logic
      };
  };

  onMounted(async () => {
    await accountStore.fetchAccount()
    noteStore.getNotesFromLocalStorage()
    noteStore.fetchNotes()
    console.log(noteStore.notes)
    connect()
  })

  onUnmounted(() => {
    if (socket) {
        socket.close();
    }
  })
</script>

<style scoped>
/* Remove old container font style */
</style>
