<template>
  <div id="app">
    <header>
      <h1>Notes App</h1>
      <button @click="showEditor = !showEditor" class="btn-add">
        {{ showEditor ? 'Hide Editor' : 'Add Note' }}
      </button>
    </header>

    <main>
      <div v-if="notesStore.error" class="error-message">
        {{ notesStore.error }}
      </div>

      <div v-if="notesStore.loading" class="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>

      <NoteEditor
        v-if="showEditor"
        :editing-note="editingNote"
        @submit="handleNoteSubmit"
        @cancel="handleCancel"
      />

      <NotesList
        :notes="notesStore.notes"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useNotesStore } from './stores/notes';
import NoteEditor from './components/NoteEditor.vue';
import NotesList from './components/NotesList.vue';
import type { Note } from './services/api';

const notesStore = useNotesStore();
const showEditor = ref(false);
const editingNote = ref<Note | undefined>();

onMounted(() => {
  notesStore.loadNotes();
});

const handleNoteSubmit = async (data: { title: string; content: string }) => {
  if (editingNote.value) {
    await notesStore.editNote(editingNote.value.id, data);
    editingNote.value = undefined;
  } else {
    await notesStore.addNote(data);
  }
  showEditor.value = false;
};

const handleEdit = (note: Note) => {
  editingNote.value = note;
  showEditor.value = true;
};

const handleDelete = async (id: number) => {
  if (confirm('Are you sure you want to delete this note?')) {
    await notesStore.removeNote(id);
  }
};

const handleCancel = () => {
  editingNote.value = undefined;
  showEditor.value = false;
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

header h1 {
  color: #2c3e50;
  font-size: 2rem;
}

.btn-add {
  padding: 0.75rem 1.5rem;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #229954;
}

main {
  position: relative;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: white;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 4px solid white;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  #app {
    padding: 1rem;
  }

  header {
    flex-direction: column;
    gap: 1rem;
  }

  header h1 {
    font-size: 1.5rem;
  }
}
</style>
