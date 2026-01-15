/**
 * ColoniaViva - Gestiona el ecosistema completo de hongos
 *
 * Características:
 * - Crea y destruye hongos según datos
 * - Recicla hongos muertos
 * - Distribuye bioluminiscencia
 * - Calcula estadísticas en tiempo real
 */

import * as THREE from 'three';
import { HongoVivo } from './HongoVivo.js';

export class ColoniaViva {
    constructor(scene, radioColonia = 12) {
        this.scene = scene;
        this.radioColonia = radioColonia;
        this.hongos = [];
        this.ambiente = null;
        this.datosActuales = null;

        // LÍMITE MÁXIMO DE HONGOS (para performance y visibilidad)
        this.MAX_HONGOS = 35;

        // Red de micelio entre hongos
        this.redMicelio = null;

        // Crear sustrato (suelo)
        this.crearSustrato();
    }

    crearSustrato() {
        // Sustrato casi invisible, solo para sombras
        const sustratoGeometry = new THREE.CircleGeometry(this.radioColonia * 2, 64);
        const sustratoMaterial = new THREE.MeshStandardMaterial({
            color: 0x050505,
            roughness: 1.0,
            metalness: 0.0,
            transparent: true,
            opacity: 0.1
        });

        this.sustrato = new THREE.Mesh(sustratoGeometry, sustratoMaterial);
        this.sustrato.rotation.x = -Math.PI / 2;
        this.sustrato.position.y = -0.5; // Bajar el sustrato para que los tallos conecten bien
        this.sustrato.receiveShadow = true;
        this.scene.add(this.sustrato);

        // Micelio orgánico como puntos brillantes
        const puntosGeometry = new THREE.BufferGeometry();
        const puntosPositions = [];
        const puntosColors = [];

        for (let i = 0; i < 800; i++) {
            const angulo = Math.random() * Math.PI * 2;
            const radio = Math.random() * this.radioColonia * 1.8;
            const x = Math.cos(angulo) * radio;
            const z = Math.sin(angulo) * radio;
            puntosPositions.push(x, Math.random() * 0.05, z);

            // Colores sutiles de micelio
            const brightness = 0.1 + Math.random() * 0.2;
            puntosColors.push(brightness, brightness * 0.8, brightness * 0.6);
        }

        puntosGeometry.setAttribute('position', new THREE.Float32BufferAttribute(puntosPositions, 3));
        puntosGeometry.setAttribute('color', new THREE.Float32BufferAttribute(puntosColors, 3));

        const puntosMaterial = new THREE.PointsMaterial({
            size: 0.03,
            transparent: true,
            opacity: 0.4,
            vertexColors: true,
            sizeAttenuation: true
        });

        this.puntos = new THREE.Points(puntosGeometry, puntosMaterial);
        this.puntos.position.y = -0.5; // Alinear con el sustrato
        this.scene.add(this.puntos);
    }

    actualizarConDatos(datos) {
        this.datosActuales = datos;
        this.ambiente = datos.ambiente;

        // Calcular cuántos hongos deberíamos tener de cada tipo
        const hongosDeseados = this.calcularHongosDeseados(datos.nutrientes);

        // Ajustar colonia
        this.ajustarColonia(hongosDeseados, datos);

        // Actualizar bioluminiscencia
        this.actualizarBioluminiscencia(datos.bioluminiscencia);

        // Actualizar ambiente de hongos existentes
        this.hongos.forEach(hongo => {
            hongo.actualizarPorAmbiente(this.ambiente);
        });
    }

    calcularHongosDeseados(nutrientes) {
        const deseados = {};

        nutrientes.forEach(nutriente => {
            const tipo = nutriente.tipo;
            const cantidad = nutriente.cantidad;
            // Reducir factor: 1 hongo por cada 50 emails (antes era 10)
            const numHongos = Math.max(1, Math.floor(cantidad / 50));

            deseados[tipo] = (deseados[tipo] || 0) + numHongos;
        });

        // LIMITAR TOTAL A MAX_HONGOS
        let totalDeseado = Object.values(deseados).reduce((a, b) => a + b, 0);

        if (totalDeseado > this.MAX_HONGOS) {
            // Escalar proporcionalmente
            const factor = this.MAX_HONGOS / totalDeseado;
            for (const tipo in deseados) {
                deseados[tipo] = Math.max(1, Math.floor(deseados[tipo] * factor));
            }
        }

        return deseados;
    }

    ajustarColonia(hongosDeseados, datos) {
        // Contar hongos actuales por tipo
        const hongosActuales = {};
        this.hongos.forEach(hongo => {
            if (hongo.estadoVida !== 'muerto') {
                hongosActuales[hongo.tipo] = (hongosActuales[hongo.tipo] || 0) + 1;
            }
        });

        // Verificar límite total antes de crear
        const totalActual = this.hongos.filter(h => h.estadoVida !== 'muerto').length;

        if (totalActual >= this.MAX_HONGOS) {
            console.log(`⚠️  Límite de ${this.MAX_HONGOS} hongos alcanzado`);
            return; // No crear más hongos
        }

        // Crear nuevos hongos si faltan
        for (const tipo in hongosDeseados) {
            const actual = hongosActuales[tipo] || 0;
            const deseado = hongosDeseados[tipo];
            const diferencia = deseado - actual;

            if (diferencia > 0) {
                // Crear nuevos hongos
                for (let i = 0; i < diferencia; i++) {
                    // Verificar límite antes de cada creación
                    if (this.hongos.length >= this.MAX_HONGOS) {
                        console.log(`⚠️  Límite alcanzado, deteniendo creación`);
                        return;
                    }
                    this.crearHongo(tipo, datos);
                }
            }
        }

        // Los hongos que sobran se marchitarán naturalmente
        // No los matamos instantáneamente, dejarlos evolucionar
    }

    crearHongo(tipo, datos) {
        // Buscar características del tipo
        const nutriente = datos.nutrientes.find(n => n.tipo === tipo);
        if (!nutriente) return;

        const caracteristicas = nutriente.caracteristicas;

        // Calcular posición basada en patrón de disco
        const posicion = this.calcularPosicion(tipo, datos.ambiente.disco);

        // Crear hongo
        const hongo = new HongoVivo(
            tipo,
            posicion,
            caracteristicas,
            this.ambiente
        );

        this.hongos.push(hongo);
        this.scene.add(hongo.grupo);
    }

    calcularPosicion(tipo, discoInfo) {
        const patron = discoInfo?.patron || 'agrupado';
        const minDistancia = 0.8; // Distancia mínima entre hongos
        const maxIntentos = 30;

        let posicionValida = null;
        let intentos = 0;

        while (!posicionValida && intentos < maxIntentos) {
            let radio, angulo;

            switch (patron) {
                case 'circulo_de_hadas':
                    // Distribución en anillo
                    angulo = Math.random() * Math.PI * 2;
                    radio = this.radioColonia * (0.6 + Math.random() * 0.4);
                    break;

                case 'agrupado':
                    // Distribución compacta
                    angulo = Math.random() * Math.PI * 2;
                    radio = this.radioColonia * Math.random() * 0.5;
                    break;

                case 'apretado':
                    // Muy cerca del centro
                    angulo = Math.random() * Math.PI * 2;
                    radio = this.radioColonia * Math.random() * 0.3;
                    break;

                default:
                    // Distribución aleatoria
                    angulo = Math.random() * Math.PI * 2;
                    radio = this.radioColonia * Math.random();
            }

            const x = Math.cos(angulo) * radio;
            const z = Math.sin(angulo) * radio;

            // Ajustar según tipo (importantes al centro, spam en periferia)
            let factorPosicion = 1.0;
            if (tipo === 'importante') {
                factorPosicion = 0.6;
            } else if (tipo === 'spam') {
                factorPosicion = 1.3;
            }

            const posicionCandidato = [x * factorPosicion, 0, z * factorPosicion];

            // Verificar colisión con hongos existentes
            let hayColision = false;
            for (const hongo of this.hongos) {
                const dx = posicionCandidato[0] - hongo.posicion.x;
                const dz = posicionCandidato[2] - hongo.posicion.z;
                const distancia = Math.sqrt(dx * dx + dz * dz);

                if (distancia < minDistancia) {
                    hayColision = true;
                    break;
                }
            }

            if (!hayColision) {
                posicionValida = posicionCandidato;
            }

            intentos++;
        }

        // Si no encontramos posición válida, usar la última candidata
        return posicionValida || [Math.random() * 2 - 1, 0, Math.random() * 2 - 1];
    }

    actualizarBioluminiscencia(bioInfo) {
        if (!bioInfo || !bioInfo.activa) {
            // Desactivar todos
            this.hongos.forEach(h => h.desactivarBioluminiscencia());
            return;
        }

        const porcentaje = bioInfo.porcentaje_hongos || 0.3;
        const intensidad = bioInfo.intensidad || 0.8;

        // Seleccionar hongos al azar para que brillen
        const hongosVivos = this.hongos.filter(h => h.estadoVida === 'vivo');
        const numBrillantes = Math.floor(hongosVivos.length * porcentaje);

        // Desactivar todos primero
        hongosVivos.forEach(h => h.desactivarBioluminiscencia());

        // Activar algunos al azar
        const seleccionados = this.seleccionarAleatorios(hongosVivos, numBrillantes);
        seleccionados.forEach(h => h.activarBioluminiscencia(intensidad));
    }

    seleccionarAleatorios(array, n) {
        const resultado = [];
        const copia = [...array];

        for (let i = 0; i < Math.min(n, copia.length); i++) {
            const index = Math.floor(Math.random() * copia.length);
            resultado.push(copia[index]);
            copia.splice(index, 1);
        }

        return resultado;
    }

    evolucionar(deltaTime) {
        // Evolucionar cada hongo
        this.hongos.forEach(hongo => {
            hongo.evolucionar(deltaTime, this.ambiente);
        });

        // Actualizar red de micelio entre hongos vivos
        this.actualizarRedMicelio();

        // Reciclar hongos muertos
        this.reciclarHongosMuertos();
    }

    actualizarRedMicelio() {
        // Remover red anterior
        if (this.redMicelio) {
            this.scene.remove(this.redMicelio);
            this.redMicelio.geometry.dispose();
            this.redMicelio.material.dispose();
        }

        // Obtener TODOS los hongos (vivos, marchitos, muertos)
        // Para mantener las conexiones incluso después de la muerte
        const todosHongos = this.hongos;

        if (todosHongos.length < 2) {
            return; // Necesitamos al menos 2 hongos para conectar
        }

        const positions = [];
        const colors = [];

        // Conectar hongos cercanos (máximo 3 conexiones por hongo)
        todosHongos.forEach((hongo, i) => {
            const pos1 = hongo.posicion;
            let conexiones = 0;

            // Buscar los 3 hongos más cercanos
            const distancias = todosHongos
                .map((h, idx) => ({
                    hongo: h,
                    dist: pos1.distanceTo(h.posicion),
                    idx: idx
                }))
                .filter(d => d.idx !== i) // No conectar consigo mismo
                .sort((a, b) => a.dist - b.dist)
                .slice(0, 3); // Solo los 3 más cercanos

            distancias.forEach(({ hongo: hongo2, dist }) => {
                if (dist < this.radioColonia && conexiones < 3) {
                    const pos2 = hongo2.posicion;

                    // Línea base al nivel del suelo (-0.4 para que esté bajo tierra)
                    positions.push(pos1.x, -0.4, pos1.z);
                    positions.push(pos2.x, -0.4, pos2.z);

                    // Color del micelio - mezcla de ambos hongos, semi-transparente
                    const color1 = hongo.colorOriginal;
                    const color2 = hongo2.colorOriginal;
                    const mixColor = color1.clone().lerp(color2, 0.5).multiplyScalar(0.5);

                    colors.push(mixColor.r, mixColor.g, mixColor.b);
                    colors.push(mixColor.r, mixColor.g, mixColor.b);

                    conexiones++;
                }
            });
        });

        if (positions.length === 0) return;

        // Crear geometría de líneas
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const material = new THREE.LineBasicMaterial({
            vertexColors: true,
            transparent: true,
            opacity: 0.4,
            linewidth: 2
        });

        this.redMicelio = new THREE.LineSegments(geometry, material);
        this.scene.add(this.redMicelio);
    }

    reciclarHongosMuertos() {
        const parasReciclar = this.hongos.filter(h => h.marcarParaReciclaje);

        parasReciclar.forEach(hongo => {
            // Remover de la escena
            this.scene.remove(hongo.grupo);
            hongo.destruir();

            // Remover del array
            const index = this.hongos.indexOf(hongo);
            if (index > -1) {
                this.hongos.splice(index, 1);
            }
        });

        if (parasReciclar.length > 0) {
            console.log(`♻️  Reciclados ${parasReciclar.length} hongos muertos`);
        }
    }

    obtenerEstadisticas() {
        const stats = {
            total: this.hongos.length,
            vivos: 0,
            marchitos: 0,
            muertos: 0,
            brillantes: 0,
            porTipo: {}
        };

        this.hongos.forEach(hongo => {
            const estado = hongo.obtenerEstado();

            // Contar por estado
            if (estado.estadoVida === 'vivo' || estado.estadoVida === 'naciendo') {
                stats.vivos++;
            } else if (estado.estadoVida === 'marchito') {
                stats.marchitos++;
            } else if (estado.estadoVida === 'muerto') {
                stats.muertos++;
            }

            // Contar brillantes
            if (estado.bioluminiscente) {
                stats.brillantes++;
            }

            // Contar por tipo
            stats.porTipo[estado.tipo] = (stats.porTipo[estado.tipo] || 0) + 1;
        });

        return stats;
    }

    limpiar() {
        this.hongos.forEach(hongo => {
            this.scene.remove(hongo.grupo);
            hongo.destruir();
        });
        this.hongos = [];

        // Limpiar red de micelio
        if (this.redMicelio) {
            this.scene.remove(this.redMicelio);
            this.redMicelio.geometry.dispose();
            this.redMicelio.material.dispose();
            this.redMicelio = null;
        }
    }

    resetear() {
        this.limpiar();
        console.log('🔄 Colonia reseteada');
    }
}
