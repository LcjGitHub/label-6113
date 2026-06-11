import axios from 'axios'
import type { BatchDeleteResult, DialectWord, WordForm, WordQueryParams } from '@/types/word'

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

export async function searchWords(params: WordQueryParams): Promise<DialectWord[]> {
  const { data } = await api.get<DialectWord[]>('/words/search', { params })
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

export async function fetchRandomWord(): Promise<DialectWord> {
  const { data } = await api.get<DialectWord>('/words/random')
  return data
}

export async function fetchRegions(): Promise<string[]> {
  const { data } = await api.get<string[]>('/regions')
  return data
}
