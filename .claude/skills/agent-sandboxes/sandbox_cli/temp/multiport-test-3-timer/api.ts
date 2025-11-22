import axios from 'axios'

// Use the public backend URL for external access
const API_BASE = window.location.hostname.includes('e2b.app')
  ? `https://8000-${window.location.hostname.split('-').slice(1).join('-')}`
  : 'http://localhost:8000'

export interface TimerPreset {
  id: number
  name: string
  hours: number
  minutes: number
  seconds: number
  created_at: string
}

export interface TimerHistory {
  id: number
  preset_id: number | null
  duration_seconds: number
  completed_at: string
}

export const api = {
  async getPresets(): Promise<TimerPreset[]> {
    const response = await axios.get(`${API_BASE}/api/presets`)
    return response.data
  },

  async createPreset(preset: Omit<TimerPreset, 'id' | 'created_at'>): Promise<TimerPreset> {
    const response = await axios.post(`${API_BASE}/api/presets`, preset)
    return response.data
  },

  async deletePreset(id: number): Promise<void> {
    await axios.delete(`${API_BASE}/api/presets/${id}`)
  },

  async getHistory(): Promise<TimerHistory[]> {
    const response = await axios.get(`${API_BASE}/api/history`)
    return response.data
  },

  async createHistory(history: Omit<TimerHistory, 'id' | 'completed_at'>): Promise<TimerHistory> {
    const response = await axios.post(`${API_BASE}/api/history`, history)
    return response.data
  }
}
