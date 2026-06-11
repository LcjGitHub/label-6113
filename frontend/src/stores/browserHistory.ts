import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export interface HistoryItem {
  id: number
  dialect_word: string
  visited_at: number
}

const STORAGE_KEY = 'dialect-browser-history'
const MAX_HISTORY = 20

function loadFromStorage(): HistoryItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      return JSON.parse(raw) as HistoryItem[]
    }
  } catch {
    // ignore parse errors
  }
  return []
}

function saveToStorage(items: HistoryItem[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  } catch {
    // ignore storage errors
  }
}

export const useBrowserHistoryStore = defineStore('browserHistory', () => {
  const history = ref<HistoryItem[]>(loadFromStorage())

  watch(
    history,
    (newVal) => {
      saveToStorage(newVal)
    },
    { deep: true }
  )

  function addVisit(id: number, dialect_word: string) {
    const existingIndex = history.value.findIndex((item) => item.id === id)
    if (existingIndex !== -1) {
      history.value.splice(existingIndex, 1)
    }
    history.value.unshift({
      id,
      dialect_word,
      visited_at: Date.now(),
    })
    if (history.value.length > MAX_HISTORY) {
      history.value.splice(MAX_HISTORY)
    }
  }

  function removeHistory(id: number) {
    const index = history.value.findIndex((item) => item.id === id)
    if (index !== -1) {
      history.value.splice(index, 1)
    }
  }

  function clearHistory() {
    history.value = []
  }

  return {
    history,
    addVisit,
    removeHistory,
    clearHistory,
  }
})
