import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="Oyak Horse Görme Testi", layout="wide")

st.markdown("""
<style>
.block-container {padding: 0!important; max-width: 100%!important;}
header, footer {visibility: hidden; height:0;}
.stApp {background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%)!important;}
</style>
""", unsafe_allow_html=True)

# === YENI BASLIK - ORTADA ===
st.markdown("""
<div style="margin:0; padding:18px 24px 14px 24px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); text-align:center;">
  <h1 style="margin:0; color:#f8fafc; font-weight:800; font-size:26px; letter-spacing:0.5px;">Oyak Horse Görme Testi Uygulaması</h1>
  <p style="margin:6px 0 0 0; color:#94a3b8; font-size:13px;">İnteraktif 3D Motor İnceleme • Gerçek zamanlı render</p>
  <div style="margin-top:10px; display:flex; justify-content:center; gap:8px;">
    <span style="background:#0ea5e9; color:white; padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700;">LIVE 3D</span>
    <span style="background:rgba(255,255,255,0.1); color:#cbd5e1; padding:5px 14px; border-radius:20px; font-size:11px;">motor-v2.glb</span>
  </div>
</div>
<div style="text-align:center; padding:8px; background: rgba(0,0,0,0.2); color:#64748b; font-size:12px;">
  🖱 Sürükle = Döndür | 🔍 Tekerlek = Zoom | 👆 Sağ tık = Kaydır | 🎯 Yağ kapağının olduğu yere tıkla
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🔧 Görme Testi Ayarları")
test_mode = st.sidebar.radio("Mod", ["Sağlam Motor", "Vida Eksik (Test)"])
eksik_sayi = st.sidebar.slider("Kaç vida eksik olsun", 1, 6, 2, disabled=(test_mode=="Sağlam Motor"))

POSSIBLE_NAMES = ["motor3.glb", "motor.glb", "engine.glb"]
glb_b64 = ""
for name in POSSIBLE_NAMES:
    if os.path.exists(name) and os.path.getsize(name) > 1000:
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        break

html_code = """
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
  html, body {margin:0; padding:0; overflow:hidden; background:#1e293b; width:100%; height:100%; font-family: sans-serif;}
  #c {width:100vw; height:calc(100vh - 130px); display:block; cursor: crosshair;}
  #msgBox {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) scale(0.8);
    background: linear-gradient(135deg, #16a34a, #15803d);
    color: white; padding: 24px 36px; border-radius: 16px;
    font-size: 20px; font-weight: 800;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 2px rgba(255,255,255,0.2) inset;
    opacity: 0; pointer-events: none;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 100; text-align: center; line-height: 1.4;
  }
  #msgBox.show { opacity: 1; transform: translate(-50%, -50%) scale(1); pointer-events: auto; }
  #msgBox.error { background: linear-gradient(135deg, #dc2626, #991b1b); }
  #hint {
    position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: rgba(0,0,0,0.6); color: #e2e8f0;
    padding: 8px 16px; border-radius: 20px; font-size: 12px;
    backdrop-filter: blur(6px); z-index: 10;
  }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="msgBox"></div>
<div id="hint">🎯 Test Modunda: Büyük turuncu yağ kapağının olduğu boşluğa tıkla</div>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const TEST_MODE = "__TESTMODE__";
const EKSIK_SAYI = __EKSIK__;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(42, window.innerWidth/(window.innerHeight-130), 0.1, 100);
camera.position.set(1.6, 0.9, 1.6);

const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight-130);
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
grid.position.y = -0.8; grid.material.opacity = 0.3; grid.material.transparent = true;
scene.add(grid);

const engineGroup = new THREE.Group();
scene.add(engineGroup);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hotspotMesh = null;
let modelRef = null;
const msgBox = document.getElementById('msgBox');

function showMessage(text, isError=false){
  msgBox.innerHTML = text;
  msgBox.className = isError? 'error' : '';
  msgBox.classList.add('show');
  setTimeout(()=>{ msgBox.classList.remove('show'); }, 3500);
}

const b64 = "__B64__";
if(b64){
  const bytes = Uint8Array.from(atob(b64), c=>c.charCodeAt(0));
  const loader = new GLTFLoader();
  const draco = new DRACOLoader();
  draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
  loader.setDRACOLoader(draco);
  loader.parse(bytes.buffer, '', (gltf)=>{
    let model = gltf.scene;
    modelRef = model;
    let box = new THREE.Box3().setFromObject(model);
    let center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    model.position.y += 0.15;
    let size = box.getSize(new THREE.Vector3()).length();
    model.scale.setScalar(1.9/size);

    let allMeshes = [];
    model.traverse(o=>{ if(o.isMesh){ allMeshes.push(o); }});
    allMeshes.sort((a,b)=>{
      let sa = new THREE.Box3().setFromObject(a).getSize(new THREE.Vector3()).length();
      let sb = new THREE.Box3().setFromObject(b).getSize(new THREE.Vector3()).length();
      return sa - sb;
    });

    let candidateCap = null;
    let maxY = -1000;
    model.traverse(o=>{
      if(o.isMesh && o.material){
        let col = o.material.color;
        if(col){
          let isYellow = col.r > 0.7 && col.g > 0.5 && col.b < 0.4;
          let b = new THREE.Box3().setFromObject(o);
          let cen = b.getCenter(new THREE.Vector3());
          if(isYellow && cen.y > maxY){
            let s = b.getSize(new THREE.Vector3()).length();
            if(s > 0.05){
              maxY = cen.y;
              candidateCap = o;
            }
          }
        }
      }
    });

    if(TEST_MODE.includes("Vida Eksik")){
      for(let i=0; i<EKSIK_SAYI && i<allMeshes.length; i++){
        allMeshes[i].visible = false;
      }
      if(candidateCap){
        candidateCap.visible = false;
        let worldCapPos = new THREE.Vector3();
        candidateCap.getWorldPosition(worldCapPos);
        let geo = new THREE.SphereGeometry(0.18, 32, 32);
        let mat = new THREE.MeshBasicMaterial({color: 0xff8800, transparent:true, opacity:0.0, depthWrite:false});
        hotspotMesh = new THREE.Mesh(geo, mat);
        hotspotMesh.position.copy(worldCapPos);
        model.add(hotspotMesh);
        hotspotMesh.userData.isHotspot = true;
      } else {
        let geo = new THREE.SphereGeometry(0.2, 32, 32);
        let mat = new THREE.MeshBasicMaterial({color: 0xff8800, transparent:true, opacity:0.0});
        hotspotMesh = new THREE.Mesh(geo, mat);
        hotspotMesh.position.set(0, 0.6, 0);
        hotspotMesh.userData.isHotspot = true;
        model.add(hotspotMesh);
      }
    }
    model.traverse(o=>{ if(o.isMesh){ o.castShadow=true; }});
    engineGroup.add(model);
  });
}

function onClick(event){
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);

  let intersects = [];
  if(hotspotMesh){
    intersects = raycaster.intersectObject(hotspotMesh);
  }
  if(intersects.length > 0){
    if(TEST_MODE.includes("Vida Eksik")){
      showMessage("✅ DOĞRU! HATA BULUNDU!<br><span style='font-size:14px; font-weight:400; opacity:0.9'>Büyük turuncu yağ kapağı eksik</span>", false);
      controls.autoRotate = false;
      hotspotMesh.material.opacity = 0.5;
      hotspotMesh.material.color.set(0x00ff00);
      setTimeout(()=>{ hotspotMesh.material.opacity = 0.0; }, 600);
    } else {
      showMessage("ℹ️ Bu motorda hata yok.<br><span style='font-size:13px'>Test moduna geçin</span>", true);
    }
  } else {
    if(modelRef){
      let allHits = raycaster.intersectObject(modelRef, true);
      if(allHits.length > 0 && TEST_MODE.includes("Vida Eksik")){
        showMessage("❌ Burası değil, tekrar dene!<br><span style='font-size:13px'>Yağ kapağının olduğu üst boşluğa odaklan</span>", true);
      }
    }
  }
}

renderer.domElement.addEventListener('click', onClick);

function animate(){
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', ()=>{
  camera.aspect = window.innerWidth/(window.innerHeight-130);
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight-130);
});
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64).replace("__TESTMODE__", test_mode).replace("__EKSIK__", str(eksik_sayi))
components.html(final_html, height=820, scrolling=False)

if test_mode == "Vida Eksik (Test)":
    st.toast("🎯 İpucu: Büyük yağ kapağının olduğu boşluğa tıkla!", icon="🔍")
