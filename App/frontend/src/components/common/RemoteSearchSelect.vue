<template>
  <div class="remote-search-select">
    <el-select
      v-model="innerValue"
      filterable
      remote
      clearable
      reserve-keyword
      :placeholder="placeholder"
      :disabled="disabled"
      :loading="loading"
      :remote-method="remoteSearch"
      style="width: 100%"
      @change="handleChange"
      @clear="handleClear"
      @focus="handleFocus"
    >
      <el-option
        v-for="item in mergedOptions"
        :key="String(item.value)"
        :label="item.label"
        :value="item.value"
      />
    </el-select>

    <div v-if="$slots.action" class="action-row">
      <slot name="action" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { SelectOption } from '../../types/select'

const props = withDefaults(
  defineProps<{
    modelValue: string | number | null
    placeholder?: string
    disabled?: boolean
    fetchOptions: (keyword: string) => Promise<SelectOption[]>
    extraOptions?: SelectOption[]
  }>(),
  {
    placeholder: 'Please select',
    disabled: false,
    extraOptions: () => [],
  },
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
  (e: 'change', option: SelectOption | null): void
  (e: 'clear'): void
}>()

const innerValue = ref<string | number | null>(props.modelValue)
const options = ref<SelectOption[]>([])
const loading = ref(false)

let timer: number | undefined
let hasLoadedDefault = false

const mergedOptions = computed(() => {
  const map = new Map<string | number, SelectOption>()

  props.extraOptions.forEach((item) => {
    map.set(item.value, item)
  })

  options.value.forEach((item) => {
    map.set(item.value, item)
  })

  return Array.from(map.values())
})

watch(
  () => props.modelValue,
  (value) => {
    innerValue.value = value
  },
)

async function loadOptions(keyword = '') {
  if (props.disabled) return

  loading.value = true

  try {
    options.value = await props.fetchOptions(keyword)
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to load options')
  } finally {
    loading.value = false
  }
}

function remoteSearch(query: string) {
  window.clearTimeout(timer)

  timer = window.setTimeout(() => {
    loadOptions(query)
  }, 300)
}

function handleFocus() {
  if (!hasLoadedDefault && !props.disabled) {
    hasLoadedDefault = true
    loadOptions('')
  }
}

function handleChange(value: string | number | null) {
  if (value === null || value === undefined || value === '') {
    handleClear()
    return
  }

  const selected = mergedOptions.value.find((item) => item.value === value) ?? null

  emit('update:modelValue', value)
  emit('change', selected)
}

function handleClear() {
  innerValue.value = null

  emit('update:modelValue', null)
  emit('change', null)
  emit('clear')
}
</script>

<style scoped>
.remote-search-select {
  width: 100%;
}

.action-row {
  margin-top: 6px;
  display: flex;
  justify-content: flex-start;
}
</style>