import { useEffect, useRef, useCallback } from 'react'
import { useCanvasStore } from '../store/canvasStore'
import { fetchNodes, updateNode } from '../api/client'
import NodeCard from './NodeCard'
import EdgeLayer from './EdgeLayer'
import CreateNodePanel from './CreateNodePanel'
import './Canvas.css'

const ZOOM_MIN = 0.15
const ZOOM_MAX = 3
const ZOOM_SENSITIVITY = 0.001

export default function Canvas() {
  const { nodes, edges, setNodes, camera, setCamera, setIsCreating, setCreatePosition } = useCanvasStore()
  const containerRef = useRef<HTMLDivElement>(null)
  const isPanning    = useRef(false)
  const panStart     = useRef({ x: 0, y: 0 })
  const cameraRef    = useRef(camera)
  const draggingNode = useRef<string | null>(null)
  const dragOffset   = useRef({ x: 0, y: 0 })

  useEffect(() => { cameraRef.current = camera }, [camera])
  useEffect(() => { fetchNodes().then(setNodes).catch(console.error) }, [setNodes])

  const screenToWorld = useCallback((sx: number, sy: number) => {
    const cam = cameraRef.current
    return { x: (sx - cam.x) / cam.zoom, y: (sy - cam.y) / cam.zoom }
  }, [])

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button !== 0) return
    isPanning.current = true
    panStart.current = { x: e.clientX - cameraRef.current.x, y: e.clientY - cameraRef.current.y }
  }, [])

  const onMouseMove = useCallback((e: React.MouseEvent) => {
    if (draggingNode.current) {
      const worldPos = screenToWorld(e.clientX, e.clientY)
      useCanvasStore.getState().upsertNode({
        ...useCanvasStore.getState().nodes.find((n) => n.id === draggingNode.current)!,
        x: worldPos.x - dragOffset.current.x,
        y: worldPos.y - dragOffset.current.y,
      })
      return
    }
    if (!isPanning.current) return
    setCamera({ ...cameraRef.current, x: e.clientX - panStart.current.x, y: e.clientY - panStart.current.y })
  }, [screenToWorld, setCamera])

  const onMouseUp = useCallback(async () => {
    if (draggingNode.current) {
      const node = useCanvasStore.getState().nodes.find((n) => n.id === draggingNode.current)
      if (node) await updateNode(node.id, { x: node.x, y: node.y }).catch(console.error)
      draggingNode.current = null
    }
    isPanning.current = false
  }, [])

  const onDoubleClick = useCallback((e: React.MouseEvent) => {
    const worldPos = screenToWorld(e.clientX, e.clientY)
    setCreatePosition(worldPos)
    setIsCreating(true)
  }, [screenToWorld, setCreatePosition, setIsCreating])

  const onWheel = useCallback((e: WheelEvent) => {
    e.preventDefault()
    const cam = cameraRef.current
    const newZoom = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, cam.zoom * (1 + -e.deltaY * ZOOM_SENSITIVITY)))
    const rect = containerRef.current!.getBoundingClientRect()
    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top
    setCamera({
      x: mx - (mx - cam.x) * (newZoom / cam.zoom),
      y: my - (my - cam.y) * (newZoom / cam.zoom),
      zoom: newZoom,
    })
  }, [setCamera])

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    el.addEventListener('wheel', onWheel, { passive: false })
    return () => el.removeEventListener('wheel', onWheel)
  }, [onWheel])

  const handleNodeDragStart = useCallback((e: React.MouseEvent, nodeId: string) => {
    isPanning.current = false
    draggingNode.current = nodeId
    const node = useCanvasStore.getState().nodes.find((n) => n.id === nodeId)!
    const worldPos = screenToWorld(e.clientX, e.clientY)
    dragOffset.current = { x: worldPos.x - node.x, y: worldPos.y - node.y }
  }, [screenToWorld])

  const size = containerRef.current?.getBoundingClientRect() ?? { width: window.innerWidth, height: window.innerHeight }

  return (
    <div ref={containerRef} className="canvas" onMouseDown={onMouseDown} onMouseMove={onMouseMove} onMouseUp={onMouseUp} onDoubleClick={onDoubleClick}>
      <svg className="canvas__grid" width="100%" height="100%">
        <defs>
          <pattern id="grid" width={40*camera.zoom} height={40*camera.zoom} x={camera.x%(40*camera.zoom)} y={camera.y%(40*camera.zoom)} patternUnits="userSpaceOnUse">
            <circle cx="0.5" cy="0.5" r="0.5" fill="rgba(0,229,255,0.12)" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
      <EdgeLayer edges={edges} nodes={nodes} camera={camera} width={size.width} height={size.height} />
      <div className="canvas__world" style={{ transform: `translate(${camera.x}px, ${camera.y}px) scale(${camera.zoom})` }}>
        {nodes.map((node) => (
          <NodeCard key={node.id} node={node} screenX={node.x} screenY={node.y} onDragStart={handleNodeDragStart} />
        ))}
      </div>
      <div className="canvas__hud">
        <span>NEURALMAP</span>
        <span className="canvas__hud-zoom">{Math.round(camera.zoom*100)}%</span>
        <span>{nodes.length} nodes</span>
      </div>
      <div className="canvas__hint">double-click to create node</div>
      <CreateNodePanel />
    </div>
  )
}