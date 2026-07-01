import type { SelectOption } from '@/types/select'

import {
  searchSuppliers,
  searchOriginAddresses,
  getOriginAddressLabel,
  type Supplier,
  type OriginAddress,
} from './supplier'

import {
  searchMaterials,
  type Material,
} from './material'

export async function fetchSupplierOptions(
  keyword: string,
): Promise<SelectOption<Supplier>[]> {
  const list = await searchSuppliers(keyword)

  return list.map((item) => ({
    label: item.supplier_name_en
      ? `${item.supplier_name_cn} / ${item.supplier_name_en}`
      : item.supplier_name_cn,
    value: item.supplier_id,
    raw: item,
  }))
}

export async function fetchMaterialOptions(
  keyword: string,
): Promise<SelectOption<Material>[]> {
  const list = await searchMaterials(keyword)

  return list.map((item) => ({
    label: item.material_code
      ? `${item.material_name_cn} / ${item.material_code}`
      : item.material_name_cn,
    value: item.id,
    raw: item,
  }))
}

export async function fetchOriginAddressOptions(
  supplierId: string,
  keyword: string,
): Promise<SelectOption<OriginAddress>[]> {
  const list = await searchOriginAddresses(supplierId, keyword)

  return list.map((item) => ({
    label: getOriginAddressLabel(item),
    value: item.id,
    raw: item,
  }))
}