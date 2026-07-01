<template>
  <div class="select-material">
    <el-select
      v-model="selectedMaterialId"
      filterable
      remote
      clearable
      reserve-keyword
      placeholder="Search or select material"
      :remote-method="remoteSearch"
      :loading="loading"
      style="width: 100%"
      @change="handleChange"
      @clear="handleClear"
    >
      <el-option
        v-for="item in materialOptions"
        :key="item.id"
        :label="getMaterialLabel(item)"
        :value="item.id"
      />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { searchMaterials, type Material } from '@/api/material'

const props = defineProps<{
  materialId: number | null
  materialName: string
}>()

const emit = defineEmits<{
  (e: 'update:materialId', value: number | null): void
  (e: 'update:materialName', value: string): void
}>()

const selectedMaterialId = ref<number | null>(props.materialId)
const materialOptions = ref<Material[]>([])
const loading = ref(false)

let searchTimer: number | undefined

watch(
  () => props.materialId,
  (newValue) => {
    selectedMaterialId.value = newValue
  },
)

onMounted(() => {
  loadMaterials('')
})

function getMaterialLabel(item: Material) {
  if (item.material_code) {
    return `${item.material_name_cn} / ${item.material_code}`
  }

  return item.material_name_cn
}

function remoteSearch(query: string) {
  window.clearTimeout(searchTimer)

  searchTimer = window.setTimeout(() => {
    loadMaterials(query)
  }, 300)
}

async function loadMaterials(keyword: string) {
  loading.value = true

  try {
    materialOptions.value = await searchMaterials(keyword)
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to load materials')
  } finally {
    loading.value = false
  }
}

function handleChange(value: number | null) {
  if (!value) {
    handleClear()
    return
  }

  const selected = materialOptions.value.find((item) => item.id === value)

  emit('update:materialId', value)
  emit('update:materialName', selected?.material_name_cn ?? '')
}

function handleClear() {
  selectedMaterialId.value = null
  emit('update:materialId', null)
  emit('update:materialName', '')
}
</script>

<style scoped>
.select-material {
  width: 100%;
}
</style>