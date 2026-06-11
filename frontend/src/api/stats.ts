import axios from 'axios'
import type { RegionStatsResponse } from '@/types/word'

const api = axios.create({
  baseURL: '/api',
})

export async function fetchRegionStats(): Promise<RegionStatsResponse> {
  const { data } = await api.get<RegionStatsResponse>('/stats/region')
  return data
}
