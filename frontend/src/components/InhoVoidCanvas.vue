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
  secondaryColor: { type: String, default: '#10b981' },
  particleCount: { type: Number, default: 7000 },
})

const mountRef = ref(null)

const VERTEX_SHADER = `
  uniform float uTime;
  uniform vec2 uPointer;
  uniform float uPixelRatio;
  attribute float aRandomSeed;
  varying vec3 vColor;
  varying float vDistToPointer;
  varying float vSeed;

  void main() {
    vSeed = aRandomSeed;
    vec3 pos = position;
    float seed = aRandomSeed * 6.2831853;
    float wave = sin(uTime * 1.6 + seed) * 0.025;
    pos += normal * wave;

    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    vec2 screenPos = gl_Position.xy / gl_Position.w;
    vDistToPointer = length(screenPos - uPointer);

    float sizePulse = 1.0 + sin(uTime * 2.2 + seed * 3.5) * 0.22;
    float pointerAttract = smoothstep(0.7, 0.0, vDistToPointer) * 1.2;
    
    // Crisp micro-particle sizing with device pixel ratio scaling
    gl_PointSize = (2.2 * sizePulse + pointerAttract * 1.4) * uPixelRatio;
    gl_PointSize = clamp(gl_PointSize, 1.0, 5.0);
  }
`

const FRAGMENT_SHADER = `
  uniform vec3 uPrimaryColor;
  uniform vec3 uSecondaryColor;
  varying float vDistToPointer;
  varying float vSeed;

  void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    if (dist > 0.5) discard;

    // Specular center with sharp neon quantum falloff
    float core = smoothstep(0.45, 0.0, dist);
    float glow = smoothstep(0.5, 0.15, dist);
    vec3 baseColor = mix(uPrimaryColor, uSecondaryColor, vSeed);

    float cursorHighlight = smoothstep(0.7, 0.0, vDistToPointer);
    vec3 finalColor = mix(baseColor, vec3(0.92, 0.98, 1.0), cursorHighlight * 0.7);

    float alpha = (core * 0.85 + glow * 0.35) * (0.8 + cursorHighlight * 0.2);
    gl_FragColor = vec4(finalColor, alpha);
  }
`

function buildInhoPixDrePositions(count) {
  const geos = []

  const addQrFinderPattern = (cx, cy) => {
    const size = 0.72
    const thickness = 0.10
    const depth = 0.14

    const top = new THREE.BoxGeometry(size, thickness, depth)
    top.translate(cx, cy + size / 2 - thickness / 2, 0)
    const bottom = new THREE.BoxGeometry(size, thickness, depth)
    bottom.translate(cx, cy - size / 2 + thickness / 2, 0)
    const left = new THREE.BoxGeometry(thickness, size, depth)
    left.translate(cx - size / 2 + thickness / 2, cy, 0)
    const right = new THREE.BoxGeometry(thickness, size, depth)
    right.translate(cx + size / 2 - thickness / 2, cy, 0)
    const center = new THREE.BoxGeometry(0.26, 0.26, depth * 1.1)
    center.translate(cx, cy, 0)

    geos.push(top, bottom, left, right, center)
  }

  // 3 Finders do QR Code PIX
  addQrFinderPattern(-1.25, 0.70)
  addQrFinderPattern(1.25, 0.70)
  addQrFinderPattern(-1.25, -0.70)

  // 4 Barras verticais de análise contábil DRE
  const barHeights = [0.8, 1.3, 1.8, 2.3]
  barHeights.forEach((h, i) => {
    const x = -0.22 + i * 0.42
    const bar = new THREE.BoxGeometry(0.22, h, 0.25)
    bar.translate(x, -0.75 + h / 2, 0)
    geos.push(bar)
  })

  // Amostragem volumétrica homogênea
  const positions = new Float32Array(count * 3)
  for (let i = 0; i < count; i++) {
    const geo = geos[Math.floor(Math.random() * geos.length)]
    const posAttr = geo.getAttribute('position')
    const idx = Math.floor(Math.random() * posAttr.count)
    positions[i * 3] = posAttr.getX(idx) + (Math.random() - 0.5) * 0.04
    positions[i * 3 + 1] = posAttr.getY(idx) + (Math.random() - 0.5) * 0.04
    positions[i * 3 + 2] = posAttr.getZ(idx) + (Math.random() - 0.5) * 0.04
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
    42,
    container.clientWidth / Math.max(container.clientHeight, 1),
    0.1,
    100
  )
  camera.position.set(0, 0.35, 5.8)

  const pixelRatio = Math.min(window.devicePixelRatio || 1, 2)
  renderer.setPixelRatio(pixelRatio)
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
      uPixelRatio: { value: pixelRatio },
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

    // Ajusta z para manter enquadramento perfeito em telas mobile e desktop
    if (camera.aspect < 1.0) {
      camera.position.z = 5.8 / Math.max(camera.aspect, 0.65)
    } else {
      camera.position.z = 5.8
    }

    camera.updateProjectionMatrix()
    renderer.setSize(w, h)
    material.uniforms.uPixelRatio.value = renderer.getPixelRatio()
  })
  resizeObserver.observe(container)

  const clock = new THREE.Clock()
  const animate = () => {
    frameId = requestAnimationFrame(animate)
    if (!isVisible || document.hidden) return

    const elapsed = clock.getElapsedTime()
    material.uniforms.uTime.value = elapsed
    material.uniforms.uPointer.value.lerp(targetPointer, 0.12)

    points.rotation.y = Math.sin(elapsed * 0.3) * 0.22
    points.rotation.x = Math.cos(elapsed * 0.22) * 0.06

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
