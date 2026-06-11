export interface DialectWord {
  id: number
  dialect_word: string
  mandarin: string
  region: string
  example: string
  source: string
  remark: string
}

export interface WordForm {
  dialect_word: string
  mandarin: string
  region: string
  example: string
  source: string
  remark: string
}

export interface WordQueryParams {
  region?: string
  keyword?: string
}

export interface RegionStat {
  region: string
  count: number
}

export interface RegionStatsResponse {
  total: number
  regions: RegionStat[]
}

export interface BatchDeleteResult {
  deleted_count: number
}
