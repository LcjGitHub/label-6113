import axios from 'axios'
import type { BatchDeleteResult, DialectWord, Region, WordForm } from '@/types/word'

const api = axios.create({
  baseURL: '/api',
})

export async function fetchWords(region?: string, keyword?: string): Promise<DialectWord[]> {
  const params: Record<string, string> = {}
  if (region) params.region = region
  if (keyword) params.keyword = keyword
  const { data } = await api.get<DialectWord[]>('/words', { params })
  return data
}

export async function fetchWord(id: number): Promise<DialectWord> {
  const { data } = await api.get<DialectWord>(`/words/${id}`)
  return data
}

export async function createWord(form: WordForm): Promise<DialectWord> {
  const { data } = await api.post<DialectWord>('/words', form)
  return data
}

export async function updateWord(id: number, form: WordForm): Promise<DialectWord> {
  const { data } = await api.put<DialectWord>(`/words/${id}`, form)
  return data
}

export async function deleteWord(id: number): Promise<void> {
  await api.delete(`/words/${id}`)
}

export async function batchDeleteWords(ids: number[]): Promise<BatchDeleteResult> {
  const { data } = await api.post<BatchDeleteResult>('/words/batch-delete', { ids })
  return data
}

export async function fetchRandomWord(region?: string): Promise<DialectWord> {
  const params: Record<string, string> = {}
  if (region) params.region = region
  const { data } = await api.get<DialectWord>('/words/random', { params })
  return data
}

export async function exportWords(region?: string, keyword?: string): Promise<void> {
  const params: Record<string, string> = {}
  if (region) params.region = region
  if (keyword) params.keyword = keyword
  const { data } = await api.get('/words/export', {
    params,
    responseType: 'blob',
  })
  const url = URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  link.href = url
  link.download = 'dialect_words.csv'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export async function fetchRegions(): Promise<Region[]> {
  const { data } = await api.get<Region[]>('/regions')
  return data
}
