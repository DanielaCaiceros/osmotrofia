/**
 * AmbienteVivo - Sistema de ambiente dinámico que reacciona a condiciones del sistema
 *
 * Incluye:
 * - Partículas atmosféricas (sporas, polvo, niebla)
 * - Elementos del bosque (rocas, troncos, plantas)
 * - Efectos de iluminación dinámicos
 * - Cambios según temperatura, RAM, batería, etc.
 */

import * as THREE from 'three';

export class AmbienteVivo {
    constructor(scene, radioColonia = 12) {
        this.scene = scene;
        this.radioColonia = radioColonia;
        this.ambiente = null;

        // Sistemas de partículas
        this.particulas = {
            sporas: null,
            niebla: null,
            lluvia: null
        };

        // Elementos decorativos
        this.elementos = {
            rocas: [],
            troncos: [],
            plantas: [],
            raices: []
        };

        // Luces dinámicas
        this.lucesDinamicas = [];

        // Inicializar ambiente
        this.crearElementosEstaticos();
        this.crearSistemasParticulas();
    }

    crearElementosEstaticos() {
        // ROCAS - distribuidas alrededor de la colonia
        const numRocas = 8 + Math.floor(Math.random() * 6);
        for (let i = 0; i < numRocas; i++) {
            const roca = this.crearRoca();
            this.elementos.rocas.push(roca);
            this.scene.add(roca);
        }

        // TRONCOS CAÍDOS - 2-4 troncos
        const numTroncos = 2 + Math.floor(Math.random() * 3);
        for (let i = 0; i < numTroncos; i++) {
            const tronco = this.crearTronco();
            this.elementos.troncos.push(tronco);
            this.scene.add(tronco);
        }

        // RAÍCES EMERGENTES - raíces que salen del suelo
        const numRaices = 10 + Math.floor(Math.random() * 10);
        for (let i = 0; i < numRaices; i++) {
            const raiz = this.crearRaiz();
            this.elementos.raices.push(raiz);
            this.scene.add(raiz);
        }

        // PLANTAS PEQUEÑAS - helechos, musgos
        const numPlantas = 15 + Math.floor(Math.random() * 15);
        for (let i = 0; i < numPlantas; i++) {
            const planta = this.crearPlanta();
            this.elementos.plantas.push(planta);
            this.scene.add(planta);
        }
    }

    crearRoca() {
        const grupo = new THREE.Group();

        // Forma irregular de roca usando esferas deformadas
        const numSegmentos = 3 + Math.floor(Math.random() * 4);
        for (let i = 0; i < numSegmentos; i++) {
            const radio = 0.3 + Math.random() * 0.5;
            const geo = new THREE.SphereGeometry(radio, 8, 6);

            // Deformar para hacerla irregular
            const positions = geo.attributes.position;
            for (let j = 0; j < positions.count; j++) {
                const factor = 0.7 + Math.random() * 0.6;
                positions.setX(j, positions.getX(j) * factor);
                positions.setY(j, positions.getY(j) * factor);
                positions.setZ(j, positions.getZ(j) * factor);
            }
            positions.needsUpdate = true;

            const color = new THREE.Color().setHSL(0.1, 0.1, 0.2 + Math.random() * 0.15);
            const mat = new THREE.MeshStandardMaterial({
                color: color,
                roughness: 0.9,
                metalness: 0.1
            });

            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.set(
                (Math.random() - 0.5) * 0.3,
                (Math.random() - 0.5) * 0.2,
                (Math.random() - 0.5) * 0.3
            );
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            grupo.add(mesh);
        }

        // Posicionar en el perímetro
        const angulo = Math.random() * Math.PI * 2;
        const distancia = this.radioColonia * (0.7 + Math.random() * 0.5);
        grupo.position.set(
            Math.cos(angulo) * distancia,
            -0.4,
            Math.sin(angulo) * distancia
        );
        grupo.rotation.set(
            Math.random() * 0.3,
            Math.random() * Math.PI * 2,
            Math.random() * 0.3
        );

        return grupo;
    }

    crearTronco() {
        const longitud = 2 + Math.random() * 3;
        const radio = 0.2 + Math.random() * 0.15;

        const geo = new THREE.CylinderGeometry(radio, radio * 0.9, longitud, 12);

        // Deformar para hacer más orgánico
        const positions = geo.attributes.position;
        for (let i = 0; i < positions.count; i++) {
            const y = positions.getY(i);
            const noise = (Math.random() - 0.5) * 0.05;
            positions.setX(i, positions.getX(i) + noise);
            positions.setZ(i, positions.getZ(i) + noise);
        }
        positions.needsUpdate = true;

        const color = new THREE.Color().setHSL(0.08, 0.4, 0.15 + Math.random() * 0.1);
        const mat = new THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.95,
            metalness: 0
        });

        const tronco = new THREE.Mesh(geo, mat);
        tronco.castShadow = true;
        tronco.receiveShadow = true;

        // Posicionar caído en el suelo
        const angulo = Math.random() * Math.PI * 2;
        const distancia = this.radioColonia * (0.6 + Math.random() * 0.6);
        tronco.position.set(
            Math.cos(angulo) * distancia,
            -0.3,
            Math.sin(angulo) * distancia
        );
        tronco.rotation.set(
            Math.PI / 2 + (Math.random() - 0.5) * 0.4,
            Math.random() * Math.PI * 2,
            (Math.random() - 0.5) * 0.5
        );

        return tronco;
    }

    crearRaiz() {
        const grupo = new THREE.Group();
        const numSegmentos = 3 + Math.floor(Math.random() * 4);

        let x = 0, y = -0.4, z = 0;

        for (let i = 0; i < numSegmentos; i++) {
            const radio = 0.05 - i * 0.01;
            const altura = 0.3 + Math.random() * 0.4;

            const geo = new THREE.CylinderGeometry(radio, radio * 0.7, altura, 6);
            const color = new THREE.Color().setHSL(0.08, 0.5, 0.1 + Math.random() * 0.1);
            const mat = new THREE.MeshStandardMaterial({
                color: color,
                roughness: 0.9
            });

            const segmento = new THREE.Mesh(geo, mat);
            segmento.position.set(x, y + altura / 2, z);

            const curvatura = (Math.random() - 0.5) * 0.4;
            segmento.rotation.z = curvatura;

            grupo.add(segmento);

            // Calcular siguiente posición
            y += altura * Math.cos(curvatura);
            x += altura * Math.sin(curvatura) * 0.5;
        }

        // Posicionar
        const angulo = Math.random() * Math.PI * 2;
        const distancia = Math.random() * this.radioColonia * 1.2;
        grupo.position.set(
            Math.cos(angulo) * distancia,
            0,
            Math.sin(angulo) * distancia
        );

        return grupo;
    }

    crearPlanta() {
        const grupo = new THREE.Group();
        const tipoPlanta = Math.random();

        if (tipoPlanta < 0.5) {
            // Helecho pequeño
            const numHojas = 3 + Math.floor(Math.random() * 4);
            for (let i = 0; i < numHojas; i++) {
                const geo = new THREE.PlaneGeometry(0.2 + Math.random() * 0.15, 0.4 + Math.random() * 0.3);
                const color = new THREE.Color().setHSL(0.3, 0.5 + Math.random() * 0.3, 0.2 + Math.random() * 0.15);
                const mat = new THREE.MeshStandardMaterial({
                    color: color,
                    side: THREE.DoubleSide,
                    roughness: 0.7,
                    transparent: true,
                    opacity: 0.8
                });

                const hoja = new THREE.Mesh(geo, mat);
                const angulo = (i / numHojas) * Math.PI * 2;
                hoja.position.set(
                    Math.cos(angulo) * 0.1,
                    0.2,
                    Math.sin(angulo) * 0.1
                );
                hoja.rotation.y = angulo;
                hoja.rotation.x = Math.PI / 4;

                grupo.add(hoja);
            }
        } else {
            // Musgo o planta baja
            const geo = new THREE.ConeGeometry(0.15, 0.2, 6);
            const color = new THREE.Color().setHSL(0.25, 0.6, 0.15 + Math.random() * 0.1);
            const mat = new THREE.MeshStandardMaterial({
                color: color,
                roughness: 1.0
            });

            const planta = new THREE.Mesh(geo, mat);
            planta.position.y = 0.1;
            grupo.add(planta);
        }

        // Posicionar
        const angulo = Math.random() * Math.PI * 2;
        const distancia = Math.random() * this.radioColonia * 1.3;
        grupo.position.set(
            Math.cos(angulo) * distancia,
            -0.45,
            Math.sin(angulo) * distancia
        );

        return grupo;
    }

    crearSistemasParticulas() {
        // SPORAS - siempre presentes, flotan en el aire
        this.crearSistemaSporas();

        // NIEBLA - partículas de niebla volumétrica
        this.crearSistemaNiebla();

        // LLUVIA - se activa condicionalmente
        this.crearSistemaLluvia();
    }

    crearSistemaSporas() {
        const numSporas = 200;
        const geo = new THREE.BufferGeometry();
        const positions = [];
        const velocities = [];

        for (let i = 0; i < numSporas; i++) {
            const x = (Math.random() - 0.5) * this.radioColonia * 3;
            const y = Math.random() * 10;
            const z = (Math.random() - 0.5) * this.radioColonia * 3;
            positions.push(x, y, z);

            // Velocidades aleatorias
            velocities.push(
                (Math.random() - 0.5) * 0.1,
                -0.05 - Math.random() * 0.1,
                (Math.random() - 0.5) * 0.1
            );
        }

        geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geo.userData.velocities = velocities;

        const mat = new THREE.PointsMaterial({
            color: 0xaaffaa,
            size: 0.05,
            transparent: true,
            opacity: 0.3,
            sizeAttenuation: true
        });

        this.particulas.sporas = new THREE.Points(geo, mat);
        this.scene.add(this.particulas.sporas);
    }

    crearSistemaNiebla() {
        const numParticulas = 100;
        const geo = new THREE.BufferGeometry();
        const positions = [];

        for (let i = 0; i < numParticulas; i++) {
            const x = (Math.random() - 0.5) * this.radioColonia * 3;
            const y = Math.random() * 2;
            const z = (Math.random() - 0.5) * this.radioColonia * 3;
            positions.push(x, y, z);
        }

        geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        const mat = new THREE.PointsMaterial({
            color: 0x888888,
            size: 0.8,
            transparent: true,
            opacity: 0.15,
            sizeAttenuation: true
        });

        this.particulas.niebla = new THREE.Points(geo, mat);
        this.scene.add(this.particulas.niebla);
    }

    crearSistemaLluvia() {
        const numGotas = 300;
        const geo = new THREE.BufferGeometry();
        const positions = [];

        for (let i = 0; i < numGotas; i++) {
            const x = (Math.random() - 0.5) * this.radioColonia * 3;
            const y = Math.random() * 15;
            const z = (Math.random() - 0.5) * this.radioColonia * 3;
            positions.push(x, y, z);
        }

        geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        const mat = new THREE.PointsMaterial({
            color: 0x4488ff,
            size: 0.08,
            transparent: true,
            opacity: 0.6,
            sizeAttenuation: true
        });

        this.particulas.lluvia = new THREE.Points(geo, mat);
        this.particulas.lluvia.visible = false; // Inicialmente invisible
        this.scene.add(this.particulas.lluvia);
    }

    actualizar(deltaTime, ambiente) {
        if (!ambiente) return;

        this.ambiente = ambiente;

        // Actualizar partículas
        this.actualizarSporas(deltaTime);
        this.actualizarNiebla(deltaTime);
        this.actualizarLluvia(deltaTime, ambiente);

        // Actualizar iluminación según ambiente
        this.actualizarIluminacion(ambiente);

        // Animar plantas con viento
        this.animarPlantas(deltaTime, ambiente);
    }

    actualizarSporas(deltaTime) {
        if (!this.particulas.sporas) return;

        const positions = this.particulas.sporas.geometry.attributes.position.array;
        const velocities = this.particulas.sporas.geometry.userData.velocities;

        for (let i = 0; i < positions.length; i += 3) {
            positions[i] += velocities[i] * deltaTime * 2;
            positions[i + 1] += velocities[i + 1] * deltaTime * 2;
            positions[i + 2] += velocities[i + 2] * deltaTime * 2;

            // Resetear si sale del área
            if (positions[i + 1] < -1) {
                positions[i + 1] = 10;
            }
            if (Math.abs(positions[i]) > this.radioColonia * 2) {
                positions[i] = (Math.random() - 0.5) * this.radioColonia * 3;
            }
            if (Math.abs(positions[i + 2]) > this.radioColonia * 2) {
                positions[i + 2] = (Math.random() - 0.5) * this.radioColonia * 3;
            }
        }

        this.particulas.sporas.geometry.attributes.position.needsUpdate = true;
    }

    actualizarNiebla(deltaTime) {
        if (!this.particulas.niebla) return;

        // Rotar lentamente la niebla
        this.particulas.niebla.rotation.y += deltaTime * 0.05;
    }

    actualizarLluvia(deltaTime, ambiente) {
        if (!this.particulas.lluvia) return;

        // Activar lluvia si temperatura es muy baja o humedad muy alta
        const tempBaja = ambiente.temperatura?.estado === 'frio';
        const humedadAlta = ambiente.humedad?.humedad > 0.7;

        const deberiaLlover = tempBaja || humedadAlta;
        this.particulas.lluvia.visible = deberiaLlover;

        if (deberiaLlover) {
            const positions = this.particulas.lluvia.geometry.attributes.position.array;

            for (let i = 0; i < positions.length; i += 3) {
                positions[i + 1] -= deltaTime * 10; // Caída rápida

                if (positions[i + 1] < -1) {
                    positions[i + 1] = 15;
                    positions[i] = (Math.random() - 0.5) * this.radioColonia * 3;
                    positions[i + 2] = (Math.random() - 0.5) * this.radioColonia * 3;
                }
            }

            this.particulas.lluvia.geometry.attributes.position.needsUpdate = true;
        }
    }

    actualizarIluminacion(ambiente) {
        // Cambiar color de fondo según condiciones
        const temp = ambiente.temperatura?.valor || 50;
        const ram = ambiente.ram?.disponible || 50;

        // Temperatura afecta el tono
        let hue = 0.5; // Azul base
        if (ambiente.temperatura?.estado === 'caliente') {
            hue = 0.05; // Rojizo
        } else if (ambiente.temperatura?.estado === 'frio') {
            hue = 0.6; // Azul frío
        }

        const bgColor = new THREE.Color().setHSL(hue, 0.3, 0.05);
        this.scene.background = bgColor;

        // Actualizar fog
        const fogColor = new THREE.Color().setHSL(hue, 0.2, 0.08);
        if (this.scene.fog) {
            this.scene.fog.color = fogColor;
        }
    }

    animarPlantas(deltaTime, ambiente) {
        // Animar plantas como si hubiera viento
        const tiempo = Date.now() * 0.001;
        const velocidadViento = ambiente.temperatura?.velocidad_crecimiento || 0.5;

        this.elementos.plantas.forEach((planta, i) => {
            const offset = i * 0.5;
            const balanceo = Math.sin(tiempo + offset) * 0.1 * velocidadViento;
            planta.rotation.z = balanceo;
        });

        // Animar raíces sutilmente
        this.elementos.raices.forEach((raiz, i) => {
            const offset = i * 0.3;
            const movimiento = Math.sin(tiempo * 0.5 + offset) * 0.05;
            raiz.rotation.y = movimiento;
        });
    }

    limpiar() {
        // Limpiar partículas
        Object.values(this.particulas).forEach(particula => {
            if (particula) {
                this.scene.remove(particula);
                particula.geometry.dispose();
                particula.material.dispose();
            }
        });

        // Limpiar elementos
        Object.values(this.elementos).forEach(array => {
            array.forEach(elem => {
                this.scene.remove(elem);
                elem.traverse(obj => {
                    if (obj.geometry) obj.geometry.dispose();
                    if (obj.material) obj.material.dispose();
                });
            });
        });
    }
}
