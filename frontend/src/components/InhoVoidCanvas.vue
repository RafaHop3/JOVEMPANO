<template>
  <div
    ref="mountRef"
    aria-hidden="true"
    class="relative w-full h-full select-none pointer-events-auto overflow-hidden"
  ></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const props = defineProps({
  accentColor: { type: String, default: '#00fff5' },
  secondaryColor: { type: String, default: '#3b82f6' },
  particleCount: { type: Number, default: 4500 },
})

const mountRef = ref(null)

const VERTEX_SHADER = `
  uniform float uTime;
  uniform vec2 uPointer;
  attribute float aRandomSeed;
  varying vec3 vColor;
  varying float vDistToPointer;

  void main() {
    vec3 pos = position;
    float seed = aRandomSeed * 6.2831853;
    float wave = sin(uTime * 1.5 + seed) * 0.04;
    pos += normal * wave;

    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    vec2 screenPos = gl_Position.xy / gl_Position.w;
    vDistToPointer = length(screenPos - uPointer);

    float sizePulse = 1.0 + sin(uTime * 2.0 + seed * 3.0) * 0.35;
    float pointerAttract = smoothstep(0.9, 0.0, vDistToPointer) * 1.6;
    gl_PointSize = (3.2 * sizePulse + pointerAttract * 2.5) * (180.0 / -mvPosition.z);
    gl_PointSize = clamp(gl_PointSize, 1.0, 16.0);
  }
`

const FRAGMENT_SHADER = `
  uniform vec3 uPrimaryColor;
  uniform vec3 uSecondaryColor;
  varying float vDistToPointer;

  void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    if (dist > 0.5) discard;

    float coreGlow = smoothstep(0.5, 0.0, dist);
    vec3 baseColor = mix(uPrimaryColor, uSecondaryColor, gl_PointCoord.y);

    float cursorHighlight = smoothstep(0.85, 0.0, vDistToPointer);
    vec3 finalColor = mix(baseColor, vec3(0.95, 0.99, 1.0), cursorHighlight * 0.6);

    float alpha = coreGlow * (0.75 + cursorHighlight * 0.25);
    gl_FragColor = vec4(finalColor, alpha);
  }
`

function buildInhoPixDrePositions(count) {
  const geos = []

  const addQrFinderPattern = (cx, cy) => {
    const size = 0.76
    const thickness = 0.12
    const depth = 0.16

    const top = new THREE.BoxGeometry(size, thickness, depth)
    top.translate(cx, cy + size / 2 - thickness / 2, 0)
    const bottom = new THREE.BoxGeometry(size, thickness, depth)
    bottom.translate(cx, cy - size / 2 + thickness / 2, 0)
    const left = new THREE.BoxGeometry(thickness, size, depth)
    left.translate(cx - size / 2 + thickness / 2, cy, 0)
    const right = new THREE.BoxGeometry(thickness, size, depth)
    right.translate(cx + size / 2 - thickness / 2, cy, 0)
    const center = new THREE.BoxGeometry(0.3, 0.3, depth * 1.2)
    center.translate(cx, cy, 0)

    geos.push(top, bottom, left, right, center)
  }

  // 3 Finders do QR Code
  addQrFinderPattern(-1.3, 0.75)
  addQrFinderPattern(1.3, 0.75)
  addQrFinderPattern(-1.3, -0.75)

  // 4 Barras verticais DRE
  const barHeights = [0.9, 1.5, 2.1, 2.7]
  barHeights.forEach((h, i) => {
    const x = -0.2 + i * 0.45
    const bar = new THREE.BoxGeometry(0.24, h, 0.3)
    bar.translate(x, -0.85 + h / 2, 0)
    geos.push(bar)
  })

  // Superfície de amostragem
  const positions = new Float32Array(count * 3)
  for (let i = 0; i < count; i++) {
    const geo = geos[Math.floor(Math.random() * geos.length)]
    const posAttr = geo.getAttribute('position')
    const idx = Math.floor(Math.random() * posAttr.count)
    positions[i * 3] = posAttr.getX(idx) + (Math.random() - 0.5) * 0.05
    positions[i * 3 + 1] = posAttr.getY(idx) + (Math.random() - 0.5) * 0.05
    positions[i * 3 + 2] = posAttr.getZ(idx) + (Math.random() - 0.5) * 0.05
  }

  geos.forEach((g) => g.dispose())
  return positions
}

let renderer = null
let frameId = 0
let cleanups = []

onMounted(() => {
  const container = mountRef.value
  if (!container) return

  try {
    renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true, powerPreference: 'high-performance' })
  } catch (e) {
    return
  }

  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / Math.max(container.clientHeight, 1),
    0.1,
    100
  )
  camera.position.set(0, 0.2, 4.4)

  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))
  renderer.setSize(container.clientWidth, container.clientHeight)
  container.innerHTML = ''
  container.appendChild(renderer.domElement)

  const count = props.particleCount
  const positions = buildInhoPixDrePositions(count)
  const seeds = new Float32Array(count)
  for (let i = 0; i < count; i++) seeds[i] = Math.random()

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('aRandomSeed', new THREE.BufferAttribute(seeds, 1))

  const material = new THREE.ShaderMaterial({
    vertexShader: VERTEX_SHADER,
    fragmentShader: FRAGMENT_SHADER,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    uniforms: {
      uTime: { value: 0 },
      uPointer: { value: new THREE.Vector2(99, 99) },
      uPrimaryColor: { value: new THREE.Color(props.accentColor) },
      uSecondaryColor: { value: new THREE.Color(props.secondaryColor) },
    },
  })

  const points = new THREE.Points(geometry, material)
  scene.add(points)

  const targetPointer = new THREE.Vector2(99, 99)
  const handlePointerMove = (e) => {
    const rect = container.getBoundingClientRect()
    targetPointer.set(
      ((e.clientX - rect.left) / rect.width) * 2 - 1,
      -((e.clientY - rect.top) / rect.height) * 2 + 1
    )
  }
  const handlePointerLeave = () => targetPointer.set(99, 99)
  container.addEventListener('pointermove', handlePointerMove)
  container.addEventListener('pointerleave', handlePointerLeave)

  let isVisible = true
  const observer = new IntersectionObserver(
    ([entry]) => {
      isVisible = entry.isIntersecting
    },
    { threshold: 0.05 }
  )
  observer.observe(container)

  const resizeObserver = new ResizeObserver(() => {
    const w = container.clientWidth
    const h = Math.max(container.clientHeight, 1)
    camera.aspect = w / h
    camera.updateProjectionMatrix()
    renderer.setSize(w, h)
  })
  resizeObserver.observe(container)

  const clock = new THREE.Clock()
  const animate = () => {
    frameId = requestAnimationFrame(animate)
    if (!isVisible || document.hidden) return

    const elapsed = clock.getElapsedTime()
    material.uniforms.uTime.value = elapsed
    material.uniforms.uPointer.value.lerp(targetPointer, 0.12)

    points.rotation.y = Math.sin(elapsed * 0.35) * 0.28
    points.rotation.x = Math.cos(elapsed * 0.25) * 0.08

    renderer.render(scene, camera)
  }
  animate()

  cleanups.push(() => {
    cancelAnimationFrame(frameId)
    observer.disconnect()
    resizeObserver.disconnect()
    container.removeEventListener('pointermove', handlePointerMove)
    container.removeEventListener('pointerleave', handlePointerLeave)
    geometry.dispose()
    material.dispose()
    renderer.dispose()
    if (renderer.domElement.parentNode === container) {
      container.removeChild(renderer.domElement)
    }
  })
})

onUnmounted(() => {
  cleanups.forEach((fn) => fn())
})
</script>
