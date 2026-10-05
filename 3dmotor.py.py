import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="3D Araba Motoru", layout="wide")

st.markdown("""
<style>
.block-container {padding: 0 !important; max-width: 100% !important;}
header, footer {visibility: hidden; height:0;}
.stApp {background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin:0; padding:16px 24px 12px 24px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <h2 style="margin:0; color:#f8fafc; font-weight:700;">🚗 İnteraktif 3D Araba Motoru</h2>
      <p style="margin:4px 0 0 0; color:#94a3b8; font-size:13px;">Trackpad ve fare ile tam kontrol • Gerçek zamanlı render</p>
    </div>
    <div style="display:flex; gap:8px;">
      <span style="background:#0ea5e9; color:white; padding:6px 12px; border-radius:20px; font-size:11px; font-weight:700;">LIVE 3D</span>
      <span style="background:rgba(255,255,255,0.1); color:#cbd5e1; padding:6px 12px; border-radius:20px; font-size:11px;">motor-v2.glb</span>
    </div>
  </div>
</div>
<div style="text-align:center; padding:8px; background: rgba(0,0,0,0.2); color:#64748b; font-size:12px;">
  🖱️ Sürükle = Döndür | 🔍 Tekerlek = Zoom | 👆 Sağ tık = Kaydır
</div>
""", unsafe_allow_html=True)

POSSIBLE_NAMES = ["motor-v2.glb", "motor.glb", "engine.glb"]
glb_b64 = ""
for name in POSSIBLE_NAMES:
    if os.path.exists(name) and os.path.getsize(name) > 1000:
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        break

# f-string YOK - SyntaxError imkansiz
html_code = """
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
  html, body {margin:0; padding:0; overflow:hidden; background:#1e293b; width:100%; height:100%}
  #c {width:100vw; height:calc(100vh - 95px); display:block}
</style>
</head>
<body>
<canvas id="c"></canvas>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(42, window.innerWidth/(window.innerHeight-95), 0.1, 100);
camera.position.set(1.6, 0.9, 1.6);

const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight-95);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;

scene.add(new THREE.AmbientLight(0xffffff, 1.2));
let d1 = new THREE.DirectionalLight(0xffffff, 2.0); d1.position.set(5,10,5); scene.add(d1);
let d2 = new THREE.DirectionalLight(0xffffff, 0.9); d2.position.set(-5,4,-3); scene.add(d2);

const grid = new THREE.GridHelper(6, 12, 0x334155, 0x1e293b);
grid.position.y = -0.8;
grid.material.opacity = 0.3;
grid.material.transparent = true;
scene.add(grid);

const engineGroup = new THREE.Group();
scene.add(engineGroup);

const b64 = "__B64__";
const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
const loader = new GLTFLoader();
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);
loader.parse(bytes.buffer, '', (gltf)=>{
  let model = gltf.scene;
  let box = new THREE.Box3().setFromObject(model);
  let center = box.getCenter(new THREE.Vector3());
  model.position.sub(center);
  model.position.y += 0.15;
  let size = box.getSize(new THREE.Vector3()).length();
  model.scale.setScalar(1.9/size);
  model.traverse(o=>{ if(o.isMesh){ o.castShadow=true; }});
  engineGroup.add(model);
});

function animate(){
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', ()=>{
  camera.aspect = window.innerWidth/(window.innerHeight-95);
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight-95);
});
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64)
components.html(final_html, height=800, scrolling=False)
