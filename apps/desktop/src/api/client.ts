import axios from 'axios'
import type { NeuralNode, NeuralEdge } from '../store/canvasStore'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
})

export const createNode = async (data: {
  title: string
  type?: NeuralNode['type']
  content?: string
  tags?: string[]
  x: number
  y: number
}): Promise<NeuralNode> => {
  const res = await api.post('/api/nodes/', data)
  return res.data
}

export const fetchNodes = async (): Promise<NeuralNode[]> => {
  const res = await api.get('/api/nodes/')
  return res.data
}

export const deleteNode = async (id: string): Promise<void> => {
  await api.delete(`/api/nodes/${id}`)
}

export const updateNode = async (
  id: string,
  data: Partial<NeuralNode>
): Promise<NeuralNode> => {
  const res = await api.patch(`/api/nodes/${id}`, data)
  return res.data
}

export const createEdge = async (data: {
  source_id: string
  target_id: string
  label?: string
  weight?: number
}): Promise<NeuralEdge> => {
  const res = await api.post('/api/edges/', data)
  return res.data
}

export const fetchViewport = async (
  x_min: number, y_min: number, x_max: number, y_max: number
): Promise<{ nodes: NeuralNode[]; edges: NeuralEdge[] }> => {
  const res = await api.post('/api/graph/viewport', { x_min, y_min, x_max, y_max, limit: 200 })
  return res.data
}
