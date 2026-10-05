import streamlit as st
import os, shutil

st.set_page_config(layout="wide")

# static'e kopyala
os.makedirs("static", exist_ok=True)
if os.path.exists("motor-v2.glb"):
    shutil.copy("motor-v2.glb", "static/motor-v2.glb")
    st.write(f"✅ motor-v2.glb {os.path.getsize('motor-v2.glb')/1024/1024:.1f} MB")
else:
    st.error(f"Yok! {os.listdir('.')}")
    st.stop()

html = """
<div id="status" style="color:white; background:#0f172a; padding:10px; text-align:center; font-family:monospace;">Yükleniyor...</div>
<canvas id="c" style="width:100%; height:700px; background:#1e293b;"></canvas>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const status = document.getElementById('status');
function log(m){ status.innerText = m; console.log(m); }

const scene = new THREE.Scene(); scene.background = new THREE.Color(0x1e293b);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/700, 0.1, 100); camera.position.set(1.5,1,1.5);
const renderer = new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true}); renderer.setSize(window.innerWidth,700);
const controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true;
scene.add(new THREE.AmbientLight(0xffffff,2));
let d=new THREE.DirectionalLight(0xffffff,2); d.position.set(5,10,5); scene.add(d);

const loader
