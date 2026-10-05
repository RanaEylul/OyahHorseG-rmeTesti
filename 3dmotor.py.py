html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Three.js GLTF Model Yükleme</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #1a1a1a;
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-family: Arial, sans-serif;
            font-size: 20px;
            pointer-events: none;
        }
    </style>
</head>
<body>

    <div id="loading">Model Yükleniyor...</div>

    <!-- Three.js ve Eklentilerini ES Modülü Olarak Çağrılması -->
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

        let scene, camera, renderer, controls;

        function init() {
            // 1. Sahne (Scene) Oluşturma
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x222222);

            // 2. Kamera (Camera) Oluşturma
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 2, 5);

            // 3. Renderer (Görüntüleyici) Oluşturma
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);

            // 4. Fare Kontrolleri (OrbitControls)
            controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true; // Daha yumuşak hareket için

            // 5. Işıklandırma (Modelin karanlık görünmemesi için çok önemlidir)
            const ambientLight = new THREE.AmbientLight(0xffffff, 1.5); // Genel ortam ışığı
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 2.5); // Güneş ışığı etkisi
            directionalLight.position.set(5, 10, 7);
            scene.add(directionalLight);

            // 6. GLTF Modelini Yükleme
            const loader = new GLTFLoader();
            const loadingElement = document.getElementById('loading');

            // Modelinizin yolunu buraya yazın (Örn: './model.glb' veya GitHub Raw linki)
            loader.load(
                'modelin_adi.glb', // <-- Kendi dosya yolunuzla veya adıyla değiştirin
                function (gltf) {
                    const model = gltf.scene;
                    
                    // Modelin boyutunu veya konumunu ayarlamak isterseniz:
                    // model.scale.set(1, 1, 1);
                    // model.position.set(0, 0, 0);

                    scene.add(model);
                    loadingElement.style.display = 'none'; // Yüklenince yazıyı kaldır
                    console.log('Model başarıyla yüklendi!');
                },
                function (xhr) {
                    // Yükleme ilerleme yüzdesi
                    const percent = (xhr.loaded / xhr.total * 100).toFixed(0);
                    if(!isNaN(percent)) {
                        loadingElement.innerText = `Yükleniyor: %${percent}`;
                    }
                },
                function (error) {
                    console.error('Model yüklenirken hata oluştu:', error);
                    loadingElement.innerText = 'Model yüklenemedi! Konsolu kontrol edin.';
                }
            );

            // Pencere Boyutu Değiştiğinde Tepki Verme
            window.addEventListener('resize', onWindowResize);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            requestAnimationFrame(animate);
            controls.update(); // Kontrollerin dampig özelliğinin çalışması için gerekli
            renderer.render(scene, camera);
        }

        init();
        animate();
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html başarıyla oluşturuldu!")