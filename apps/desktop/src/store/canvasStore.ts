import { create } from 'zustand'

export interface NeuralNode {
  id: string
  title: string
  type: 'note' | 'code' | 'image' | 'file' | 'journal' | 'url'
  content?: string
  tags: string[]
  x: number
  y: number
  asset_key?: string
  created_at: string
  updated_at: string
}

export interface NeuralEdge {
  id: string
  source_id: string
  target_id: string
  label?: string
  weight: number
  kind: 'manual' | 'ai_suggested' | 'approved'
  created_at: string
}

export interface Camera {
  x: number
  y: number
  zoom: number
}

interface CanvasStore {
  nodes: NeuralNode[]
  edges: NeuralEdge[]
  setNodes: (nodes: NeuralNode[]) => void
  setEdges: (edges: NeuralEdge[]) => void
  upsertNode: (node: NeuralNode) => void
  camera: Camera
  setCamera: (camera: Camera) => void
  selectedNodeId: string | null
  setSelectedNodeId: (id: string | null) => void
  isCreating: boolean
  setIsCreating: (v: boolean) => void
  createPosition: { x: number; y: number }
  setCreatePosition: (pos: { x: number; y: number }) => void
}

export const useCanvasStore = create<CanvasStore>((set) => ({
  nodes: [],
  edges: [],
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges }),
  upsertNode: (node) =>
    set((state) => ({
      nodes: state.nodes.find((n) => n.id === node.id)
        ? state.nodes.map((n) => (n.id === node.id ? node : n))
        : [...state.nodes, node],
    })),
  camera: { x: 0, y: 0, zoom: 1 },
  setCamera: (camera) => set({ camera }),
  selectedNodeId: null,
  setSelectedNodeId: (id) => set({ selectedNodeId: id }),
  isCreating: false,
  setIsCreating: (v) => set({ isCreating: v }),
  createPosition: { x: 0, y: 0 },
  setCreatePosition: (pos) => set({ createPosition: pos }),
}))
