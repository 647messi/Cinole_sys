import { http, unwrap } from './http'
import { API_PREFIX } from './config'

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

export async function createGoodsReceipt(
  payload: CreateGoodsReceiptPayload,
): Promise<CreateGoodsReceiptResult> {
  const res = await http.post(
    // `${API_PREFIX.transaction}/goods-receipts`,
    `${API_PREFIX.transaction}/goods-receipts`,
    payload,
  )

  return unwrap<CreateGoodsReceiptResult>(res)
}