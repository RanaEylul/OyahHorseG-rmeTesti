import os, shutil
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

os.makedirs("static", exist_ok=True)
if os.path.exists("motor-v2.glb"):
    shutil.copy("motor-v2.glb", "static/motor-v2.glb")

components.html('''
<canvas id="c" style="width:100%; height:800px; display:block; background:#1e293b;"></canvas>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

const scene=new THREE.Scene(); scene.background=new THREE.Color(0x1e293b);
const camera=new THREE.PerspectiveCamera(45, innerWidth/800, 0.1, 100); camera.position.set(1.3,0.9,1.3);
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('c'), antialias:true}); renderer.setSize(innerWidth,800);
const controls=new OrbitControls(camera, renderer.domElement); controls.enableDamping=true; controls.autoRotate=true; controls.autoRotateSpeed=0.8;
scene.add(new THREE.AmbientLight(0xffffff,2));
let d=new THREE.DirectionalLight(0xffffff,2); d.position.set(5,10,5); scene.add(d);

const loader=new GLTFLoader();
const draco=new DRACOLoader();
draco.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
loader.setDRACOLoader(draco);
loader.load('app/static/motor-v2.glb', (gltf)=>{
  let m=gltf.scene;
  let box=new THREE.Box3().setFromObject(m);
  let c=box.getCenter(new THREE.Vector3()); m.position.sub(c);
  let s=box.getSize(new THREE.Vector3()).length(); m.scale.setScalar(2.2/s);
  scene.add(m);
});
(function loop(){ requestAnimationFrame(loop); controls.update(); renderer.render(scene,camera); })();
</script>
''', height=820, scrolling=False)
