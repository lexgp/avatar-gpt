<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as THREE from 'three'
import { Character } from '../three/character'
import Sidebar from './Sidebar.vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)

let renderer: THREE.WebGLRenderer
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
const character = new Character();


// Анимация
const clock = new THREE.Clock();
let previousTime = 0;

onMounted(() => {
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x222222)

  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.set(0, 1.5, 3)

  renderer = new THREE.WebGLRenderer({
    canvas: canvasRef.value as HTMLCanvasElement,
    antialias: true,
  })
  renderer.setSize(window.innerWidth, window.innerHeight)

  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2)
  scene.add(hemiLight)
  const dirLight = new THREE.DirectionalLight(0xffffff, 1)
  dirLight.position.set(3, 10, 10)
  scene.add(dirLight)

  // Создание персонажа
  character.loadModel('/68b6c51d3000de881070b3dc.glb', (model: THREE.Object3D) => {
    scene.add(model);
  });

  animate()
  window.addEventListener('resize', onResize)
})

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

function animate() {
  requestAnimationFrame(animate);
  
  const currentTime = clock.getElapsedTime();
  const deltaTime = currentTime - previousTime;
  previousTime = currentTime;
  
  // Обновление персонажа
  character.update(deltaTime);
  
  // Idle-анимация тела
  scene.position.y = character.getIdleBodyMovement();
  
  renderer.render(scene, camera);
}

function talk() {
  character.speakForDuration(4); // Говорить 4 секунды
}
</script>

<template>
  <div>
    <Sidebar />
    <el-button type="primary" @click="talk" style="position: absolute; top: 10px; left: 10px; z-index: 10;">
      Сказать
    </el-button>
    <canvas ref="canvasRef" style="width: 100vw; height: 100vh; display: block;"></canvas>
  </div>
</template>