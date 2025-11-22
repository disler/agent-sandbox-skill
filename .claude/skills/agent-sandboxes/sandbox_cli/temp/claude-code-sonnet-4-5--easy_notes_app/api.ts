import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export interface Note {
  id: number;
  title: string;
  content: string | null;
  created_at: string;
  updated_at: string;
}

export interface NoteCreate {
  title: string;
  content?: string;
}

export interface NoteUpdate {
  title?: string;
  content?: string;
}

export const fetchNotes = async (): Promise<Note[]> => {
  const response = await api.get<Note[]>('/notes');
  return response.data;
};

export const createNote = async (data: NoteCreate): Promise<Note> => {
  const response = await api.post<Note>('/notes', data);
  return response.data;
};

export const updateNote = async (id: number, data: NoteUpdate): Promise<Note> => {
  const response = await api.put<Note>(`/notes/${id}`, data);
  return response.data;
};

export const deleteNote = async (id: number): Promise<void> => {
  await api.delete(`/notes/${id}`);
};
