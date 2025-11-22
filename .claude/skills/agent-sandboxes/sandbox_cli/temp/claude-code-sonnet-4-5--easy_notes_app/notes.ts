import { defineStore } from 'pinia';
import { ref } from 'vue';
import * as api from '../services/api';
import type { Note, NoteCreate, NoteUpdate } from '../services/api';

export const useNotesStore = defineStore('notes', () => {
  const notes = ref<Note[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const loadNotes = async () => {
    loading.value = true;
    error.value = null;
    try {
      notes.value = await api.fetchNotes();
    } catch (e) {
      error.value = 'Failed to load notes';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  const addNote = async (noteData: NoteCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newNote = await api.createNote(noteData);
      notes.value.unshift(newNote);
    } catch (e) {
      error.value = 'Failed to create note';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  const editNote = async (id: number, noteData: NoteUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedNote = await api.updateNote(id, noteData);
      const index = notes.value.findIndex(n => n.id === id);
      if (index !== -1) {
        notes.value[index] = updatedNote;
      }
    } catch (e) {
      error.value = 'Failed to update note';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  const removeNote = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      await api.deleteNote(id);
      notes.value = notes.value.filter(n => n.id !== id);
    } catch (e) {
      error.value = 'Failed to delete note';
      console.error(e);
    } finally {
      loading.value = false;
    }
  };

  return {
    notes,
    loading,
    error,
    loadNotes,
    addNote,
    editNote,
    removeNote,
  };
});
