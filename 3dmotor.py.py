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

st.markdown("""
<div style="margin:0; padding:18px 24px 14px 24px; background: rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); text-align:center;">
  <h1 style="margin:0; color:#f8fafc; font-weight:800; font-size:26px;">Oyak Horse Görme Testi Uygulaması</h1>
  <p style="margin:6px 0 0 0; color:#94a3b8; font-size:13px;">İnteraktif 3D Motor İnceleme</p>
</div>
<div style="text-align:center; padding:8px; background: rgba(0,0,0,0.2); color:#fbbf24; font-size:12px; font-weight:600;">
  🎯 TEST MODU: Yağ kapağının olduğu ÜST BOŞLUĞA TIKLA - Doğru hata bulundu diyecek
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🔧 Ayarlar")
test_mode = st.sidebar.radio("Mod", ["Sağlam Motor", "Vida Eksik (Test)"])
eksik_sayi = st.sidebar.slider("Kaç vida eksik", 1, 6, 2, disabled=(test_mode=="Sağlam Motor"))

POSSIBLE_NAMES = ["motor3.glb", "motor.glb", "engine.glb", "motor-v2.glb"]
glb_b64 = ""
found_name = ""
for name in POSSIBLE_NAMES:
    if os.path.exists(name) and os.path.getsize(name) > 1000:
        with open(name, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()
        found_name = name
        break

if not glb_b64:
    st.warning("GLB bulunamadı, klasöre motor.glb koy")

html_code = """
<!DOCTYPE html>
<html>
<head>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<style>
  html, body {margin:0; padding:0; overflow:hidden; background:#1e293b; width:100%; height:100%; font-family: sans-serif;}
  #c {width:100vw; height:calc(100vh - 120px); display:block;}
  #msgBox {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%) scale(0.8);
    background: #16a34a; color: white; padding: 28px 40px; border-radius: 20px;
    font-size: 24px; font-weight: 900; text-align:center;
    box-shadow: 0 25px 80px rgba(0,0,0,0.6);
    opacity: 0; pointer-events: none; transition: all 0.4s ease;
    z-index: 100; min-width: 320px;
  }
  #msgBox.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  #msgBox.error { background: #dc2626; }
  #debug { position:absolute; top:10px; left:10px; color:#0f0; font-size:11px; background:rgba(0,0,0,0.7); padding:6px 10px; border-radius:6px; z-index:20; }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="msgBox"></div>
<div id="debug">yükleniyor...</div>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const TEST_MODE = "__TESTMODE__";
const EKSIK_SAYI = __EKSIK__;
const debugEl = document.getElementById('debug');
function log(t){ debugEl.innerText = t; console.log(t); }

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(42, window.innerWidth/(window.innerHeight-120), 0.1, 100);
camera.position.set(1.5, 0.9, 1.5);

const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight-120);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; controls.dampingFactor = 0.08;
controls.autoRotate = true; controls.autoRotateSpeed = 0.6;

scene.add(new THREE.AmbientLight(0xffffff, 1.3));
let d1 = new THREE.DirectionalLight(0xffffff, 2.2); d1.position.set(5,10,5); scene.add(d1);
let d2 = new THREE.DirectionalLight(0xffffff, 1.0); d2.position.set(-5,5,-5); scene.add(d2);

const grid = new THREE.GridHelper(6, 12, 0x334155, 0x1e293b);
grid.position.y = -0.8; grid.material.opacity = 0.3; grid.material.transparent = true; scene.add(grid);

const engineGroup = new THREE.Group(); scene.add(engineGroup);

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hotspot = null;
let modelRef = null;
let oilCapMesh = null;
const msgBox = document.getElementById('msgBox');

function showMsg(txt, err=false){
  msgBox.innerHTML = txt;
  msgBox.className = err ? 'error' : '';
  msgBox.classList.add('show');
  setTimeout(()=>msgBox.classList.remove('show'), 4000);
}

log("Mod: " + TEST_MODE);

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
    model.traverse(o=>{ if(o.isMesh) allMeshes.push(o); });
    log("Mesh sayisi: "+allMeshes.length);

    // EN USTTEKI MESH'I BUL (yag kapagi genelde en ustte)
    let topMesh = null;
    let topY = -9999;
    allMeshes.forEach(m=>{
      let b = new THREE.Box3().setFromObject(m);
      let c = b.getCenter(new THREE.Vector3());
      if(c.y > topY){
        topY = c.y;
        topMesh = m;
      }
    });

    // SARI/TURUNCU KAPAGI BULMAYA CALIS
    let yellowCap = null;
    allMeshes.forEach(m=>{
      if(m.material && m.material.color){
        let c = m.material.color;
        // Biraz daha genis tolerans
        if(c.r > 0.6 && c.g > 0.4 && c.b < 0.5){
          let b = new THREE.Box3().setFromObject(m);
          let cen = b.getCenter(new THREE.Vector3());
          let sz = b.getSize(new THREE.Vector3()).length();
          // Buyuk olan yag kapagi, kucuk olan dipstick
          if(sz > 0.08 && cen.y > 0){
            if(!yellowCap || cen.y > new THREE.Box3().setFromObject(yellowCap).getCenter(new THREE.Vector3()).y){
              yellowCap = m;
            }
          }
        }
      }
    });

    oilCapMesh = yellowCap || topMesh;
    if(oilCapMesh) log("Kapak bulundu: "+oilCapMesh.name+" Y:"+topY.toFixed(2));

    // TEST MODU: KAPAGI GIZLE + HOTSPOT EKLE
    if(TEST_MODE.includes("Vida Eksik")){
      // Vida gizle
      allMeshes.sort((a,b)=>{
        let sa = new THREE.Box3().setFromObject(a).getSize(new THREE.Vector3()).length();
        let sb = new THREE.Box3().setFromObject(b).getSize(new THREE.Vector3()).length();
        return sa - sb;
      });
      for(let i=0;i<EKSIK_SAYI && i<allMeshes.length;i++) allMeshes[i].visible = false;

      if(oilCapMesh){
        oilCapMesh.visible = false;
        log("Kapak gizlendi, hotspot olusturuluyor");
      }

      // HOTSPOT - kesin calisan versiyon
      // Kapagin LOCAL pozisyonunu kullan
      let capLocalPos = oilCapMesh ? oilCapMesh.position.clone() : new THREE.Vector3(0, 0.5, 0);
      // Eger cap worldde ise local'e cevirmek yerine, model icinde sabit ust noktaya koy
      // En garanti: modelin en ust noktasina hotspot
      let hotspotPos = new THREE.Vector3();
      if(oilCapMesh){
        // cap'in box center'ini local olarak al
        let b = new THREE.Box3().setFromObject(oilCapMesh);
        let cen = b.getCenter(new THREE.Vector3());
        hotspotPos.copy(oilCapMesh.position); // local pos
        // World center'i kullanmak daha iyi
        // Basit: cap'in parent'inda pos'u al
        hotspotPos.copy(oilCapMesh.position);
      } else {
        hotspotPos.set(0, 0.8, 0);
      }

      // GORUNUR turuncu kure olarak baslat (debug icin 3sn sonra gizlenecek)
      let geo = new THREE.SphereGeometry(0.22, 24, 24);
      let mat = new THREE.MeshStandardMaterial({color: 0xff8800, emissive: 0xff4400, emissiveIntensity: 0.6, transparent:true, opacity:0.9});
      hotspot = new THREE.Mesh(geo, mat);
      hotspot.position.copy(hotspotPos);
      hotspot.userData.isHotspot = true;
      hotspot.renderOrder = 999;
      // cap'in parent'ina ekle
      if(oilCapMesh && oilCapMesh.parent) oilCapMesh.parent.add(hotspot);
      else model.add(hotspot);

      // Ekstra buyuk gorunmez box (tiklamayi kolaylastirir)
      let boxGeo = new THREE.BoxGeometry(0.6, 0.4, 0.6);
      let boxMat = new THREE.MeshBasicMaterial({transparent:true, opacity:0.0});
      let boxHot = new THREE.Mesh(boxGeo, boxMat);
      boxHot.position.copy(hotspotPos);
      boxHot.userData.isHotspot = true;
      if(oilCapMesh && oilCapMesh.parent) oilCapMesh.parent.add(boxHot);
      else model.add(boxHot);

      // 3 saniye sonra turuncuyu gizle (sadece hayalet kalacak)
      setTimeout(()=>{
        mat.opacity = 0.15;
        mat.emissiveIntensity = 0.1;
        log("Hotspot artik hayalet modda - tikla!");
      }, 3000);

      log("Hazir! Turuncu kureye tikla");
    }

    model.traverse(o=>{ if(o.isMesh){ o.castShadow=true; }});
    engineGroup.add(model);
  });
}

// TIKLAMA
let isDragging = false;
let startPos = {x:0,y:0};

renderer.domElement.addEventListener('mousedown', e=>{ isDragging=false; startPos={x:e.clientX,y:e.clientY}; });
renderer.domElement.addEventListener('mousemove', e=>{
  if(Math.abs(e.clientX-startPos.x)>5 || Math.abs(e.clientY-startPos.y)>5) isDragging=true;
});

renderer.domElement.addEventListener('click', (event)=>{
  if(isDragging) return; // surukleme ise tiklama sayma

  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);

  // Oncelikle hotspot
  if(hotspot){
    let hits = raycaster.intersectObject(hotspot, false);
    // Ayrica tum child hotspotlari kontrol et
    if(modelRef){
      let allHits = raycaster.intersectObject(modelRef, true);
      for(let h of allHits){
        if(h.object.userData && h.object.userData.isHotspot){
          hits = [h];
          break;
        }
      }
    }
    if(hits.length>0){
      log("DOGRU YER TIKLANDI");
      showMsg("✅ DOĞRU! HATA BULUNDU!<br><span style='font-size:16px'>Büyük turuncu yağ kapağı eksik</span>", false);
      controls.autoRotate = false;
      // Yesil yap
      hotspot.material.color.set(0x00ff00);
      hotspot.material.opacity = 0.9;
      hotspot.material.emissive.set(0x00ff00);
      setTimeout(()=>{ hotspot.material.opacity = 0.0; }, 1000);
      return;
    }
  }

  // Baska yere tiklandi
  if(modelRef && TEST_MODE.includes("Vida Eksik")){
    let hits = raycaster.intersectObject(modelRef, true);
    if(hits.length>0){
      // Gercekten motorun bir yerine tiklandi ama hotspot degil
      let isHot = hits.some(h=>h.object.userData && h.object.userData.isHotspot);
      if(!isHot){
        showMsg("❌ Burası değil!<br><span style='font-size:14px'>Üstteki turuncu boşluğa tıkla</span>", true);
        log("Yanlis yer");
      }
    }
  }
});

function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
animate();

window.addEventListener('resize', ()=>{
  camera.aspect = window.innerWidth/(window.innerHeight-120);
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight-120);
});
</script>
</body>
</html>
"""

final_html = html_code.replace("__B64__", glb_b64).replace("__TESTMODE__", test_mode).replace("__EKSIK__", str(eksik_sayi))
components.html(final_html, height=820, scrolling=False)
