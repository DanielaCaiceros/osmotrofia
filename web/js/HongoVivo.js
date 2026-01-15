/**
 * HongoVivo - Hongo digital con ciclo de vida completo
 *
 * Características:
 * - Nace, crece, se marchita y muere
 * - Evoluciona continuamente según ambiente
 * - Reacciona a nutrientes y condiciones
 * - Se mueve orgánicamente (inclinación, pulsación)
 * - Puede ser bioluminiscente
 */

import * as THREE from 'three';

export class HongoVivo {
    constructor(tipo, posicion, caracteristicas, ambiente) {
        this.tipo = tipo;
        this.posicion = new THREE.Vector3(...posicion);
        this.caracteristicas = caracteristicas;

        // Estado de vida
        this.edad = 0;
        this.energia = 1.0;
        this.estadoVida = 'naciendo'; // naciendo -> vivo -> marchito -> muerto
        this.tiempoEnEstado = 0;

        // Propiedades de crecimiento
        this.escalaActual = 0.1; // Empieza pequeño
        this.escalaObjetivo = caracteristicas.tamano_final || 1.0;
        this.velocidadCrecimiento = 0.5;

        // Variedad de formas (selección aleatoria)
        this.tipoForma = this.seleccionarTipoForma();

        // Forma base con variaciones
        this.formaBase = this.generarFormaVariada(this.tipoForma);

        // Forma actual (evoluciona)
        this.formaActual = { ...this.formaBase };

        // Movimiento orgánico
        this.inclinacion = 0;
        this.rotacionBase = Math.random() * Math.PI * 2;
        this.pulsacionFase = Math.random() * Math.PI * 2;

        // Bioluminiscencia
        this.bioluminiscente = false;
        this.intensidadBrillo = 0;

        // Color con variaciones
        this.color = this.generarColorVariado(caracteristicas.color);
        this.colorOriginal = this.color.clone();

        // Color secundario para degradados
        this.colorSecundario = this.generarColorSecundario(this.color);

        // Patrón de textura (manchas, rayas, etc.)
        this.patronTextura = this.seleccionarPatron();

        // Decoraciones (bolitas, escamas, etc.)
        this.tieneDecoraciones = Math.random() > 0.4; // 60% de probabilidad

        // Crear geometría 3D
        this.grupo = new THREE.Group();
        this.crearGeometria();
        this.grupo.position.copy(this.posicion);

        // Aplicar ambiente inicial
        this.actualizarPorAmbiente(ambiente);
    }

    seleccionarTipoForma() {
        const formas = [
            'redondeado',      // Classic round mushroom
            'plano',           // Flat wide cap
            'conico',          // Pointy cone
            'irregular',       // Asymmetric wild
            'campana',         // Bell shaped
            'parasol',         // Umbrella-like
            'ostra',           // Oyster mushroom fan
            'coral',           // Coral/branch-like
            'bola',            // Puffball sphere
            'seta_china'       // Asian conical hat
        ];
        return formas[Math.floor(Math.random() * formas.length)];
    }

    generarFormaVariada(tipo) {
        switch (tipo) {
            case 'redondeado':
                return {
                    capRadio: 0.8 + Math.random() * 0.4,
                    capAltura: 0.6 + Math.random() * 0.3,
                    stemAltura: 1.2 + Math.random() * 0.8,
                    stemGrosor: 0.25 + Math.random() * 0.15,
                    curvatura: 0.5
                };
            case 'plano':
                return {
                    capRadio: 1.0 + Math.random() * 0.5,
                    capAltura: 0.2 + Math.random() * 0.2,
                    stemAltura: 1.0 + Math.random() * 0.6,
                    stemGrosor: 0.2 + Math.random() * 0.1,
                    curvatura: 0.3
                };
            case 'conico':
                return {
                    capRadio: 0.6 + Math.random() * 0.3,
                    capAltura: 0.8 + Math.random() * 0.5,
                    stemAltura: 1.5 + Math.random() * 1.0,
                    stemGrosor: 0.2 + Math.random() * 0.1,
                    curvatura: 0.8
                };
            case 'irregular':
                return {
                    capRadio: 0.7 + Math.random() * 0.6,
                    capAltura: 0.4 + Math.random() * 0.5,
                    stemAltura: 1.0 + Math.random() * 1.2,
                    stemGrosor: 0.15 + Math.random() * 0.25,
                    curvatura: Math.random()
                };
            case 'campana':
                return {
                    capRadio: 0.8 + Math.random() * 0.4,
                    capAltura: 0.7 + Math.random() * 0.4,
                    stemAltura: 1.8 + Math.random() * 0.8,
                    stemGrosor: 0.15 + Math.random() * 0.1,
                    curvatura: 0.6
                };
            case 'parasol':
                // Very wide, flat, umbrella-like
                return {
                    capRadio: 1.2 + Math.random() * 0.6,
                    capAltura: 0.15 + Math.random() * 0.1,
                    stemAltura: 2.0 + Math.random() * 1.0,
                    stemGrosor: 0.12 + Math.random() * 0.08,
                    curvatura: 0.25
                };
            case 'ostra':
                // Fan/oyster shaped, minimal stem
                return {
                    capRadio: 1.0 + Math.random() * 0.7,
                    capAltura: 0.3 + Math.random() * 0.2,
                    stemAltura: 0.3 + Math.random() * 0.2,
                    stemGrosor: 0.3 + Math.random() * 0.2,
                    curvatura: 0.4
                };
            case 'coral':
                // Multiple branches, unique look
                return {
                    capRadio: 0.5 + Math.random() * 0.3,
                    capAltura: 0.8 + Math.random() * 0.6,
                    stemAltura: 1.0 + Math.random() * 0.8,
                    stemGrosor: 0.25 + Math.random() * 0.15,
                    curvatura: 0.7
                };
            case 'bola':
                // Puffball - spherical
                return {
                    capRadio: 0.8 + Math.random() * 0.5,
                    capAltura: 0.8 + Math.random() * 0.5,
                    stemAltura: 0.2 + Math.random() * 0.1,
                    stemGrosor: 0.4 + Math.random() * 0.2,
                    curvatura: 1.0
                };
            case 'seta_china':
                // Asian conical hat shape
                return {
                    capRadio: 0.9 + Math.random() * 0.4,
                    capAltura: 0.6 + Math.random() * 0.3,
                    stemAltura: 1.4 + Math.random() * 0.7,
                    stemGrosor: 0.18 + Math.random() * 0.12,
                    curvatura: 0.55
                };
            default:
                return {
                    capRadio: 1.0,
                    capAltura: 0.5,
                    stemAltura: 1.5,
                    stemGrosor: 0.3,
                    curvatura: 0.5
                };
        }
    }

    generarColorVariado(colorBase) {
        const baseColor = new THREE.Color(colorBase.r, colorBase.g, colorBase.b);

        // Variación de matiz, saturación y brillo
        const h = { h: 0, s: 0, l: 0 };
        baseColor.getHSL(h);

        // Variar ±15% en matiz, ±20% en saturación, ±15% en brillo
        h.h += (Math.random() - 0.5) * 0.15;
        h.s = Math.max(0, Math.min(1, h.s + (Math.random() - 0.5) * 0.2));
        h.l = Math.max(0.1, Math.min(0.9, h.l + (Math.random() - 0.5) * 0.15));

        return new THREE.Color().setHSL(h.h, h.s, h.l);
    }

    generarColorSecundario(colorPrimario) {
        // Generar color complementario o análogo para degradados
        const h = { h: 0, s: 0, l: 0 };
        colorPrimario.getHSL(h);

        const tipo = Math.random();
        if (tipo < 0.4) {
            // Color más oscuro (degradado vertical)
            h.l = Math.max(0.1, h.l - 0.2 - Math.random() * 0.2);
        } else if (tipo < 0.7) {
            // Color más claro
            h.l = Math.min(0.9, h.l + 0.15 + Math.random() * 0.15);
        } else {
            // Color análogo (matiz cercano)
            h.h = (h.h + (Math.random() - 0.5) * 0.1) % 1;
            h.s = Math.max(0, Math.min(1, h.s + (Math.random() - 0.5) * 0.2));
        }

        return new THREE.Color().setHSL(h.h, h.s, h.l);
    }

    seleccionarPatron() {
        const patrones = ['liso', 'manchas', 'rayas', 'moteado', 'gradiente'];
        return {
            tipo: patrones[Math.floor(Math.random() * patrones.length)],
            intensidad: 0.2 + Math.random() * 0.5
        };
    }

    calcularColorVertice(x, y, z) {
        const baseColor = this.color.clone();
        const patron = this.patronTextura;

        switch (patron.tipo) {
            case 'manchas':
                // Manchas aleatorias usando color secundario
                const manchaNoise = Math.sin(x * 10) * Math.cos(z * 10);
                if (manchaNoise > 0.3) {
                    return baseColor.lerp(this.colorSecundario, 0.5 + Math.random() * 0.3);
                }
                break;

            case 'rayas':
                // Rayas radiales alternando colores
                const angulo = Math.atan2(z, x);
                const rayaNoise = Math.sin(angulo * 8);
                if (rayaNoise > 0) {
                    return this.colorSecundario.clone();
                }
                break;

            case 'moteado':
                // Puntos aleatorios con color secundario
                if (Math.random() > 0.7) {
                    return this.colorSecundario.clone().multiplyScalar(0.9 + Math.random() * 0.2);
                }
                break;

            case 'gradiente':
                // Degradado vertical de color primario a secundario
                const factorGrad = Math.abs(y) / this.formaBase.capAltura;
                return baseColor.clone().lerp(this.colorSecundario, factorGrad);

            case 'liso':
            default:
                // Color con leve variación hacia secundario
                const lerpFactor = Math.random() * 0.15;
                return baseColor.lerp(this.colorSecundario, lerpFactor);
        }

        return baseColor;
    }

    agregarDecoraciones() {
        // Número de decoraciones según tamaño del cap
        const numDecoraciones = Math.floor(5 + Math.random() * 15);
        const tipoDecoracion = Math.random();

        for (let i = 0; i < numDecoraciones; i++) {
            let decoracion;

            if (tipoDecoracion < 0.5) {
                // Bolitas pequeñas
                const tamano = 0.05 + Math.random() * 0.08;
                const geoDecor = new THREE.SphereGeometry(tamano, 8, 8);
                const matDecor = new THREE.MeshStandardMaterial({
                    color: this.colorSecundario.clone().multiplyScalar(1.2),
                    roughness: 0.4,
                    metalness: 0.1
                });
                decoracion = new THREE.Mesh(geoDecor, matDecor);
            } else {
                // Escamas/picos pequeños
                const tamano = 0.04 + Math.random() * 0.06;
                const geoDecor = new THREE.ConeGeometry(tamano, tamano * 2, 6);
                const matDecor = new THREE.MeshStandardMaterial({
                    color: this.color.clone().multiplyScalar(0.7),
                    roughness: 0.8
                });
                decoracion = new THREE.Mesh(geoDecor, matDecor);
            }

            // Posicionar aleatoriamente en la superficie del cap
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI * this.formaBase.curvatura;

            const x = this.formaBase.capRadio * Math.sin(phi) * Math.cos(theta);
            const y = this.formaBase.capRadio * Math.cos(phi) * 0.5;
            const z = this.formaBase.capRadio * Math.sin(phi) * Math.sin(theta);

            decoracion.position.set(x, y, z);
            decoracion.lookAt(x * 2, y * 2, z * 2); // Orientar hacia afuera

            this.cap.add(decoracion);
        }
    }

    crearGeometria() {
        // CAP (sombrero del hongo) - forma según tipo
        const capGeometry = new THREE.SphereGeometry(
            this.formaBase.capRadio,
            32,
            16,
            0,
            Math.PI * 2,
            0,
            Math.PI * this.formaBase.curvatura
        );

        // Deformar para hacerlo más orgánico + aplicar patrón
        const positions = capGeometry.attributes.position;
        const colors = [];

        for (let i = 0; i < positions.count; i++) {
            const x = positions.getX(i);
            const y = positions.getY(i);
            const z = positions.getZ(i);

            // Ruido orgánico
            const noise = (Math.random() - 0.5) * 0.08;
            positions.setY(i, y + noise);

            // Deformación según tipo de forma
            if (this.tipoForma === 'irregular') {
                const noiseX = (Math.random() - 0.5) * 0.1;
                const noiseZ = (Math.random() - 0.5) * 0.1;
                positions.setX(i, x + noiseX);
                positions.setZ(i, z + noiseZ);
            }

            // Colores vertex para patrones
            const vertexColor = this.calcularColorVertice(x, y, z);
            colors.push(vertexColor.r, vertexColor.g, vertexColor.b);
        }

        positions.needsUpdate = true;
        capGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        this.capMaterial = new THREE.MeshStandardMaterial({
            color: this.color,
            roughness: 0.6 + Math.random() * 0.3,
            metalness: 0.05 + Math.random() * 0.15,
            emissive: new THREE.Color(0x000000),
            emissiveIntensity: 0,
            vertexColors: true  // Usar colores de vértices para patrones
        });

        this.cap = new THREE.Mesh(capGeometry, this.capMaterial);
        this.cap.castShadow = true;
        this.cap.receiveShadow = true;

        // STEM (tallo) - con variaciones orgánicas NO CILÍNDRICAS
        const tipoStem = Math.random();
        let stemGeometry;

        if (tipoStem < 0.3) {
            // Tallo que se ensancha en el medio (bulboso)
            stemGeometry = new THREE.CylinderGeometry(
                this.formaBase.stemGrosor * (0.6 + Math.random() * 0.2),
                this.formaBase.stemGrosor * (1.2 + Math.random() * 0.3),
                this.formaBase.stemAltura,
                16
            );
        } else if (tipoStem < 0.6) {
            // Tallo irregular con múltiples segmentos
            stemGeometry = new THREE.CylinderGeometry(
                this.formaBase.stemGrosor * (0.8 + Math.random() * 0.3),
                this.formaBase.stemGrosor * (0.7 + Math.random() * 0.4),
                this.formaBase.stemAltura,
                12
            );
        } else {
            // Tallo cónico suave
            stemGeometry = new THREE.CylinderGeometry(
                this.formaBase.stemGrosor * (0.5 + Math.random() * 0.2),
                this.formaBase.stemGrosor * (1.0 + Math.random() * 0.3),
                this.formaBase.stemAltura,
                16
            );
        }

        // Deformar stem para que no sea perfectamente recto
        const stemPositions = stemGeometry.attributes.position;
        for (let i = 0; i < stemPositions.count; i++) {
            const x = stemPositions.getX(i);
            const y = stemPositions.getY(i);
            const z = stemPositions.getZ(i);

            // Curvatura y bumps orgánicos
            const curvatura = Math.sin(y * 2) * 0.04;
            const bumpX = Math.sin(y * 8 + x * 10) * 0.02;
            const bumpZ = Math.cos(y * 6 + z * 10) * 0.02;

            // Variación radial (hacer el stem no perfectamente redondo)
            const variacionRadial = (Math.random() - 0.5) * 0.15;

            stemPositions.setX(i, x * (1 + variacionRadial) + curvatura + bumpX);
            stemPositions.setZ(i, z * (1 + variacionRadial) + bumpZ);
        }
        stemPositions.needsUpdate = true;

        // Color del stem con variación
        const stemColor = this.color.clone().multiplyScalar(0.6 + Math.random() * 0.2);

        this.stemMaterial = new THREE.MeshStandardMaterial({
            color: stemColor,
            roughness: 0.85 + Math.random() * 0.1,
            metalness: 0.02 + Math.random() * 0.05
        });

        this.stem = new THREE.Mesh(stemGeometry, this.stemMaterial);
        this.stem.castShadow = true;
        this.stem.receiveShadow = true;
        this.stem.position.y = -this.formaBase.capAltura;

        // GILLS (láminas debajo del cap) - con textura variada
        const gillsRadio = this.formaBase.capRadio * (0.92 + Math.random() * 0.06);
        const gillsGeometry = new THREE.CylinderGeometry(
            gillsRadio,
            gillsRadio,
            0.08 + Math.random() * 0.04,
            32
        );

        // Color de gills más oscuro y variado
        const gillsColor = this.color.clone().multiplyScalar(0.4 + Math.random() * 0.2);

        this.gillsMaterial = new THREE.MeshStandardMaterial({
            color: gillsColor,
            roughness: 0.95 + Math.random() * 0.05,
            side: THREE.DoubleSide
        });

        this.gills = new THREE.Mesh(gillsGeometry, this.gillsMaterial);
        this.gills.position.y = -this.formaBase.capAltura * (0.4 + Math.random() * 0.2);

        // Decoraciones en el cap (bolitas, escamas, verrugas)
        if (this.tieneDecoraciones) {
            this.agregarDecoraciones();
        }

        // Ensamblar
        this.cap.add(this.gills);
        this.grupo.add(this.cap);
        this.grupo.add(this.stem);

        // Luz de bioluminiscencia (inicialmente apagada)
        this.luz = new THREE.PointLight(this.color, 0, 3);
        this.luz.position.y = this.formaBase.capAltura;
        this.grupo.add(this.luz);

        // Escala inicial pequeña
        this.grupo.scale.setScalar(this.escalaActual);
    }

    evolucionar(deltaTime, ambiente) {
        // ⚠️ SI ESTÁ MUERTO Y LISTO PARA RECICLAR, NO HACER NADA
        if (this.estadoVida === 'muerto' && this.tiempoEnEstado > 3.0) {
            return; // Ya no evolucionar, solo esperar reciclaje
        }

        this.edad += deltaTime;
        this.tiempoEnEstado += deltaTime;

        // Máquina de estados de vida
        switch (this.estadoVida) {
            case 'naciendo':
                this.estadoNaciendo(deltaTime);
                break;
            case 'vivo':
                this.estadoVivo(deltaTime, ambiente);
                break;
            case 'marchito':
                this.estadoMarchito(deltaTime);
                break;
            case 'muerto':
                this.estadoMuerto(deltaTime);
                break;
        }

        // Actualizar visual
        this.actualizarVisual(deltaTime);
    }

    estadoNaciendo(dt) {
        // Crecer desde pequeño
        this.escalaActual += this.velocidadCrecimiento * dt * 0.3;
        this.energia = Math.min(1.0, this.energia + dt * 0.2);

        if (this.escalaActual >= this.escalaObjetivo * 0.8) {
            this.estadoVida = 'vivo';
            this.tiempoEnEstado = 0;
        }
    }

    estadoVivo(dt, ambiente) {
        // Crecimiento orgánico lento
        if (this.escalaActual < this.escalaObjetivo) {
            this.escalaActual += this.velocidadCrecimiento * dt * 0.1;
        }

        // Energía se ve afectada por ambiente
        let deltaEnergia = 0;

        // Temperatura
        if (ambiente.temperatura.estado === 'extremo') {
            deltaEnergia -= dt * 0.05; // Pierde energía con calor extremo
        } else if (ambiente.temperatura.estado === 'optimo') {
            deltaEnergia += dt * 0.02; // Gana energía en óptimo
        }

        // Humedad (batería)
        if (ambiente.humedad.humedad < 0.3) {
            deltaEnergia -= dt * 0.03; // Pierde energía con poca batería
        }

        // RAM (absorción)
        if (ambiente.ram.absorcion === 'critica') {
            deltaEnergia -= dt * 0.04; // Sin RAM, no puede alimentarse
        }

        this.energia = Math.max(0, Math.min(1.0, this.energia + deltaEnergia));

        // Transición a marchito si energía baja
        if (this.energia < 0.3) {
            this.estadoVida = 'marchito';
            this.tiempoEnEstado = 0;
        }

        // Movimiento orgánico vivo
        this.velocidadCrecimiento = 0.5 * this.energia;
    }

    estadoMarchito(dt) {
        // Pierde energía rápido
        this.energia = Math.max(0, this.energia - dt * 0.1);

        // Se encoge lentamente
        this.escalaObjetivo *= 0.99;

        // Color se apaga
        this.color.lerp(new THREE.Color(0.3, 0.2, 0.1), dt * 0.1);

        // Si energía llega a 0, muere
        if (this.energia <= 0.05) {
            this.estadoVida = 'muerto';
            this.tiempoEnEstado = 0;
        }
    }

    estadoMuerto(dt) {
        // Colapsa (escala Y se reduce)
        this.escalaActual *= 0.95;

        // Marca para reciclaje después de 3 segundos
        if (this.tiempoEnEstado > 3.0) {
            this.marcarParaReciclaje = true;
        }
    }

    actualizarVisual(dt) {
        // Escala con interpolación suave
        const escalaTarget = new THREE.Vector3(
            this.escalaActual,
            this.escalaActual * (this.estadoVida === 'muerto' ? 0.3 : 1.0),
            this.escalaActual
        );
        this.grupo.scale.lerp(escalaTarget, dt * 2);

        // Pulsación (respiración)
        if (this.estadoVida === 'vivo') {
            const pulsacion = Math.sin(this.edad * 2 + this.pulsacionFase) * 0.02;
            this.cap.scale.setScalar(1 + pulsacion);
        }

        // Inclinación orgánica
        if (this.estadoVida === 'vivo' || this.estadoVida === 'marchito') {
            const factorMarchito = this.estadoVida === 'marchito' ? 2.0 : 1.0;
            this.inclinacion = Math.sin(this.edad * 0.5) * 0.1 * (1 - this.energia) * factorMarchito;
            this.grupo.rotation.z = this.inclinacion;
        }

        // Rotación lenta
        this.grupo.rotation.y = this.rotacionBase + this.edad * 0.05;

        // Actualizar colores
        this.capMaterial.color.copy(this.color);
        this.stemMaterial.color.copy(this.color).multiplyScalar(0.7);

        // Bioluminiscencia
        if (this.bioluminiscente && this.estadoVida === 'vivo') {
            const brillo = (Math.sin(this.edad * 3) * 0.5 + 0.5) * this.intensidadBrillo;
            this.capMaterial.emissive.copy(this.colorOriginal);
            this.capMaterial.emissiveIntensity = brillo * 0.5;
            this.luz.intensity = brillo * 2;
            this.luz.distance = 3 + brillo * 2;
        } else {
            this.capMaterial.emissiveIntensity = 0;
            this.luz.intensity = 0;
        }

        // Humedad (brillo especular)
        // Más batería = más brillo
    }

    actualizarPorAmbiente(ambiente) {
        // Aplicar efectos del ambiente
        if (!ambiente) return;

        // Velocidad de crecimiento por temperatura
        if (ambiente.temperatura) {
            this.velocidadCrecimiento = ambiente.temperatura.velocidad_crecimiento || 0.5;
        }

        // Brillo por humedad
        if (ambiente.humedad) {
            this.capMaterial.roughness = 0.9 - (ambiente.humedad.brillo * 0.4);
            this.stemMaterial.roughness = 0.95 - (ambiente.humedad.brillo * 0.2);
        }

        // Grosor del stem por RAM
        if (ambiente.ram) {
            const factorRAM = ambiente.ram.densidad_micelio || 1.0;
            this.stem.scale.x = factorRAM;
            this.stem.scale.z = factorRAM;
        }
    }

    activarBioluminiscencia(intensidad = 0.8) {
        this.bioluminiscente = true;
        this.intensidadBrillo = intensidad;
    }

    desactivarBioluminiscencia() {
        this.bioluminiscente = false;
        this.intensidadBrillo = 0;
    }

    obtenerEstado() {
        return {
            tipo: this.tipo,
            estadoVida: this.estadoVida,
            edad: this.edad,
            energia: this.energia,
            escala: this.escalaActual,
            bioluminiscente: this.bioluminiscente
        };
    }

    destruir() {
        this.grupo.traverse((obj) => {
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) {
                if (Array.isArray(obj.material)) {
                    obj.material.forEach(mat => mat.dispose());
                } else {
                    obj.material.dispose();
                }
            }
        });
    }
}
