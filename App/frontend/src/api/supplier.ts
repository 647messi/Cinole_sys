import { http, unwrap } from './http'
import { API_PREFIX } from './config'

export interface Supplier {
  supplier_id: string
  supplier_name_cn: string
  supplier_name_en?: string | null
  supplier_short_code?: string | null
  supplier_type_code?: string | null
  contact_name?: string | null
  phone?: string | null
  email?: string | null
  is_active?: boolean
  remark?: string | null
  created_at?: string
  updated_at?: string
}

export interface OriginAddress {
  id: number
  supplier_id: string

  country?: string | null
  province?: string | null
  city?: string | null
  district?: string | null
  postal_code?: string | null
  detailed_address?: string | null

  full_address?: string | null
  origin_address?: string | null

  is_default?: boolean
  is_active?: boolean
  remark?: string | null
  created_at?: string
  updated_at?: string
}

export interface CreateSupplierPayload {
  supplier: {
    supplier_name_cn: string
    supplier_name_en?: string | null
    supplier_short_code?: string | null
    supplier_type_code?: string | null
    contact_name?: string | null
    phone?: string | null
    email?: string | null
    is_active: boolean
    remark?: string | null
  }
  origin_address: {
    country?: string | null
    province?: string | null
    city?: string | null
    district?: string | null
    postal_code?: string | null
    detailed_address?: string | null
    full_address: string
    is_default: boolean
    is_active: boolean
    remark?: string | null
  }
}

export interface CreateSupplierResult {
  supplier: Supplier
  origin_address: OriginAddress
}

export interface CreateOriginAddressPayload {
  country?: string | null
  province?: string | null
  city?: string | null
  district?: string | null
  postal_code?: string | null
  detailed_address?: string | null
  full_address: string
  is_default: boolean
  is_active: boolean
  remark?: string | null
}

export async function searchSuppliers(keyword = ''): Promise<Supplier[]> {
  const res = await http.get(`${API_PREFIX.master}/suppliers`, {
    params: {
      keyword,
      is_active: true,
    },
  })

  return unwrap<Supplier[]>(res)
}

export async function getSupplierById(supplierId: string): Promise<Supplier> {
  const res = await http.get(`${API_PREFIX.master}/suppliers/${supplierId}`)
  return unwrap<Supplier>(res)
}

export async function createSupplierWithOrigin(
  payload: CreateSupplierPayload,
): Promise<CreateSupplierResult> {
  const res = await http.post(`${API_PREFIX.master}/suppliers`, payload)
  return unwrap<CreateSupplierResult>(res)
}

export async function searchOriginAddresses(
  supplierId: string,
  keyword = '',
): Promise<OriginAddress[]> {
  const res = await http.get(
    `${API_PREFIX.master}/suppliers/${supplierId}/origin-addresses`,
    {
      params: {
        keyword,
        is_active: true,
      },
    },
  )

  return unwrap<OriginAddress[]>(res)
}

export async function createOriginAddress(
  supplierId: string,
  payload: CreateOriginAddressPayload,
): Promise<OriginAddress> {
  const res = await http.post(
    `${API_PREFIX.master}/suppliers/${supplierId}/origin-addresses`,
    payload,
  )

  return unwrap<OriginAddress>(res)
}

export function buildFullAddress(address: {
  country?: string | null
  province?: string | null
  city?: string | null
  district?: string | null
  detailed_address?: string | null
  postal_code?: string | null
}) {
  return [
    address.country,
    address.province,
    address.city,
    address.district,
    address.detailed_address,
    address.postal_code,
  ]
    .map((item) => String(item ?? '').trim())
    .filter(Boolean)
    .join(' ')
}

export function getOriginAddressLabel(origin: OriginAddress) {
  return (
    origin.full_address ||
    origin.origin_address ||
    buildFullAddress(origin) ||
    ''
  )
}