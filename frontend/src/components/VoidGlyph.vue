<template>
  <div
    class="inline-flex items-center justify-center relative select-none pointer-events-none align-middle"
    :style="{ width: `${size}px`, height: `${size}px` }"
  >
    <canvas
      ref="canvasRef"
      :width="renderDim"
      :height="renderDim"
      :style="{ width: `${size}px`, height: `${size}px` }"
      class="block"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  shape: {
    type: String,
    default: 'cluster', // 'cluster' | 'pix-dre' | 'shield' | 'nvme' | 'daw' | 'globe' | 'positive' | 'scanner'
  },
  size: {
    type: [Number, String],
    default: 20,
  },
  color: {
    type: String,
    default: '#00fff5',
  },
})

const canvasRef = ref(null)
const renderDim = 96 // Internal resolution for crisp rendering
let animId = null
let angle = 0

onMounted(() => {
  const canvas = canvasRef.current
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const d = renderDim
  const cx = d / 2
  const cy = d / 2

  const draw = () => {
    angle += 0.03
    ctx.clearRect(0, 0, d, d)

    const baseColor = props.color || '#00fff5'

    ctx.save()
    ctx.translate(cx, cy)

    if (props.shape === 'cluster') {
      // 3 Blades horizontais + nós piscantes
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2.5
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      // Blade superior
      ctx.strokeRect(-28, -26, 56, 12)
      // Blade médio
      ctx.strokeRect(-28, -6, 56, 12)
      // Blade inferior
      ctx.strokeRect(-28, 14, 56, 12)

      // Barramento vertical giratório
      const busX = Math.sin(angle * 2) * 20
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(busX - 2, -26, 4, 52)

      // LEDs
      ctx.fillStyle = baseColor
      for (let i = -20; i <= 20; i += 10) {
        ctx.beginPath()
        ctx.arc(i, -20, 2, 0, Math.PI * 2)
        ctx.arc(i, 0, 2, 0, Math.PI * 2)
        ctx.arc(i, 20, 2, 0, Math.PI * 2)
        ctx.fill()
      }
    } else if (props.shape === 'pix-dre') {
      // Marcador QR Code PIX + Barras verticais DRE
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2.5
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      // QR Finder pattern
      ctx.strokeRect(-32, -32, 28, 28)
      ctx.fillStyle = baseColor
      ctx.fillRect(-24, -24, 12, 12)

      // Barras DRE crescendo dinamicamente
      const barHeights = [
        16 + Math.sin(angle) * 8,
        28 + Math.cos(angle * 1.2) * 10,
        42 + Math.sin(angle * 1.5) * 12,
        54 + Math.cos(angle * 0.8) * 14,
      ]

      ctx.fillStyle = baseColor
      barHeights.forEach((h, idx) => {
        const bx = 4 + idx * 8
        const by = 28 - h
        ctx.fillRect(bx, by, 6, h)
      })

      // Linha de base contábil
      ctx.beginPath()
      ctx.moveTo(-32, 30)
      ctx.lineTo(32, 30)
      ctx.stroke()
    } else if (props.shape === 'shield') {
      // Escudo Zero-Trust + Fechadura central
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 3
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 10

      ctx.beginPath()
      ctx.moveTo(0, -32)
      ctx.lineTo(26, -18)
      ctx.lineTo(26, 6)
      ctx.quadraticCurveTo(24, 28, 0, 36)
      ctx.quadraticCurveTo(-24, 28, -26, 6)
      ctx.lineTo(-26, -18)
      ctx.closePath()
      ctx.stroke()

      // Arco giratório interno de autenticação
      ctx.rotate(angle)
      ctx.beginPath()
      ctx.arc(0, 0, 12, 0, Math.PI * 1.4)
      ctx.stroke()

      // Centro
      ctx.fillStyle = '#ffffff'
      ctx.beginPath()
      ctx.arc(0, 0, 4, 0, Math.PI * 2)
      ctx.fill()
    } else if (props.shape === 'nvme') {
      // PCB SSD NVMe + Blocos de cache orbitando
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2.5
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      // Placa PCB
      ctx.strokeRect(-30, -18, 60, 36)

      // Chanfro M.2 à esquerda
      ctx.fillStyle = '#ffffff'
      ctx.fillRect(-32, -8, 4, 16)

      // Chip processador central
      ctx.fillStyle = baseColor
      ctx.fillRect(-10, -10, 20, 20)

      // Blocos de cache ejetados radialmente
      for (let i = 0; i < 4; i++) {
        const rad = angle + (i * Math.PI) / 2
        const ox = Math.cos(rad) * 26
        const oy = Math.sin(rad) * 26
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(ox - 3, oy - 3, 6, 6)
      }
    } else if (props.shape === 'daw') {
      // Mesa de Som / Equalizador FFT + Faders
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2.5
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      // 4 Faders verticais
      ;[-22, -8, 8, 22].forEach((fx, i) => {
        ctx.beginPath()
        ctx.moveTo(fx, -28)
        ctx.lineTo(fx, 28)
        ctx.stroke()

        // Cursor do fader oscilando
        const fy = Math.sin(angle * 2 + i * 1.5) * 18
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(fx - 5, fy - 4, 10, 8)
      })

      // Arco FFT de espectro no topo
      ctx.beginPath()
      for (let x = -30; x <= 30; x += 4) {
        const sy = -32 + Math.sin((x + angle * 20) * 0.2) * 5
        if (x === -30) ctx.moveTo(x, sy)
        else ctx.lineTo(x, sy)
      }
      ctx.stroke()
    } else if (props.shape === 'globe') {
      // Esfera de rede global com nós em órbita
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      // Círculo base
      ctx.beginPath()
      ctx.arc(0, 0, 30, 0, Math.PI * 2)
      ctx.stroke()

      // Elipse equatorial girando
      ctx.save()
      ctx.rotate(angle)
      ctx.beginPath()
      ctx.ellipse(0, 0, 30, 10, 0, 0, Math.PI * 2)
      ctx.stroke()

      // Nós satélite
      ctx.fillStyle = '#ffffff'
      ctx.beginPath()
      ctx.arc(30, 0, 3.5, 0, Math.PI * 2)
      ctx.arc(-30, 0, 3.5, 0, Math.PI * 2)
      ctx.fill()
      ctx.restore()
    } else if (props.shape === 'positive') {
      // Matriz orgânica viva em pulso
      const scale = 1 + Math.sin(angle * 2) * 0.15
      ctx.scale(scale, scale)
      ctx.strokeStyle = '#10b981'
      ctx.lineWidth = 2.5
      ctx.shadowColor = '#10b981'
      ctx.shadowBlur = 10

      // Losango exterior
      ctx.beginPath()
      ctx.moveTo(0, -30)
      ctx.lineTo(30, 0)
      ctx.lineTo(0, 30)
      ctx.lineTo(-30, 0)
      ctx.closePath()
      ctx.stroke()

      // Centro em folha / pulso
      ctx.fillStyle = '#39ff14'
      ctx.beginPath()
      ctx.arc(0, 0, 8, 0, Math.PI * 2)
      ctx.fill()
    } else {
      // 'scanner': Radar cibernético de varredura
      ctx.strokeStyle = baseColor
      ctx.lineWidth = 2
      ctx.shadowColor = baseColor
      ctx.shadowBlur = 8

      ctx.beginPath()
      ctx.arc(0, 0, 32, 0, Math.PI * 2)
      ctx.stroke()

      ctx.beginPath()
      ctx.arc(0, 0, 18, 0, Math.PI * 2)
      ctx.stroke()

      // Linha de radar rotativa
      const rx = Math.cos(angle * 2) * 32
      const ry = Math.sin(angle * 2) * 32
      ctx.beginPath()
      ctx.moveTo(0, 0)
      ctx.lineTo(rx, ry)
      ctx.stroke()

      ctx.fillStyle = '#ffffff'
      ctx.beginPath()
      ctx.arc(0, 0, 4, 0, Math.PI * 2)
      ctx.fill()
    }

    ctx.restore()
    animId = requestAnimationFrame(draw)
  }

  draw()
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
})
</script>
