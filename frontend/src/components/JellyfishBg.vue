<template>
  <canvas ref="canvasRef" class="fixed inset-0 w-full h-full pointer-events-none z-0" style="opacity: 0.12;"></canvas>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const canvasRef = ref(null)
let animId = null

class Tendril {
  constructor(canvas) {
    this.canvas = canvas
    this.reset()
  }

  reset() {
    this.x = Math.random() * this.canvas.width
    this.y = this.canvas.height + Math.random() * 100
    this.baseX = this.x
    this.size = 2 + Math.random() * 4
    this.speedY = 0.15 + Math.random() * 0.25
    this.wobbleAmp = 20 + Math.random() * 40
    this.wobbleFreq = 0.008 + Math.random() * 0.008
    this.phase = Math.random() * Math.PI * 2
    this.opacity = 0.2 + Math.random() * 0.5
    this.pulseSpeed = 0.01 + Math.random() * 0.015
    this.pulsePhase = Math.random() * Math.PI * 2
    this.life = 0
    this.maxLife = 400 + Math.random() * 600
    // Tentacles
    this.tentacles = []
    const numTentacles = 3 + Math.floor(Math.random() * 4)
    for (let i = 0; i < numTentacles; i++) {
      this.tentacles.push({
        angle: (Math.PI / (numTentacles - 1)) * i + Math.PI * 0.5,
        length: 8 + Math.random() * 20,
        wobble: Math.random() * 0.02,
        phase: Math.random() * Math.PI * 2
      })
    }
  }

  update() {
    this.life++
    this.y -= this.speedY
    this.x = this.baseX + Math.sin(this.life * this.wobbleFreq + this.phase) * this.wobbleAmp
    this.pulsePhase += this.pulseSpeed

    if (this.y < -50 || this.life > this.maxLife) {
      this.reset()
    }
  }

  draw(ctx) {
    const pulse = 0.5 + 0.5 * Math.sin(this.pulsePhase)
    const fadeIn = Math.min(this.life / 60, 1)
    const fadeOut = Math.min((this.maxLife - this.life) / 80, 1)
    const alpha = this.opacity * pulse * fadeIn * fadeOut

    // Bell (dome)
    ctx.save()
    ctx.globalAlpha = alpha
    ctx.beginPath()
    const bellW = this.size * 4
    const bellH = this.size * 3
    ctx.ellipse(this.x, this.y, bellW, bellH, 0, Math.PI, 0)
    ctx.fillStyle = `rgba(212, 175, 55, ${0.3 * pulse})`
    ctx.fill()
    ctx.strokeStyle = `rgba(212, 175, 55, ${0.6})`
    ctx.lineWidth = 0.8
    ctx.stroke()

    // Inner glow
    const grd = ctx.createRadialGradient(this.x, this.y - bellH * 0.3, 0, this.x, this.y, bellW)
    grd.addColorStop(0, `rgba(255, 215, 80, ${0.25 * pulse})`)
    grd.addColorStop(1, 'rgba(212, 175, 55, 0)')
    ctx.fillStyle = grd
    ctx.beginPath()
    ctx.ellipse(this.x, this.y, bellW, bellH, 0, Math.PI, 0)
    ctx.fill()

    // Tentacles
    for (const t of this.tentacles) {
      const wobble = Math.sin(this.life * t.wobble + t.phase) * 8
      const tx = this.x + Math.cos(t.angle) * t.length + wobble
      const ty = this.y + Math.sin(t.angle) * t.length + Math.abs(wobble) * 0.5
      
      ctx.beginPath()
      ctx.moveTo(this.x + Math.cos(t.angle) * bellW * 0.5, this.y)
      ctx.quadraticCurveTo(
        this.x + Math.cos(t.angle) * t.length * 0.5 + wobble * 0.5,
        this.y + t.length * 0.5,
        tx, ty
      )
      ctx.strokeStyle = `rgba(212, 175, 55, ${0.4 * alpha})`
      ctx.lineWidth = 0.6
      ctx.stroke()
    }

    ctx.restore()
  }
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  resize()
  window.addEventListener('resize', resize)

  // Create tendrils (jellyfish)
  const tendrils = []
  const count = Math.max(6, Math.floor(window.innerWidth / 200))
  for (let i = 0; i < count; i++) {
    const t = new Tendril(canvas)
    t.y = Math.random() * canvas.height // Start at random positions
    t.life = Math.random() * 200
    tendrils.push(t)
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (const t of tendrils) {
      t.update()
      t.draw(ctx)
    }
    animId = requestAnimationFrame(animate)
  }
  animate()
})

onBeforeUnmount(() => {
  if (animId) cancelAnimationFrame(animId)
})
</script>
