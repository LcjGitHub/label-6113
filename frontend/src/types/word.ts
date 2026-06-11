export interface DialectWord {
  id: number
  dialect_word: string
  mandarin: string
  pinyin: string
  region: string
  example: string
  source: string
  remark: string
}

export interface WordForm {
  dialect_word: string
  mandarin: string
  pinyin: string
  region: string
  example: string
  source: string
  remark: string
}

export interface Region {
  region: string
  count: number
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

export interface BatchImportFailedItem {
  index: number
  error: string
}

export interface BatchImportResult {
  success_count: number
  fail_count: number
  failed_items: BatchImportFailedItem[]
}

export interface BatchImportRequest {
  items: WordForm[]
}


