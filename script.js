/**
 * ============================================================================
 * MUSEUM SENI VINCENT VAN GOGH - VIRTUAL EXHIBITION ARCHITECTURE
 * Professional Front-End & WebXR Engine (Vanilla JS ES6+)
 * ============================================================================
 * 
 * 1) PANDUAN MENGGANTI GAMBAR LUKISAN (BINGKAI 3D & PANEL INFORMASI):
 * Anda dapat dengan sangat mudah mengganti gambar lukisan yang tampil di:
 * - Bingkai 3D di dalam ruangan museum
 * - Panel Informasi saat lukisan di-inspect
 * Cukup ubah properti `image` di dalam `MUSEUM_CATALOG` di bawah ini dengan
 * path file lokal (misal: "assets/images/lukisan_saya.jpg") atau URL gambar.
 * 
 * 2) PANDUAN MENGGANTI AUDIO DENGAN FILE MP3 ANDA SENDIRI:
 * Jika Anda ingin memutar file audio/lagu MP3 hasil download Anda sendiri:
 * - Letakkan file MP3 Anda ke dalam folder `assets/audio/` (misal: `musik.mp3`).
 * - Isi variabel `CUSTOM_AUDIO_PATH` di bawah ini dengan path file tersebut.
 * - Jika `CUSTOM_AUDIO_PATH` diisi, museum otomatis memutar file MP3 Anda!
 * - Jika dikosongkan (""), museum memutar sintesis Beethoven - Für Elise.
 * ============================================================================
 */
const CUSTOM_AUDIO_PATH = "";


const MUSEUM_CATALOG = {
  "starry-night": {
    title: "The Starry Night",
    year: "1889",
    subtitle: "Saint-Rémy-de-Provence, Prancis",
    image: "assets/images/starry_night.jpg", 
    textureId: "art-starry",
    fallbackImage: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
    description: "Tahun 1889.\nDilukis ketika Van Gogh berada di Saint-Rémy.\nMerupakan salah satu karya paling terkenal di dunia dengan sapuan kuas berputar yang ikonik serta langit malam yang emosional."
  },
  "sunflowers": {
    title: "Sunflowers (Bunga Matahari)",
    year: "1888",
    subtitle: "Arles, Prancis",
    image: "assets/images/sunflowers.jpg", 
    textureId: "art-sunflowers",
    fallbackImage: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/800px-Vincent_Willem_van_Gogh_127.jpg",
    description: "Tahun 1888.\nMelambangkan persahabatan dan kehidupan.\nDilukis dengan nuansa kuning keemasan yang hangat untuk menyambut sahabatnya Paul Gauguin."
  },
  "bedroom-arles": {
    title: "Bedroom in Arles",
    year: "1888",
    subtitle: "Arles, Prancis",
    image: "assets/images/bedroom_in_arles.jpg",
    textureId: "art-bedroom",
    fallbackImage: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Vincent_van_Gogh_-_De_slaapkamer_-_Google_Art_Project.jpg/1024px-Vincent_van_Gogh_-_De_slaapkamer_-_Google_Art_Project.jpg",
    description: "Tahun 1888.\nMenggambarkan kamar tidur Van Gogh di Arles, Prancis.\nMenonjolkan warna sederhana untuk memberi ketenangan."
  },
  "van-gogh-sculpture": {
    title: "Vincent Van Gogh",
    year: "1853 - 1890",
    subtitle: "Master Post-Impressionism",
    image: "assets/images/vincent_van_gogh.jpg",
    fallbackImage: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg/800px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg",
    description: "Pelukis Post-Impressionism asal Belanda yang menghasilkan lebih dari 2.000 karya seni."
  }
};

/* ============================================================================
   SINGLE STREAM BACKGROUND AUDIO ENGINE & SOUND EFFECTS
   ============================================================================ */
class MuseumAudioEngine {
  constructor() {
    this.ctx = null;
    this.isMuted = false;
    this.audioStarted = false;
    this.bgAudio = null;
  }

  init() {
    // Inisialisasi AudioContext hanya untuk sound effects (hover, langkah kaki, tembakan)
    if (!this.ctx) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
      } catch (e) {
        console.warn("AudioContext siap setelah interaksi pengguna.");
      }
    } else if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.isMuted = !this.isMuted;
    if (this.bgAudio) {
      this.bgAudio.muted = this.isMuted;
    }
    return this.isMuted;
  }

  playHoverChime() {
    if (!this.ctx || this.isMuted) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(659.25, this.ctx.currentTime); // E5
    osc.frequency.exponentialRampToValueAtTime(880.00, this.ctx.currentTime + 0.35);
    gain.gain.setValueAtTime(0.07, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.38);
    osc.connect(gain); gain.connect(this.ctx.destination);
    osc.start(); osc.stop(this.ctx.currentTime + 0.38);
  }

  playFootstep() {
    if (!this.ctx || this.isMuted) return;
    const bufferSize = this.ctx.sampleRate * 0.05;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
    }
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(420, this.ctx.currentTime);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.03, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);

    noise.connect(filter); filter.connect(gain); gain.connect(this.ctx.destination);
    noise.start();
  }

  playShootSound() {
    if (!this.ctx || this.isMuted) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(440, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(110, this.ctx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
    osc.connect(gain); gain.connect(this.ctx.destination);
    osc.start(); osc.stop(this.ctx.currentTime + 0.18);
  }

  startMagicalAmbient() {
    if (!this.ctx || this.isMuted) return;
    if (this.ambientOsc) return; 
    
    this.ambientOsc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    this.ambientOsc.type = 'triangle';
    this.ambientOsc.frequency.setValueAtTime(110, this.ctx.currentTime); 
    
    gain.gain.setValueAtTime(0, this.ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.06, this.ctx.currentTime + 2); 
    
    const lfo = this.ctx.createOscillator();
    lfo.type = 'sine';
    lfo.frequency.setValueAtTime(0.15, this.ctx.currentTime);
    const lfoGain = this.ctx.createGain();
    lfoGain.gain.setValueAtTime(8, this.ctx.currentTime);
    lfo.connect(lfoGain);
    lfoGain.connect(this.ambientOsc.frequency);
    lfo.start();
    this.ambientLfo = lfo;
    
    this.ambientOsc.connect(gain);
    gain.connect(this.ctx.destination);
    this.ambientOsc.start();
    this.ambientGain = gain;
  }

  stopMagicalAmbient() {
    if (this.ambientOsc && this.ambientGain) {
      this.ambientGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 1);
      setTimeout(() => {
        if (this.ambientOsc) {
          this.ambientOsc.stop();
          this.ambientOsc = null;
          if (this.ambientLfo) this.ambientLfo.stop();
        }
      }, 1000);
    }
  }
}

const museumAudio = new MuseumAudioEngine();

/* Sinkronisasi otomatis gambar lukisan dari MUSEUM_CATALOG ke bingkai 3D di index.html */
function syncMuseumCatalogImages() {
  Object.values(MUSEUM_CATALOG).forEach(item => {
    if (item.textureId) {
      const imgEl = document.getElementById(item.textureId);
      if (imgEl && item.image) {
        imgEl.setAttribute('src', item.image);
        imgEl.onload = () => {
          document.querySelectorAll('a-plane').forEach(plane => {
            const mesh = plane.getObject3D('mesh');
            if (mesh && mesh.material && mesh.material.map) {
              mesh.material.map.needsUpdate = true;
              mesh.material.needsUpdate = true;
            }
          });
        };
      }
    }
  });
}

/* COMPONENT: ARTWORK INSPECTOR (1 SECOND RAYCASTER HOLD) */
AFRAME.registerComponent('artwork-inspector', {
  schema: { exhibitId: { type: 'string', default: 'starry-night' } },

  init: function () {
    this.hoverStartTime = 0;
    this.isHovering = false;
    this.hasTriggered = false;
    this.inspectDuration = 1000; // 1 detik

    this.onRaycasterIntersected = this.onRaycasterIntersected.bind(this);
    this.onRaycasterIntersectedCleared = this.onRaycasterIntersectedCleared.bind(this);

    this.el.addEventListener('mouseenter', this.onRaycasterIntersected);
    this.el.addEventListener('mouseleave', this.onRaycasterIntersectedCleared);
  },

  onRaycasterIntersected: function () {
    this.isHovering = true;
    this.hoverStartTime = performance.now();
    this.hasTriggered = false;
    const crosshair = document.querySelector('.crosshair-wrapper');
    if (crosshair) crosshair.classList.add('hovering');
  },

  onRaycasterIntersectedCleared: function () {
    this.isHovering = false;
    this.hasTriggered = false;
    this.updateProgressRing(0);
    const crosshair = document.querySelector('.crosshair-wrapper');
    if (crosshair) crosshair.classList.remove('hovering');
  },

  tick: function (time) {
    if (!this.isHovering || this.hasTriggered) return;
    const elapsed = time - this.hoverStartTime;
    const progress = Math.min(1, elapsed / this.inspectDuration);
    this.updateProgressRing(progress);

    if (progress >= 1.0 && !this.hasTriggered) {
      this.hasTriggered = true;
      this.openArtworkModal();
    }
  },

  updateProgressRing: function (progress) {
    const circle = document.querySelector('.progress-ring-circle');
    if (!circle) return;
    circle.style.strokeDashoffset = 113.1 - (progress * 113.1);
  },

  openArtworkModal: function () {
    const data = MUSEUM_CATALOG[this.data.exhibitId];
    if (!data) return;

    museumAudio.playHoverChime();

    document.getElementById('modal-title').textContent = data.title;
    document.getElementById('modal-subtitle').textContent = `${data.year} • ${data.subtitle}`;
    document.getElementById('modal-description').textContent = data.description;
    document.getElementById('modal-badge').textContent = data.year;
    
    const imgEl = document.getElementById('modal-image');
    imgEl.src = data.image;
    imgEl.onerror = () => { imgEl.src = data.fallbackImage; };

    document.getElementById('info-modal').classList.add('active');
  }
});

/* COMPONENT: PORTAL TELEPORTER (3 SECOND RAYCASTER HOLD) */
AFRAME.registerComponent('portal-teleporter', {
  schema: { target: { type: 'string', default: 'lobby' } },

  init: function () {
    this.isHovering = false;
    this.hoverStartTime = 0;
    this.hasTriggered = false;
    this.inspectDuration = 1500; // 1.5 detik

    this.onRaycasterIntersected = this.onRaycasterIntersected.bind(this);
    this.onRaycasterIntersectedCleared = this.onRaycasterIntersectedCleared.bind(this);

    this.el.addEventListener('mouseenter', this.onRaycasterIntersected);
    this.el.addEventListener('mouseleave', this.onRaycasterIntersectedCleared);
  },

  onRaycasterIntersected: function () {
    this.isHovering = true;
    this.hoverStartTime = performance.now();
    this.hasTriggered = false;
    const crosshair = document.querySelector('.crosshair-wrapper');
    if (crosshair) crosshair.classList.add('hovering');
  },

  onRaycasterIntersectedCleared: function () {
    this.isHovering = false;
    this.hasTriggered = false;
    this.updateProgressRing(0);
    const crosshair = document.querySelector('.crosshair-wrapper');
    if (crosshair) crosshair.classList.remove('hovering');
  },

  tick: function (time) {
    if (!this.isHovering || this.hasTriggered) return;
    const elapsed = time - this.hoverStartTime;
    const progress = Math.min(1, elapsed / this.inspectDuration);
    this.updateProgressRing(progress);

    if (progress >= 1.0 && !this.hasTriggered) {
      this.hasTriggered = true;
      this.teleport();
    }
  },

  updateProgressRing: function (progress) {
    const circle = document.querySelector('.progress-ring-circle');
    if (!circle) return;
    circle.style.strokeDashoffset = 113.1 - (progress * 113.1);
  },

  teleport: function () {
    const playerRig = document.getElementById('player-rig');
    const fadeScreen = document.getElementById('fade-screen');
    
    museumAudio.playHoverChime();

    // 1. Fade out to black (0.5s)
    fadeScreen.setAttribute('animation', 'property: material.opacity; to: 1; dur: 500; easing: easeInOutQuad');
    
    setTimeout(() => {
      // 2. Move player and reset camera local position
      const cameraEl = document.getElementById('camera');
      if (this.data.target === 'starry-castle') {
        playerRig.setAttribute('position', '1000 1.12 1000');
        if (cameraEl) cameraEl.setAttribute('position', '0 0 0');
        if (typeof museumAudio !== 'undefined') museumAudio.startMagicalAmbient();
      } else if (this.data.target === 'bedroom-arles') {
        playerRig.setAttribute('position', '2000 1.12 1000');
        if (cameraEl) cameraEl.setAttribute('position', '0 0 0');
        if (typeof museumAudio !== 'undefined') museumAudio.stopMagicalAmbient();
      } else if (this.data.target === 'lobby') {
        playerRig.setAttribute('position', '0 1.12 13');
        if (cameraEl) cameraEl.setAttribute('position', '0 0 0');
        if (typeof museumAudio !== 'undefined') museumAudio.stopMagicalAmbient();
      }

      // 3. Fade back in (0.5s)
      fadeScreen.setAttribute('animation', 'property: material.opacity; to: 0; dur: 500; easing: easeInOutQuad');
      
      // Reset hovering state
      this.isHovering = false;
      this.hasTriggered = false;
      this.updateProgressRing(0);
      const crosshair = document.querySelector('.crosshair-wrapper');
      if (crosshair) crosshair.classList.remove('hovering');
      
    }, 550);
  }
});

/* COMPONENT: PLAYER CONTROLLER (SPACE TO JUMP + FOOTSTEPS) */
AFRAME.registerComponent('player-museum-controller', {
  init: function () {
    this.velocity = new THREE.Vector3();
    this.isJumping = false;
    this.jumpForce = 4.8;
    this.gravity = -12.5;
    this.floorY = 1.12; // eye level anak kecil umur 6 tahun (1.12 meter)
    this.lastFootstepTime = 0;

    window.addEventListener('keydown', (evt) => {
      if (evt.code === 'Space' && !this.isJumping) {
        evt.preventDefault();
        this.velocity.y = this.jumpForce;
        this.isJumping = true;
      }
    });
  },

  tick: function (time, delta) {
    const dt = delta / 1000;
    if (dt > 0.1) return;

    // Handle jumping on the RIG
    const rigPos = this.el.getAttribute('position');
    if (this.isJumping || rigPos.y > this.floorY) {
      this.velocity.y += this.gravity * dt;
      rigPos.y += this.velocity.y * dt;
      if (rigPos.y <= this.floorY) {
        rigPos.y = this.floorY;
        this.velocity.y = 0;
        this.isJumping = false;
      }
      this.el.setAttribute('position', rigPos);
    }

    // Handle collision clamping on the CAMERA absolute world position
    const cameraEl = document.getElementById('camera');
    if (!cameraEl) return;
    const camPos = cameraEl.getAttribute('position');
    
    let worldX = rigPos.x + camPos.x;
    let worldZ = rigPos.z + camPos.z;

    if (worldX > 1500) {
      // Bedroom in Arles Boundary (Room is 8x8, centered at 2000, 1000)
      // X limits: 2000 - 3.8 to 2000 + 3.8
      // Z limits: 1000 - 3.8 to 1000 + 3.8
      worldX = Math.max(1996.2, Math.min(2003.8, worldX));
      worldZ = Math.max(996.2, Math.min(1003.8, worldZ));
    } else if (worldX > 500) {
      // Starry Night 360 Boundary (Radius 40)
      const dx = worldX - 1000;
      const dz = worldZ - 1000;
      const dist = Math.sqrt(dx*dx + dz*dz);
      if (dist > 40) {
        worldX = 1000 + (dx / dist) * 40;
        worldZ = 1000 + (dz / dist) * 40;
      }
    } else {
      // Museum Boundaries
      worldZ = Math.max(-36.2, Math.min(14.8, worldZ));
      
      if (worldZ > -26.5) {
        // Main Hall
        worldX = Math.max(-4.2, Math.min(4.2, worldX));
      } else {
        // T-Junction Hallway
        worldX = Math.max(-24.2, Math.min(24.2, worldX));
        // Block walking back into the void from the wings
        if (worldX > 4.2 || worldX < -4.2) {
          worldZ = Math.max(-36.2, Math.min(-26.5, worldZ));
        }
      }
    }

    // Apply back to camera's local position
    camPos.x = worldX - rigPos.x;
    camPos.z = worldZ - rigPos.z;
    cameraEl.setAttribute('position', camPos);

    this.updateRoomTracker(worldX, worldZ);

    if (!this.lastPos) {
      this.lastPos = new THREE.Vector3(worldX, rigPos.y, worldZ);
    } else {
      const distMoved = Math.hypot(worldX - this.lastPos.x, worldZ - this.lastPos.z);
      if (distMoved > 0.05 && !this.isJumping && time - this.lastFootstepTime > 420) {
        museumAudio.playFootstep();
        this.lastFootstepTime = time;
      }
      this.lastPos.set(worldX, rigPos.y, worldZ);
    }
  },

  updateRoomTracker: function (worldX, worldZ) {
    const tracker = document.getElementById('current-room-text');
    if (!tracker) return;
    if (worldX > 1500) tracker.innerText = 'Kamar Tidur (Bedroom in Arles)';
    else if (worldX > 500) tracker.innerText = 'Starry Night 360';
    else if (worldZ > 5) tracker.innerText = 'Lobi (Pintu Masuk)';
    else if (worldZ <= 5 && worldZ > -26) tracker.innerText = 'Galeri Utama';
    else if (worldZ <= -26) tracker.innerText = 'Lorong Museum';
  }
});

/* COMPONENT: OBJECT POOL PROJECTILE SHOOTER (LEFT CLICK) */
AFRAME.registerComponent('projectile-pool-shooter', {
  init: function () {
    this.poolSize = 12;
    this.pool = [];
    this.currentIndex = 0;
    const scene = this.el.sceneEl;

    for (let i = 0; i < this.poolSize; i++) {
      const sphere = document.createElement('a-entity');
      sphere.setAttribute('geometry', 'primitive: sphere; radius: 0.12; segmentsWidth: 12; segmentsHeight: 12');
      sphere.setAttribute('material', 'color: #00E5FF; emissive: #00E5FF; emissiveIntensity: 1.5; roughness: 0.2');
      sphere.setAttribute('position', '0 -100 0');
      sphere.setAttribute('visible', 'false');
      scene.appendChild(sphere);

      this.pool.push({ el: sphere, active: false, velocity: new THREE.Vector3(), life: 0 });
    }

    window.addEventListener('mousedown', (evt) => {
      if (evt.button !== 0) return;
      const modal = document.getElementById('info-modal');
      if (modal && modal.classList.contains('active')) return;
      this.shootProjectile();
    });
  },

  shootProjectile: function () {
    const cameraEl = document.querySelector('#camera');
    if (!cameraEl) return;

    museumAudio.playShootSound();
    const proj = this.pool[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.poolSize;

    const camObj = cameraEl.object3D;
    const worldPos = new THREE.Vector3();
    camObj.getWorldPosition(worldPos);

    const forward = new THREE.Vector3(0, 0, -1);
    forward.applyQuaternion(camObj.quaternion);

    proj.el.setAttribute('position', { x: worldPos.x, y: worldPos.y - 0.15, z: worldPos.z });
    proj.el.setAttribute('visible', 'true');
    proj.velocity.copy(forward).multiplyScalar(18.0);
    proj.life = 2.2;
    proj.active = true;
  },

  tick: function (time, delta) {
    const dt = delta / 1000;
    if (dt > 0.1) return;

    for (let i = 0; i < this.poolSize; i++) {
      const p = this.pool[i];
      if (!p.active) continue;
      p.life -= dt;
      if (p.life <= 0) {
        p.active = false;
        p.el.setAttribute('visible', 'false');
        p.el.setAttribute('position', '0 -100 0');
        continue;
      }
      const pos = p.el.getAttribute('position');
      pos.x += p.velocity.x * dt;
      pos.y += p.velocity.y * dt;
      pos.z += p.velocity.z * dt;
      p.el.setAttribute('position', pos);
    }
  }
});

document.addEventListener('DOMContentLoaded', () => {
  syncMuseumCatalogImages();

  // Langsung inisiasi audio saat masuk museum
  museumAudio.init();

  // Pastikan audio berjalan setelah interaksi pertama pengguna (mengatasi kebijakan autoplay browser)
  const unlockAudio = () => {
    if (museumAudio && !museumAudio.audioStarted) {
      museumAudio.init();
    }
    const radioSoundEl = document.getElementById('museum-radio-sound');
    if (radioSoundEl && radioSoundEl.components && radioSoundEl.components.sound) {
      radioSoundEl.components.sound.playSound();
    }
    window.removeEventListener('click', unlockAudio);
    window.removeEventListener('keydown', unlockAudio);
  };
  window.addEventListener('click', unlockAudio);
  window.addEventListener('keydown', unlockAudio);

  const closeBtn = document.getElementById('close-modal-btn');
  const modal = document.getElementById('info-modal');
  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => { modal.classList.remove('active'); });
  }

  const audioBtn = document.getElementById('audio-toggle-btn');
  if (audioBtn) {
    audioBtn.addEventListener('click', () => {
      museumAudio.init();
      const muted = museumAudio.toggleMute();
      audioBtn.innerHTML = muted ? '🔇 SFX: OFF' : '🔊 SFX: ON';
    });
  }
});
