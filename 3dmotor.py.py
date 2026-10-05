import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="3D Araba Motoru Simulasyonu", layout="wide")

# PREMIUM ARAYUZ - kenar 0 ama guzel detaylar
st.markdown("""
<style>
.block-container {padding-top: 0.5rem !important; padding-bottom: 0 !important; padding-left: 0 !important; padding-right: 0 !important; max-width: 100% !important;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stApp {background: radial-gradient(circle at 50% 30%, #1e293b 0%, #0f172a 40%, #020617 100%) !important;}
.title-box {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 14px 20px;
  margin: 12px 16px;
  display:flex;
  justify-content: space-between;
  align-items:center;
}
.title-box h2 {margin:0 !important; color:#f1f5f9; font-size:22px; letter-spacing:0.5px}
.badge {background: linear-gradient(135deg, #38bdf8, #818cf8); color:white; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600}
.info-bar {text-align:center; color:#94a3b8; font-size:13px; margin: 0 0 12px 0; letter-spacing:0.3px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
  <h2>🚗 İnteraktif 3D Motor Simülasyonu</h2>
  <div class="badge">GLB • Real-time • Trackpad destekli</div>
</div>
<p class="info-bar">🖱️ Sürükle = Döndür &nbsp;|&nbsp; 🔍 Tekerlek = Zoom &nbsp;|&nbsp; 👆 İki parmak = Kaydır</p>
""", unsafe_allow_html=True)

POSSIBLE_NAMES = ["motor-v2.glb", "motor.glb", "engine.glb", "car engine 3d model.glb", "model.glb"]

glb_b64 = ""
found_file = None
for name in POSSIBLE_NAMES:
    if os.path.exists(name) and os.path.getsize(name) > 1000:
        found_file = name
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        break

if found_file:
    st.sidebar.success(f"{found_file} - {os.path.getsize(found_file)/1024/1024:.2f} MB")

html_template = f'''
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}}}
</script>
<style>
  html, body {{margin:0;padding:0;overflow:hidden; background: transparent; width:100%; height:100%}}
  #c{{width:100vw;height:calc(100vh - 110px);display:block; border-radius: 20px 20px 0 0;}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';
import {{DRACOLoader}} from 'three/addons/loaders/DRACOLoader.js';

const scene = new THREE.Scene();
// ACIK PREMIUM ARKA PLAN - koyu lacivert gri gradient yerine sahne rengi
scene.background = new THREE.Color(0x121827);
scene.fog = new THREE.Fog(0x121827, 8, 15);

const camera = new THREE.PerspectiveCamera(40, window.innerWidth/(window.innerHeight-110), 0.1, 100);
camera.position.set(1.8, 1.0, 1.8);

const renderer = new THREE.WebGLRenderer({{canvas:document.getElementById('c'), antialias:true, alpha:true}});
renderer.setSize(window.innerWidth, window.innerHeight-110);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 0.5;
controls.maxDistance = 8;

// PREMIUM ISIKLAR - daha acik ve detayli
scene.add(new THREE.AmbientLight(0xffffff, 0.8));
const key = new THREE.DirectionalLight(0xffffff, 1.8); key.position.set(5,8,5); key.castShadow=true; scene.add(key);
const fill = new THREE.DirectionalLight(0x93c5fd, 0.6); fill.position.set(-5,3,-2); scene.add(fill);
const rim = new THREE.DirectionalLight(0xfde68a, 0.4); rim.position.set(0,4,-6); scene.add(rim);

// ZEMINDE YUMUSAK GOLGE - tabla yok ama hafif yansima
const ground = new THREE.Mesh(new THREE.CircleGeometry(3, 64), new THREE.ShadowMaterial({{opacity:0.15}}));
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.7;
ground.receiveShadow = true;
scene.add(ground);

const engineGroup = new THREE.Group();
scene.add(engineGroup);

function loadFromBase64(b64){{
  if(!b64 || b64.length < 10) return;
  const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
  const loader = new GLTFLoader();
  const draco = new DRACOLoader();
  draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
  loader.setDRACOLoader(draco);
  loader.parse(bytes.buffer, '', (gltf)=>{{
    const model = gltf.scene;
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    model.position.y += 0.2;
    const size = box.getSize(new THREE.Vector3()).length();
    model.scale.setScalar(1.9/size);
    model.traverse(o=>{{ if(o.isMesh){{ o.castShadow=true; o.receiveShadow=true; }} }});
    engineGroup.add(model);
  }});
}}

function animate(){{
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}}
animate();
loadFromBase64("{glb_b64}");

window.addEventListener('resize', ()=>{{
  camera.aspect = window.innerWidth/(window.innerHeight-110);
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight-110);
}});
</script>
</body>
</html>
'''

components.html(html_template, height=860, scrolling=False)
