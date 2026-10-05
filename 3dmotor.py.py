import streamlit as st
import os, shutil
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Oyak Horse - 3D Motor")

if not os.path.exists("motor-v2.glb"):
    st.error("motor-v2.glb yok")
    st.write(os.listdir("."))
    st.stop()

os.makedirs("static", exist_ok=True)
shutil.copy("motor-v2.glb", "static/motor-v2.glb")

html_code = '''
<div id="status" style="color:white; background:#0f172a; padding:10px; text-align:center;">Yukleniyor...</div>
<canvas id="c" style="width:100%; height:700px; background:#1e293b; display:block;"></canvas>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const status = document.getElementById('status');
const scene = new THREE.Scene(); scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(45, 800/700, 0.1, 100); camera.position.set(1.5,1,1.5);
const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true}); renderer.setSize(800,700);
const controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true;
scene.add(new THREE.AmbientLight(0xffffff,2));
let d=new THREE.DirectionalLight(0xffffff,2); d.position.set(5,10,5); scene.add(d);

const loader = new GLTFLoader();
const draco = new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);

loader.load('app/static/motor-v2.glb',
  (gltf)=>{
    status.innerText='Yuklendi!';
    let m=gltf.scene; let box=new THREE.Box3().setFromObject(m); let c=box.getCenter(new THREE.Vector3()); m.position.sub(c); let s=box.getSize(new THREE.Vector3()).length(); m.scale.setScalar(2/s);
    scene.add(m);
  },
  (p)=>{ if(p.total) status.innerText='Yukleniyor %'+(p.loaded/p.total*100).toFixed(0); },
  (e)=>{ status.innerText='Hata: '+e.message; console.error(e); }
);

function anim(){ requestAnimationFrame(anim); controls.update(); renderer.render(scene,camera); } anim();
</script>
'''

components.html(html_code, height=760)
