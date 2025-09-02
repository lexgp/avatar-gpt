import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export class Character {
  
  private model: THREE.Object3D | null = null;
  private mouthMeshes: THREE.Mesh[] = [];
  private headBone: THREE.Object3D | null = null;
  
  private isTalking = false;
  private talkTimer = 0;
  private idleTimer = 0;
  
  private smileValue = 0;
  private targetSmile = 0;
  private lastSmileChange = 0;
  private smilePattern = [0, 0.2, 0.5, 0.1, 0.3, 0, 0.6, 0.2];
  
  private position = new THREE.Vector3(0, -0.1, 2.7);
  private rotation = new THREE.Euler(0, -0.4, 0);
  

  constructor() {}

  loadModel(url: string, onLoadCallback: Function|null = null) {
    const loader = new GLTFLoader();
    
    loader.load(url, (gltf: any) => {
      this.model = gltf.scene;
      
      if (!this.model) {
        throw new Error('Не удалось загрузить модель')
      }

      this.model.position.copy(this.position);
      this.model.rotation.copy(this.rotation);
      
      this.findMorphTargets();
      this.findHeadBone();
      
      if (onLoadCallback) {
        onLoadCallback(this.model);
      }
      
    }, undefined, (error: any) => {
      console.error('Ошибка загрузки модели:', error);
    });
  }

  findMorphTargets() {
    if (!this.model) return;
    
    this.model.traverse((child: any) => {
      if (child.isMesh && child.morphTargetDictionary) {
        if ('mouthOpen' in child.morphTargetDictionary) {
          this.mouthMeshes.push(child);
        }
      }
    });
  }

  findHeadBone() {
    if (!this.model) return;
    
    this.model.traverse((child: any) => {
      if (child.isBone && /Head/i.test(child.name) && !this.headBone) {
        this.headBone = child;
        console.log('Нашли кость головы:', child.name);
      }
    });
  }

  startTalking(duration: number|null = null) {
    if (this.isTalking) return;
    
    this.isTalking = true;
    this.talkTimer = 0;
    
    if (duration) {
      setTimeout(() => {
        this.stopTalking();
      }, duration * 1000);
    }
  }

  stopTalking() {
    this.isTalking = false;
    
    // Сбрасываем морфинг рта
    this.mouthMeshes.forEach(mesh => {
      if (mesh && mesh.morphTargetDictionary) {
        const idx = mesh.morphTargetDictionary['mouthOpen'];
        if (idx !== undefined && mesh.morphTargetInfluences !== undefined) {
          mesh.morphTargetInfluences[idx] = 0;
        }
      }
    });
  }

  speakForDuration(duration: number|null = null) {
    this.startTalking(duration);
  }

  update(deltaTime: number) {
    this.idleTimer += deltaTime;
    
    this.updateTalkingAnimation(deltaTime);
    this.updateHeadAnimation();
    this.updateSmileAnimation();
  }

  updateTalkingAnimation(deltaTime: number) {
    if (this.isTalking && this.mouthMeshes.length > 0) {
      this.talkTimer += deltaTime * 5; // Скорость анимации говорения
      const val = (Math.sin(this.talkTimer) * 0.5 + 0.5) * 0.8;
      
      this.mouthMeshes.forEach(mesh => {
        if (mesh && mesh.morphTargetDictionary) {
          const idx = mesh.morphTargetDictionary['mouthOpen'];
          if (idx !== undefined && mesh.morphTargetInfluences !== undefined) {
            mesh.morphTargetInfluences[idx] = val;
          }
        }
      });
    }
  }

  updateHeadAnimation() {
    if (this.headBone) {

      if (!this.isTalking) {
        this.headBone.rotation.x = Math.sin(this.idleTimer * 0.7) * 0.1;
        this.headBone.rotation.y = Math.sin(this.idleTimer * 0.5) * 0.2;
      } else {
        const targetX = 0.05
        const targetY = 0.3
        const step = 0.005
        const diffX = targetX - this.headBone.rotation.x
        const diffY = targetY - this.headBone.rotation.y
        if (Math.abs(diffX) > step) {
          this.headBone.rotation.x += diffX > 0 ? step : -step;
        }
        if (Math.abs(diffY) > step) {
          this.headBone.rotation.y += diffY > 0 ? step : -step;
        }
      }
    }
  }

  updateSmileAnimation() {
    if (this.mouthMeshes.length === 0) return;
    
    // Меняем целевое значение улыбки раз в секунду
    if (Math.floor(this.idleTimer) !== this.lastSmileChange) {
      this.lastSmileChange = Math.floor(this.idleTimer);
      this.targetSmile = this.smilePattern[
        Math.floor(Math.random() * this.smilePattern.length)
      ];
    }
    
    // Плавное изменение улыбки
    this.smileValue += (this.targetSmile - this.smileValue) * 0.05;
    
    this.mouthMeshes.forEach(mesh => {
      if (mesh && mesh.morphTargetDictionary) {
        const idx = mesh.morphTargetDictionary['mouthSmile'];
        if (idx !== undefined && mesh.morphTargetInfluences !== undefined) {
          mesh.morphTargetInfluences[idx] = this.smileValue;
        }
      }
    });
  }

  getIdleBodyMovement() {
    return Math.sin(this.idleTimer * 0.8) * 0.02;
  }

  setPosition(x: number, y: number, z: number) {
    this.position.set(x, y, z);
    if (this.model) {
      this.model.position.copy(this.position);
    }
  }

  setRotation(x: number, y: number, z: number) {
    this.rotation.set(x, y, z);
    if (this.model) {
      this.model.rotation.copy(this.rotation);
    }
  }
}