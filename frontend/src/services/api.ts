import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export interface EmailMessage {
  id: string
  thread_id: string
  subject: string
  sender: string
  date: string
  size: number
  labels: string[]
  snippet: string
}

export interface SenderStat {
  sender: string
  count: number
  total_size_mb: number
  email_ids: string[]
}

export interface ScanResult {
  emails: EmailMessage[]
  total_count: number
  total_size_mb: number
  analysis: string
  sender_stats: SenderStat[]
}

export interface Stats {
  total_emails: number
  total_size_mb: number
  spam_count: number
  large_emails_count: number
  old_emails_count: number
}

export const login = async () => {
  const response = await axios.get(`${API_BASE}/auth/login`)
  return response.data
}

export const checkAuthStatus = async () => {
  const response = await axios.get(`${API_BASE}/auth/status`)
  return response.data
}

export const logout = async () => {
  const response = await axios.post(`${API_BASE}/auth/logout`)
  return response.data
}

export const scanEmails = async (
  scanType: string,
  maxResults: number = 100,
  daysOld?: number,
  minSizeMb?: number
): Promise<ScanResult> => {
  const response = await axios.post(`${API_BASE}/gmail/scan`, {
    scan_type: scanType,
    max_results: maxResults,
    days_old: daysOld,
    min_size_mb: minSizeMb
  })
  return response.data
}

export const deleteEmails = async (emailIds: string[]) => {
  const response = await axios.post(`${API_BASE}/gmail/delete`, {
    email_ids: emailIds
  })
  return response.data
}

export const getStats = async (): Promise<Stats> => {
  const response = await axios.get(`${API_BASE}/gmail/stats`)
  return response.data
}

export const getUserInfo = async () => {
  const response = await axios.get(`${API_BASE}/gmail/user-info`)
  return response.data
}
