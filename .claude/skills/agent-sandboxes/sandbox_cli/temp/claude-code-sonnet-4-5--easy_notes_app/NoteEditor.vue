<template>
  <div class="note-editor">
    <h2>{{ editingNote ? 'Edit Note' : 'Create Note' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">Title</label>
        <input
          id="title"
          v-model="title"
          type="text"
          placeholder="Enter note title"
          required
        />
      </div>
      <div class="form-group">
        <label for="content">Content</label>
        <textarea
          id="content"
          v-model="content"
          placeholder="Enter note content"
          rows="5"
        ></textarea>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn-primary">
          {{ editingNote ? 'Update' : 'Create' }}
        </button>
        <button type="button" class="btn-secondary" @click="handleCancel">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Note } from '../services/api';

const props = defineProps<{
  editingNote?: Note;
}>();

const emit = defineEmits<{
  (e: 'submit', data: { title: string; content: string }): void;
  (e: 'cancel'): void;
}>();

const title = ref('');
const content = ref('');

watch(
  () => props.editingNote,
  (note) => {
    if (note) {
      title.value = note.title;
      content.value = note.content || '';
    } else {
      title.value = '';
      content.value = '';
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit('submit', { title: title.value, content: content.value });
  if (!props.editingNote) {
    title.value = '';
    content.value = '';
  }
};

const handleCancel = () => {
  title.value = '';
  content.value = '';
  emit('cancel');
};
</script>

<style scoped>
.note-editor {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

input,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}
</style>
