import streamlit as st
import os, shutil
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Oyak Horse")

# static'e kopyala
os.makedirs("static", exist_ok=True)
shutil.copy("motor-v2.glb", "static/motor-v2.glb")

st.markdown("""
<style>
header,footer{visibility:hidden}
.block-container{padding:0!important}
</style>
<div style="background:#0f172a; padding:14px; text-align:center; color:white; font-family:sans-serif;">
  <b>Oyak Horse Görme Testi</b> - 19.64 MB motor yüklendi ✅
</div>
""", unsafe_allow_html=True)

html = '''
<canvas id="c" style="width:100%; height:750px; display:block; background:#1e293b;"></canvas>
<div id="log" style="position:absolute; top:60px; left:10px; color:#94a3b8; font-family:monospace; font-size:12px; background:rgba(0,0,0,0.6); padding:8px; border-radius:6px;"></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const log = (m)=>{ document.getElementById('log').innerText=m; console.log(m); };
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x1e293b);
const camera=new THREE.PerspectiveCamera(45, window.innerWidth/750, 0.1, 100); camera.position.set(1.2,0.8,1.2);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true}); renderer.setSize(window.innerWidth,750);
const controls=new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true; controls.autoRotateSpeed=0.6;
scene.add(new THREE.AmbientLight(0xffffff,1.8));
let d=new THREE.DirectionalLight(0xffffff,2); d.position.set(5,10,5); scene.add(d);

const loader=new GLTFLoader();
const draco=new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

log('motor-v2.glb yükleniyor... 19.64 MB');
loader.load('app/static/motor-v2.glb', (gltf)=>{
  log('✅ Motor yüklendi! '+Object.keys(gltf).join(','));
  let m=gltf.scene;
  let box=new THREE.Box3().setFromObject(m);
  let center=box.getCenter(new THREE.Vector3());
  m.position.sub(center);
  m.position.y+=0.2;
  let size=box.getSize(new THREE.Vector3()).length();
  m.scale.setScalar(2.2/size);
  scene.add(m);
}, (p)=>{
  if(p.total) log('Yükleniyor: '+(p.loaded/p.total*100).toFixed(1)+'%');
}, (e)=>{
  log('❌ HATA: '+e.message);
  console.error(e);
});

function anim(){ requestAnimationFrame(anim); controls.update(); renderer.render(scene,camera); } anim();
</script>
'''

components.html(html, height=800, scrolling=False)
