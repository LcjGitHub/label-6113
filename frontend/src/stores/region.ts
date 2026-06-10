import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRegionStore = defineStore('region', () => {
  const selectedRegion = ref('')

  function setRegion(region: string) {
    selectedRegion.value = region
  }

  function clearRegion() {
    selectedRegion.value = ''
  }

  return {
    selectedRegion,
    setRegion,
    clearRegion,
  }
})
