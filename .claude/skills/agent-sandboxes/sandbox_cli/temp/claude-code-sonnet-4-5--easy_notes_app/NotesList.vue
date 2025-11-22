<template>
  <div class="notes-list">
    <div v-if="notes.length === 0" class="empty-state">
      <p>No notes yet. Create your first note!</p>
    </div>
    <div v-else class="notes-grid">
      <div v-for="note in notes" :key="note.id" class="note-card">
        <h3>{{ note.title }}</h3>
        <p class="note-content">
          {{ note.content ? truncate(note.content, 100) : 'No content' }}
        </p>
        <div class="note-meta">
          <span class="note-date">{{ formatDate(note.updated_at) }}</span>
        </div>
        <div class="note-actions">
          <button @click="$emit('edit', note)" class="btn-edit">Edit</button>
          <button @click="$emit('delete', note.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Note } from '../services/api';

defineProps<{
  notes: Note[];
}>();

defineEmits<{
  (e: 'edit', note: Note): void;
  (e: 'delete', id: number): void;
}>();

const truncate = (text: string, length: number) => {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>

<style scoped>
.notes-list {
  margin-top: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.note-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.note-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

h3 {
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 1.25rem;
}

.note-content {
  color: #555;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.note-meta {
  margin-bottom: 1rem;
}

.note-date {
  color: #95a5a6;
  font-size: 0.875rem;
}

.note-actions {
  display: flex;
  gap: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-edit {
  background-color: #3498db;
  color: white;
}

.btn-edit:hover {
  background-color: #2980b9;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background-color: #c0392b;
}
</style>
