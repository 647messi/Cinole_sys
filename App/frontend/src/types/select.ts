export interface SelectOption<T = any> {
  label: string
  value: string | number
  raw: T
}