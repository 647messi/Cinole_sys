import axios from 'axios'

export const http = axios.create({
  baseURL: '',
  timeout: 15000,
})

export function unwrap<T>(res: any): T {
  return res?.data?.data ?? res?.data ?? res
}