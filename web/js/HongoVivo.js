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

    // Simplex-like noise function (sin/cos based, no library needed)
    simpleNoise2D(x, y) {
        return Math.sin(x * 2.1 + Math.cos(y * 1.7)) *
               Math.cos(y * 1.9 + Math.sin(x * 2.3)) * 0.5 + 0.5;
    }

    // Radial noise - affects radius
    radialNoise(angle, t) {
        const n = this.simpleNoise2D(t * Math.cos(angle), t * Math.sin(angle));
        return -Math.abs(n - 0.5) * 0.5;
    }

    // Angular noise - affects rotation
    angularNoise(angle, t) {
        return this.simpleNoise2D(t * Math.cos(angle), t * Math.sin(angle)) * 0.2 - 0.1;
    }

    // Normal noise - affects surface bumps
    normalNoise(angle, t) {
        return this.simpleNoise2D(t * Math.cos(angle) * 3, t * Math.sin(angle) * 3) * t * 0.15;
    }

    agregarDecoraciones() {
        // Número de decoraciones según tamaño del cap
        const numDecoraciones = Math.floor(8 + Math.random() * 20);
        const tipoDecoracion = Math.random();

        for (let i = 0; i < numDecoraciones; i++) {
            // Posición aleatoria en la superficie del cap (parámetros t y angle)
            const t = Math.random() * 0.8; // No hasta el borde
            const angle = Math.random() * Math.PI * 2;

            // Obtener punto en la superficie del cap
            const radius = this.formaBase.capRadio * t;
            const height = this.formaBase.capAltura * (1 - t * 0.7);

            const centerX = Math.cos(angle) * radius;
            const centerY = height;
            const centerZ = Math.sin(angle) * radius;
            const center = new THREE.Vector3(centerX, centerY, centerZ);

            // Normal en ese punto
            const normal = new THREE.Vector3(centerX, height * 0.3, centerZ).normalize();

            let decoracion;

            if (tipoDecoracion < 0.4) {
                // Escamas orgánicas (como en el artículo)
                const scaleRadius = 0.08 + Math.random() * 0.12;
                const numVertices = 8 + Math.floor(Math.random() * 6);
                const scalePositions = [];
                const scaleIndices = [];

                // Centro de la escama
                scalePositions.push(0, 0.02, 0);

                // Vértices alrededor
                for (let j = 0; j < numVertices; j++) {
                    const a = (j / numVertices) * Math.PI * 2;
                    const r = scaleRadius * (0.7 + Math.random() * 0.5);
                    const noiseHeight = this.simpleNoise2D(j, i) * 0.03;

                    scalePositions.push(
                        Math.cos(a) * r,
                        noiseHeight,
                        Math.sin(a) * r
                    );
                }

                // Crear triángulos desde el centro
                for (let j = 0; j < numVertices; j++) {
                    scaleIndices.push(0, j + 1, ((j + 1) % numVertices) + 1);
                }

                const scaleGeo = new THREE.BufferGeometry();
                scaleGeo.setAttribute('position', new THREE.Float32BufferAttribute(scalePositions, 3));
                scaleGeo.setIndex(scaleIndices);
                scaleGeo.computeVertexNormals();

                const scaleMat = new THREE.MeshStandardMaterial({
                    color: this.colorSecundario.clone().multiplyScalar(0.9 + Math.random() * 0.3),
                    roughness: 0.8,
                    side: THREE.DoubleSide
                });

                decoracion = new THREE.Mesh(scaleGeo, scaleMat);
            } else if (tipoDecoracion < 0.7) {
                // Warts/bumps
                const size = 0.04 + Math.random() * 0.06;
                const geoDecor = new THREE.SphereGeometry(size, 6, 6);
                const matDecor = new THREE.MeshStandardMaterial({
                    color: this.colorSecundario.clone().multiplyScalar(1.1),
                    roughness: 0.5
                });
                decoracion = new THREE.Mesh(geoDecor, matDecor);
            } else {
                // Pequeños conos
                const size = 0.03 + Math.random() * 0.05;
                const geoDecor = new THREE.ConeGeometry(size, size * 1.5, 5);
                const matDecor = new THREE.MeshStandardMaterial({
                    color: this.color.clone().multiplyScalar(0.75),
                    roughness: 0.85
                });
                decoracion = new THREE.Mesh(geoDecor, matDecor);
            }

            // Posicionar y orientar hacia la normal
            decoracion.position.copy(center);
            decoracion.lookAt(center.clone().add(normal));

            this.cap.add(decoracion);
        }

        // Anillo en el tallo (ring/annulus) - común en muchos hongos
        if (Math.random() > 0.6 && this.formaBase.stemAltura > 1.0) {
            this.agregarAnillo();
        }
    }

    agregarAnillo() {
        // Ring around the stem
        const ringPos = -this.formaBase.stemAltura * (0.3 + Math.random() * 0.3);
        const ringRadio = this.formaBase.stemGrosor * 1.5;
        const ringGrosor = 0.05 + Math.random() * 0.03;

        const geoRing = new THREE.TorusGeometry(ringRadio, ringGrosor, 8, 16);
        const matRing = new THREE.MeshStandardMaterial({
            color: this.color.clone().multiplyScalar(0.9),
            roughness: 0.7
        });

        const ring = new THREE.Mesh(geoRing, matRing);
        ring.rotation.x = Math.PI / 2;
        ring.position.y = ringPos;

        this.stem.add(ring);
    }

    crearStipeRealista() {
        // Parámetros de resolución
        const vSegments = 30; // segmentos verticales
        const rSegments = 20; // segmentos radiales

        // Crear curva central del stipe (spline con curvatura)
        const curvePoints = [];
        const numCurvePoints = 5;

        for (let i = 0; i < numCurvePoints; i++) {
            const t = i / (numCurvePoints - 1);
            const y = -this.formaBase.stemAltura / 2 + t * this.formaBase.stemAltura;

            // Curvatura del tallo
            const curvX = Math.sin(t * Math.PI * 2) * this.formaBase.stemGrosor * 0.3;
            const curvZ = Math.cos(t * Math.PI * 1.5) * this.formaBase.stemGrosor * 0.2;

            curvePoints.push(new THREE.Vector3(curvX, y, curvZ));
        }

        const stipeCurve = new THREE.CatmullRomCurve3(curvePoints);

        // Función de radio que varía a lo largo del tallo
        const stipeRadius = (t) => {
            // Radio base
            let radius = this.formaBase.stemGrosor;

            // Variación según tipo de forma
            if (this.tipoForma === 'parasol' || this.tipoForma === 'campana') {
                // Más delgado, se adelgaza hacia arriba
                radius *= (1.2 - t * 0.6);
            } else if (this.tipoForma === 'bola') {
                // Muy grueso abajo, fino arriba
                radius *= (1.5 - t * 1.2);
            } else if (this.tipoForma === 'ostra') {
                // Muy corto y grueso
                radius *= 1.3;
            } else {
                // Forma natural: más grueso en la base
                radius *= (1.0 + (1 - t) * 0.4);
            }

            // Añadir noise al radio para hacerlo orgánico
            const noiseVal = this.simpleNoise2D(t * 3, t * 2);
            radius *= (0.9 + noiseVal * 0.3);

            return radius;
        };

        // Crear geometría del stipe
        const positions = [];
        const indices = [];
        const uvs = [];

        // Generar vertices
        for (let i = 0; i <= vSegments; i++) {
            const t = i / vSegments;
            const point = stipeCurve.getPointAt(t);
            const tangent = stipeCurve.getTangentAt(t);
            const radius = stipeRadius(t);

            // Calcular sistema de coordenadas local (Frenet frame)
            const up = new THREE.Vector3(0, 1, 0);
            const normal = new THREE.Vector3();
            normal.crossVectors(up, tangent).normalize();
            const binormal = new THREE.Vector3();
            binormal.crossVectors(tangent, normal).normalize();

            // Crear anillo de vertices
            for (let j = 0; j <= rSegments; j++) {
                const angle = (j / rSegments) * Math.PI * 2;

                // Noise angular para hacer la superficie irregular
                const angNoise = this.angularNoise(angle, t);
                const radNoise = this.radialNoise(angle, t);
                const normNoise = this.normalNoise(angle, t);

                const r = radius * (1 + radNoise * 0.2);
                const a = angle + angNoise;

                // Posición en el anillo
                const ringX = Math.cos(a) * r;
                const ringZ = Math.sin(a) * r;

                // Transformar al espacio 3D usando Frenet frame
                const vertex = new THREE.Vector3();
                vertex.copy(point);
                vertex.add(normal.clone().multiplyScalar(ringX));
                vertex.add(binormal.clone().multiplyScalar(ringZ));

                // Añadir noise normal (bumps en superficie)
                const surfaceNormal = new THREE.Vector3(
                    Math.cos(a),
                    0,
                    Math.sin(a)
                );
                vertex.add(surfaceNormal.multiplyScalar(normNoise * 0.1));

                positions.push(vertex.x, vertex.y, vertex.z);
                uvs.push(j / rSegments, t);
            }
        }

        // Generar indices (caras)
        for (let i = 0; i < vSegments; i++) {
            for (let j = 0; j < rSegments; j++) {
                const a = i * (rSegments + 1) + j;
                const b = a + rSegments + 1;
                const c = a + 1;
                const d = b + 1;

                indices.push(a, b, c);
                indices.push(b, d, c);
            }
        }

        // Crear geometría
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();

        return geometry;
    }

    crearCapRealista() {
        // Parámetros de resolución basados en el artículo
        const rSegments = 30; // segmentos radiales
        const cSegments = 20; // segmentos circulares (ángulo)

        // Crear curva del perfil del cap (spline que define la forma)
        const profilePoints = [];
        const numProfilePoints = 6;

        for (let i = 0; i < numProfilePoints; i++) {
            const t = i / (numProfilePoints - 1);

            // Forma del perfil según tipo de hongo
            let x, y;

            if (this.tipoForma === 'plano') {
                // Cap plano y ancho
                x = t * this.formaBase.capRadio;
                y = this.formaBase.capAltura * (1 - t * t * 0.5);
            } else if (this.tipoForma === 'conico') {
                // Cap cónico puntiagudo
                x = t * this.formaBase.capRadio * (1 - t * 0.3);
                y = this.formaBase.capAltura * (1 - t * 0.8);
            } else if (this.tipoForma === 'campana') {
                // Cap en forma de campana
                x = t * this.formaBase.capRadio * (0.3 + t * 0.7);
                y = this.formaBase.capAltura * (1 - t * 1.2);
            } else if (this.tipoForma === 'bola') {
                // Cap esférico completo
                const angle = t * Math.PI;
                x = Math.sin(angle) * this.formaBase.capRadio;
                y = Math.cos(angle) * this.formaBase.capRadio;
            } else {
                // Forma redondeada clásica
                const angle = t * Math.PI * 0.5;
                x = Math.sin(angle) * this.formaBase.capRadio;
                y = Math.cos(angle) * this.formaBase.capAltura;
            }

            profilePoints.push(new THREE.Vector2(x, y));
        }

        const capCurve = new THREE.SplineCurve(profilePoints);

        // Generar superficie del cap
        const positions = [];
        const indices = [];
        const colors = [];
        const uvs = [];

        // Función para obtener punto en la superficie del cap con noise
        const getCapSurfacePoint = (angle, t) => {
            // Obtener punto base de la curva
            const profilePoint = capCurve.getPointAt(t);
            let x = profilePoint.x;
            let y = profilePoint.y;

            // Aplicar noise radial (afecta el radio)
            const radNoise = this.radialNoise(angle, t);
            const newRadius = x * (1 + radNoise);

            // Aplicar noise angular
            const angNoise = this.angularNoise(angle, t);
            const newAngle = angle + angNoise;

            // Aplicar noise normal (bumps perpendiculares a la superficie)
            const normNoise = this.normalNoise(angle, t);

            // Calcular posición 3D
            const surfacePoint = new THREE.Vector3(
                Math.cos(newAngle) * newRadius,
                y,
                Math.sin(newAngle) * newRadius
            );

            // Calcular tangente de la curva para el noise normal
            const tangent = capCurve.getTangentAt(t);
            const surfaceNormal = new THREE.Vector3(
                Math.cos(newAngle) * tangent.y,
                -tangent.x,
                Math.sin(newAngle) * tangent.y
            ).normalize();

            // Aplicar noise normal
            surfacePoint.add(surfaceNormal.multiplyScalar(normNoise));

            return surfacePoint;
        };

        // Generar vértices
        for (let i = 0; i <= rSegments; i++) {
            const t = i / rSegments;

            for (let j = 0; j <= cSegments; j++) {
                const angle = (j / cSegments) * Math.PI * 2;

                const point = getCapSurfacePoint(angle, t);
                positions.push(point.x, point.y, point.z);

                // Color con degradado
                const vertexColor = this.calcularColorVertice(point.x, point.y, point.z);
                colors.push(vertexColor.r, vertexColor.g, vertexColor.b);

                uvs.push(j / cSegments, t);
            }
        }

        // Generar índices
        for (let i = 0; i < rSegments; i++) {
            for (let j = 0; j < cSegments; j++) {
                const a = i * (cSegments + 1) + j;
                const b = a + cSegments + 1;
                const c = a + 1;
                const d = b + 1;

                indices.push(a, b, c);
                indices.push(b, d, c);
            }
        }

        const capGeometry = new THREE.BufferGeometry();
        capGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        capGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        capGeometry.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
        capGeometry.setIndex(indices);
        capGeometry.computeVertexNormals();

        return capGeometry;
    }

    crearGeometria() {
        // CAP usando spline realista
        const capGeometry = this.crearCapRealista();

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

        // STEM (tallo) - Usando curva spline como en el artículo
        const stemGeometry = this.crearStipeRealista();

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

        // GILLS (láminas debajo del cap) - láminas radiales realistas
        const gillsGrupo = new THREE.Group();
        const numGills = 20 + Math.floor(Math.random() * 20); // 20-40 láminas
        const gillsRadio = this.formaBase.capRadio * 0.95;
        const gillsAltura = 0.15 + Math.random() * 0.1;

        // Color de gills más oscuro y variado
        const gillsColor = this.color.clone().multiplyScalar(0.4 + Math.random() * 0.2);

        for (let i = 0; i < numGills; i++) {
            const angle = (i / numGills) * Math.PI * 2;

            // Cada gill es una lámina fina
            const gillGeometry = new THREE.PlaneGeometry(gillsRadio, gillsAltura, 1, 4);

            // Curvar la lámina ligeramente
            const gillPositions = gillGeometry.attributes.position;
            for (let j = 0; j < gillPositions.count; j++) {
                const x = gillPositions.getX(j);
                const y = gillPositions.getY(j);
                const curve = Math.abs(x / gillsRadio) * 0.05;
                gillPositions.setY(j, y - curve);
            }
            gillPositions.needsUpdate = true;

            const gillMaterial = new THREE.MeshStandardMaterial({
                color: gillsColor,
                roughness: 0.95,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.9
            });

            const gill = new THREE.Mesh(gillGeometry, gillMaterial);
            gill.rotation.y = angle;
            gill.position.y = -gillsAltura / 2;

            gillsGrupo.add(gill);
        }

        this.gills = gillsGrupo;
        this.gills.position.y = -this.formaBase.capAltura * (0.3 + Math.random() * 0.2);

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
