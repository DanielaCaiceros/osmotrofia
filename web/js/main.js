/**
 * OSMOTROFIA - Main Entry Point
 * Inicializa Three.js y conecta con el backend
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { ColoniaViva } from './ColoniaViva.js';

// Configuración
const CONFIG = {
    backendURL: 'http://localhost:5050',  // ⚠️ ASEGÚRATE QUE COINCIDA CON TU SERVIDOR
    updateInterval: 5000, // 5 segundos
    radioColonia: 12,
    maxHongos: 35  // Máximo de hongos (para performance)
};

// Variables globales
let scene, camera, renderer, controls;
let colonia;
let clock = new THREE.Clock();
let pausado = false;
let datosActuales = null;

// Estado de conexión
let backendConectado = false;

// Inicialización
init();
animate();

// Iniciar actualización de datos después de que todo esté listo
setTimeout(() => {
    iniciarActualizacionDatos();
}, 500);

function init() {
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);
    scene.fog = new THREE.Fog(0x0a0a0a, 20, 50);

    // Camera - Más cerca para ver mejor los hongos
    camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(0, 8, 12);
    camera.lookAt(0, 1, 0);

    // Renderer
    const canvas = document.getElementById('canvas3d');
    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: false
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 3;
    controls.maxDistance = 30;
    controls.maxPolarAngle = Math.PI / 2;
    controls.target.set(0, 1, 0);

    // Luces
    setupLights();

    // Colonia
    colonia = new ColoniaViva(scene, CONFIG.radioColonia);

    // Event listeners
    window.addEventListener('resize', onWindowResize);
    setupUI();

    // Ocultar loading
    setTimeout(() => {
        document.getElementById('loading').classList.add('hidden');
    }, 1000);

    console.log('🍄 OSMOTROFIA inicializado');
}

function setupLights() {
    // Luz ambiente (suave)
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambientLight);

    // Luz direccional principal (simula sol/luna)
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(5, 10, 5);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 50;
    dirLight.shadow.camera.left = -20;
    dirLight.shadow.camera.right = 20;
    dirLight.shadow.camera.top = 20;
    dirLight.shadow.camera.bottom = -20;
    scene.add(dirLight);

    // Luz de relleno
    const fillLight = new THREE.DirectionalLight(0x4444ff, 0.3);
    fillLight.position.set(-5, 5, -5);
    scene.add(fillLight);

    // Luz hemisférica (ambiente natural)
    const hemiLight = new THREE.HemisphereLight(0x88ff88, 0x1a0f08, 0.4);
    scene.add(hemiLight);
}

function animate() {
    requestAnimationFrame(animate);

    if (!pausado) {
        const deltaTime = clock.getDelta();

        // Evolucionar colonia
        if (colonia) {
            colonia.evolucionar(deltaTime);
        }

        // Update controls
        controls.update();

        // Render
        renderer.render(scene, camera);

        // Actualizar stats UI
        actualizarStatsUI();
    }
}

async function iniciarActualizacionDatos() {
    // Primera actualización inmediata
    await actualizarDatos();

    // Luego cada X segundos
    setInterval(actualizarDatos, CONFIG.updateInterval);
}

async function actualizarDatos() {
    try {
        const response = await fetch(`${CONFIG.backendURL}/api/estado`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        datosActuales = await response.json();

        // Actualizar colonia con nuevos datos
        if (colonia) {
            colonia.actualizarConDatos(datosActuales);
        }

        // Actualizar UI con datos del sistema
        actualizarSistemaUI(datosActuales);

        // Marcar como conectado
        if (!backendConectado) {
            backendConectado = true;
            actualizarEstadoConexion(true);
            console.log('✅ Conectado al backend');
        }

    } catch (error) {
        console.error('❌ Error al obtener datos:', error);

        if (backendConectado) {
            backendConectado = false;
            actualizarEstadoConexion(false);
        }
    }
}

function actualizarSistemaUI(datos) {
    if (!datos) return;

    try {
        // Sistema
        const cpuUso = datos.sistema?.cpu?.uso || 0;
        const ramUso = datos.sistema?.ram?.uso || 0;
        const discoUso = datos.sistema?.disco?.uso || 0;
        const tempCpu = datos.sistema?.cpu?.temperatura || 0;
        const bateria = datos.sistema?.bateria?.porcentaje || 0;

        document.getElementById('cpu-uso').textContent = `${cpuUso.toFixed(1)}%`;
        document.getElementById('cpu-bar').style.width = `${cpuUso}%`;

        document.getElementById('ram-uso').textContent = `${ramUso.toFixed(1)}%`;
        document.getElementById('ram-bar').style.width = `${ramUso}%`;

        document.getElementById('disco-uso').textContent = `${discoUso.toFixed(1)}%`;
        document.getElementById('disco-bar').style.width = `${discoUso}%`;

        document.getElementById('temp-cpu').textContent = `${tempCpu.toFixed(1)}°C`;
        document.getElementById('bateria').textContent = `${bateria}%`;

        // Gmail
        document.getElementById('gmail-total').textContent = datos.gmail?.total || 0;
        document.getElementById('gmail-importante').textContent = datos.gmail?.importante || 0;
        document.getElementById('gmail-spam').textContent = datos.gmail?.spam || 0;
        document.getElementById('gmail-noleidos').textContent = datos.gmail?.no_leidos || 0;

        // Salud
        const saludNum = datos.salud?.ecosistema?.salud_numerica || 0;
        document.getElementById('salud-ecosistema').textContent = `${saludNum}%`;

        // Cambiar color de barra según valor
        actualizarColorBarra('cpu-bar', cpuUso);
        actualizarColorBarra('ram-bar', ramUso);
        actualizarColorBarra('disco-bar', discoUso);

        console.log('✅ UI actualizado con datos');
    } catch (error) {
        console.error('Error actualizando UI:', error);
    }
}

function actualizarStatsUI() {
    if (!colonia) return;

    const stats = colonia.obtenerEstadisticas();

    document.getElementById('hongos-vivos').textContent = stats.vivos;
    document.getElementById('hongos-marchitos').textContent = stats.marchitos;
    document.getElementById('hongos-brillantes').textContent = stats.brillantes;
}

function actualizarColorBarra(barId, valor) {
    const barra = document.getElementById(barId);
    if (!barra) return;

    if (valor < 50) {
        barra.style.background = 'linear-gradient(90deg, #88ff88, #44cc44)';
    } else if (valor < 75) {
        barra.style.background = 'linear-gradient(90deg, #ffff88, #cccc44)';
    } else {
        barra.style.background = 'linear-gradient(90deg, #ff8888, #cc4444)';
    }
}

function actualizarEstadoConexion(conectado) {
    const dot = document.getElementById('backend-status');
    const text = document.getElementById('status-text');

    if (conectado) {
        dot.classList.add('connected');
        dot.classList.remove('error');
        text.textContent = 'Conectado';
    } else {
        dot.classList.add('error');
        dot.classList.remove('connected');
        text.textContent = 'Error de conexión';
    }
}

function setupUI() {
    // Botón pausar
    document.getElementById('btn-pausar').addEventListener('click', () => {
        pausado = !pausado;
        const btn = document.getElementById('btn-pausar');
        btn.textContent = pausado ? '▶️ Reanudar' : '⏸️ Pausar';
        console.log(pausado ? '⏸️ Pausado' : '▶️ Reanudado');
    });

    // Botón resetear
    document.getElementById('btn-resetear').addEventListener('click', () => {
        if (confirm('¿Resetear la colonia? Se perderán todos los hongos actuales.')) {
            colonia.resetear();
            // Forzar actualización
            actualizarDatos();
            console.log('🔄 Colonia reseteada');
        }
    });

    // Botón stats
    document.getElementById('btn-stats').addEventListener('click', () => {
        const panel = document.getElementById('stats-panel');
        const btn = document.getElementById('btn-stats');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        btn.classList.toggle('active');
    });
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Exponer para debugging
window.osmotrofia = {
    scene,
    camera,
    colonia,
    pausar: () => { pausado = true; },
    reanudar: () => { pausado = false; },
    datos: () => datosActuales,
    stats: () => colonia?.obtenerEstadisticas()
};

console.log('💡 Tip: Usa window.osmotrofia para debugging');
