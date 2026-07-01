<template>
  <div class="select-origin-address">
    <el-select
      v-model="selectedOriginId"
      filterable
      remote
      clearable
      reserve-keyword
      placeholder="Search or select origin address"
      :disabled="!supplierId"
      :remote-method="remoteSearch"
      :loading="loading"
      style="width: 100%"
      @change="handleChange"
      @clear="handleClear"
    >
      <el-option
        v-for="item in originOptions"
        :key="item.id"
        :label="getOriginAddressLabel(item)"
        :value="item.id"
      />
    </el-select>

    <div class="action-row">
      <el-button
        type="primary"
        link
        :disabled="!supplierId"
        @click="createDialogVisible = true"
      >
        + New Origin Address
      </el-button>
    </div>

    <CreateOriginAddressDialog
      v-model="createDialogVisible"
      :supplier-id="supplierId"
      :supplier-name="supplierName"
      @created="handleOriginCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import CreateOriginAddressDialog from './CreateOriginAddressDialog.vue'
import {
  searchOriginAddresses,
  getOriginAddressLabel,
  type OriginAddress,
} from '@/api/supplier'

const props = defineProps<{
  originId: number | null
  originAddress: string
  supplierId: string | null
  supplierName: string
}>()

const emit = defineEmits<{
  (e: 'update:originId', value: number | null): void
  (e: 'update:originAddress', value: string): void
}>()

const selectedOriginId = ref<number | null>(props.originId)
const originOptions = ref<OriginAddress[]>([])
const loading = ref(false)
const createDialogVisible = ref(false)

let searchTimer: number | undefined

watch(
  () => props.originId,
  (newValue) => {
    selectedOriginId.value = newValue
  },
)

watch(
  () => props.supplierId,
  async (newSupplierId, oldSupplierId) => {
    if (newSupplierId !== oldSupplierId) {
      handleClear()
      originOptions.value = []

      if (newSupplierId) {
        await loadOriginAddresses('')
      }
    }
  },
)

onMounted(() => {
  if (props.supplierId) {
    loadOriginAddresses('')
  }
})

function remoteSearch(query: string) {
  if (!props.supplierId) return

  window.clearTimeout(searchTimer)

  searchTimer = window.setTimeout(() => {
    loadOriginAddresses(query)
  }, 300)
}

async function loadOriginAddresses(keyword: string) {
  if (!props.supplierId) return

  loading.value = true

  try {
    originOptions.value = await searchOriginAddresses(props.supplierId, keyword)
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to load origin addresses')
  } finally {
    loading.value = false
  }
}

function handleChange(value: number | null) {
  if (!value) {
    handleClear()
    return
  }

  const selected = originOptions.value.find((item) => item.id === value)
  const label = selected ? getOriginAddressLabel(selected) : ''

  emit('update:originId', value)
  emit('update:originAddress', label)
}

function handleClear() {
  selectedOriginId.value = null
  emit('update:originId', null)
  emit('update:originAddress', '')
}

function handleOriginCreated(origin: OriginAddress) {
  if (!originOptions.value.some((item) => item.id === origin.id)) {
    originOptions.value.unshift(origin)
  }

  selectedOriginId.value = origin.id

  emit('update:originId', origin.id)
  emit('update:originAddress', getOriginAddressLabel(origin))
}
</script>

<style scoped>
.select-origin-address {
  width: 100%;
}

.action-row {
  margin-top: 6px;
  display: flex;
  justify-content: flex-start;
}
</style>