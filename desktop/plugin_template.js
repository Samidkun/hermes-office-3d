import { atom, host, useValue } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'
import { useEffect, useRef, useState } from 'react'

const ID = 'office-3d'
const $bigOpen = atom(false)
let CTX = null
let IFRAME_REF = null

// We inject the HTML content of office_scene.html into this constant at build/install time
// SCENE_HTML_PLACEHOLDER

function OfficeStage({ wide }) {
  const iframeRef = useRef(null)

  useEffect(() => {
    IFRAME_REF = iframeRef.current
    return () => {
      if (IFRAME_REF === iframeRef.current) IFRAME_REF = null
    }
  }, [])

  return jsx('div', {
    className: 'relative h-full w-full overflow-hidden rounded border border-(--ui-border) bg-[#0C0E14]',
    children: jsx('iframe', {
      ref: iframeRef,
      title: 'Hermes Pixel Office',
      srcDoc: SCENE_HTML,
      sandbox: 'allow-scripts',
      className: 'h-full w-full border-0 bg-transparent',
    }),
  })
}

function OfficeHeader({ onOpenBig, bigOpen }) {
  return jsxs('div', {
    className: 'flex items-center justify-between border-b border-(--ui-border) pb-2',
    children: [
      jsxs('div', {
        className: 'flex items-center gap-1.5 font-medium text-(--ui-text-primary)',
        children: [
          jsx('span', { children: '🏢' }),
          jsx('span', { children: 'Agent Office' }),
        ],
      }),
      onOpenBig && !bigOpen
        ? jsx('button', {
            type: 'button',
            className: 'rounded bg-(--ui-bg-hover) px-2 py-0.5 text-[0.6875rem] text-(--ui-text-secondary) hover:text-(--ui-text-primary)',
            onClick: onOpenBig,
            children: 'Buka Lebar ↗',
          })
        : null,
    ].filter(Boolean),
  })
}

function OfficePane() {
  const bigOpen = useValue($bigOpen)

  const openBig = () => {
    if (typeof host.openWorkspace !== 'function') return
    host.openWorkspace('office-3d:view', {
      title: 'Agent Office',
      minWidth: '34rem',
      render: () => jsx(OfficeWorkspace, {}),
      onClose: () => $bigOpen.set(false),
    })
    $bigOpen.set(true)
  }

  return jsxs('div', {
    className: 'flex h-full min-h-0 flex-col gap-2 p-2 text-xs',
    children: [
      jsx(OfficeHeader, { onOpenBig: openBig, bigOpen }),
      jsx(OfficeStage, { wide: false }),
    ],
  })
}

function OfficeWorkspace() {
  return jsxs('div', {
    className: 'flex h-full min-h-0 flex-col gap-2 p-3 text-xs',
    children: [
      jsx(OfficeHeader, { onOpenBig: null, bigOpen: false }),
      jsx(OfficeStage, { wide: true }),
    ],
  })
}

// Forward Hermes Gateway events to office iframe
function setupEventBridge(ctx) {
  ctx.onEvent('*', (event) => {
    if (!IFRAME_REF || !IFRAME_REF.contentWindow) return
    if (!event || !event.type) return

    const t = event.type
    // Map delegate / subagent / tool events to visualizer
    if (t.includes('delegate') || t.includes('subagent') || t.includes('tool')) {
      let state = 'coding'
      let speech = ''
      if (t.includes('thinking')) {
        state = 'thinking'
        speech = 'Analyzing next action...'
      } else if (t.includes('completed') || t.includes('complete')) {
        state = 'done'
        speech = 'Task completed!'
      } else if (t.includes('failed')) {
        state = 'error'
        speech = 'Incident blocker encountered!'
      } else if (t.includes('started') || t.includes('spawned')) {
        state = 'coding'
        speech = event.goal || event.task || 'Starting delegated execution...'
      }

      IFRAME_REF.contentWindow.postMessage({
        type: 'HERMES_EVENT',
        payload: {
          agentId: event.agent_id || event.subagent_id || 'parent',
          role: event.subagent_id ? 'worker' : 'orchestrator',
          state: state,
          speech: speech,
          tool: event.tool || event.tool_name || 'terminal',
          model: event.model || 'ag/gemini-3.8-flash',
        }
      }, '*')
    }
  })
}

export default {
  id: ID,
  name: 'Agent Office',
  description: 'Retro 2.5D Isometric AI Agent Office & Telemetry Simulator.',
  defaultEnabled: true,
  register(ctx) {
    CTX = ctx
    setupEventBridge(ctx)

    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'office',
      data: { placement: 'right', width: '420px' },
      render: () => jsx(OfficePane, {}),
    })
  },
}
