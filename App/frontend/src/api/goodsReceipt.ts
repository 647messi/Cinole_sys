import axios from 'axios'
import { API_PREFIX } from './config'

const http = axios.create({
  baseURL: '',
  timeout: 15000,
})

export interface CreateGoodsReceiptPayload {
  receipt_time: string

  supplier_id: string
  supplier_name: string

  origin_address_id: number
  origin_address: string

  material_id: number
  material_name_cn: string
}

export interface CreateGoodsReceiptResult {
  id?: number
  receipt_id: string
  receipt_time: string

  supplier_id: string
  supplier_name: string

  origin_address_id: number
  origin_address: string

  material_id: number
  material_name_cn: string
}

function unwrap<T>(res: any): T {
  return res?.data?.data ?? res?.data ?? res
}

export async function createGoodsReceipt(
  payload: CreateGoodsReceiptPayload,
): Promise<CreateGoodsReceiptResult> {
  const res = await http.post(`${API_PREFIX.master}/goods-receipts`, payload)
  return unwrap<CreateGoodsReceiptResult>(res)
}