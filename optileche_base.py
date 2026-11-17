import math

# ==========================================
# 🥛 DATASET: OPTILECHE LÉRIDA+
# ==========================================
# Origen: Centro de acopio lechero en Lérida Urbano (0, 0)
ORIGEN = {'id': 0, 'name': 'Centro Acopio (Lérida Urbano)', 'x': 0.0, 'y': 0.0, 'weight': 0.0, 'value': 0.0}

veredas_lerida = [
    {'id': 1, 'name': 'Vereda La Sierra', 'x': 2.0, 'y': 3.0, 'weight': 4.0, 'value': 45.0},
    {'id': 2, 'name': 'Vereda El Delirio', 'x': 5.0, 'y': 8.0, 'weight': 6.0, 'value': 70.0},
    {'id': 3, 'name': 'Vereda San Rafael', 'x': 1.0, 'y': -4.0, 'weight': 3.0, 'value': 30.0},
    {'id': 4, 'name': 'El Convenio', 'x': 7.0, 'y': 2.0, 'weight': 5.0, 'value': 60.0},
    {'id': 5, 'name': 'Vereda La Cabaña', 'x': -3.0, 'y': 5.0, 'weight': 4.0, 'value': 50.0},
    {'id': 6, 'name': 'Vereda Santa Rosa', 'x': 6.0, 'y': -2.0, 'weight': 2.0, 'value': 25.0}
]

def distancia_euclidiana(p1, p2):
    """Calcula la distancia en línea recta entre dos puntos geográficos (coordenadas cartesianas)."""
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)


# ==========================================
# 1. DIVIDE Y VENCERÁS: MergeSort Geográfico
# ==========================================
def ordenar_veredas_por_cercania(lista):
    """Ordena las veredas por su distancia euclidiana al centro de acopio usando Divide y Vencerás."""
    if len(lista) <= 1:
        return lista

    mid = len(lista) // 2
    izquierda = ordenar_veredas_por_cercania(lista[:mid])
    derecha = ordenar_veredas_por_cercania(lista[mid:])

    return _merge(izquierda, derecha)

def _merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        d_izq = distancia_euclidiana(ORIGEN, izq[i])
        d_der = distancia_euclidiana(ORIGEN, der[j])
        if d_izq <= d_der:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


# ==========================================
# 2. PROGRAMACIÓN DINÁMICA: Mochila 0/1 (Carga de Leche)
# ==========================================
def seleccion_carga_dp(items, capacidad_maxima):
    """Selecciona los pedidos de leche que maximizan el valor sin exceder la capacidad W del vehículo."""
    n = len(items)
    cap = int(capacidad_maxima)
    dp = [[0.0 for _ in range(cap + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_i = int(items[i-1]['weight'])
        valor_i = items[i-1]['value']
        for w in range(cap + 1):
            if peso_i <= w:
                dp[i][w] = max(valor_i + dp[i-1][w - peso_i], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    # Reconstrucción de la solución (Backtracking de la tabla DP)
    w = cap
    seleccionados = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            seleccionados.append(items[i-1])
            w -= int(items[i-1]['weight'])

    return seleccionados, dp[n][cap]


# ==========================================
# 3. ALGORITMO VORAZ: Vecino Más Cercano (Ruta Inicial)
# ==========================================
def ruta_voraz_leche(veredas_asignadas):
    """Genera una ruta inicial visitando la vereda más cercana no visitada (Cota Superior)."""
    no_visitados = list(veredas_asignadas)
    actual = ORIGEN
    ruta = [ORIGEN]
    distancia_total = 0.0

    while no_visitados:
        siguiente = min(no_visitados, key=lambda v: distancia_euclidiana(actual, v))
        distancia_total += distancia_euclidiana(actual, siguiente)
        ruta.append(siguiente)
        no_visitados.remove(siguiente)
        actual = siguiente

    # Regresar al centro de acopio (Cierre del ciclo)
    distancia_total += distancia_euclidiana(actual, ORIGEN)
    ruta.append(ORIGEN)

    return ruta, distancia_total


# ==========================================
# 4. BACKTRACKING CON PODA: TSP Óptimo Exacto
# ==========================================
def resolver_tsp_backtracking(veredas_asignadas):
    """Encuentra la ruta óptima exacta de reparto entre las veredas utilizando Backtracking con Poda."""
    n = len(veredas_asignadas)
    if n == 0:
        return [ORIGEN, ORIGEN], 0.0

    # Usar el resultado voraz como cota superior inicial para la poda
    _, distancia_voraz = ruta_voraz_leche(veredas_asignadas)
    mejor_distancia = distancia_voraz
    mejor_ruta = []
    ramas_podadas = 0

    def backtrack(actual_idx, visitados_mask, ruta_actual, dist_actual):
        nonlocal mejor_distancia, mejor_ruta, ramas_podadas

        # Poda: Si la distancia parcial supera o iguala la mejor distancia conocida, descartar rama
        if dist_actual >= mejor_distancia:
            ramas_podadas += 1
            return

        # Si ya se visitaron todas las veredas, cerrar el ciclo volviendo al origen
        if len(ruta_actual) == n:
            dist_total = dist_actual + distancia_euclidiana(veredas_asignadas[actual_idx], ORIGEN)
            if dist_total < mejor_distancia:
                mejor_distancia = dist_total
                mejor_ruta = list(ruta_actual) + [ORIGEN]
            return

        for siguiente_idx in range(n):
            if not (visitados_mask & (1 << siguiente_idx)):
                nodo_actual = veredas_asignadas[actual_idx] if ruta_actual else ORIGEN
                nodo_siguiente = veredas_asignadas[siguiente_idx]
                nueva_dist = dist_actual + distancia_euclidiana(nodo_actual, nodo_siguiente)
                
                backtrack(
                    siguiente_idx, 
                    visitados_mask | (1 << siguiente_idx), 
                    ruta_actual + [nodo_siguiente], 
                    nueva_dist
                )

    for i in range(n):
        dist_inicial = distancia_euclidiana(ORIGEN, veredas_asignadas[i])
        backtrack(i, 1 << i, [veredas_asignadas[i]], dist_inicial)

    ruta_completa = [ORIGEN] + mejor_ruta
    return ruta_completa, mejor_distancia, ramas_podadas


# ==========================================
# 🚀 EJECUCIÓN PRINCIPAL Y PRUEBAS
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🥛 PROYECTO INTEGRADOR: OPTILECHE LÉRIDA+")
    print("=" * 60)

    # 1. Probar Divide y Vencerás
    print("\n[1] DIVIDE Y VENCERÁS (Ordenamiento por distancia a Lérida Urbano):")
    veredas_ordenadas = ordenar_veredas_por_cercania(veredas_lerida)
    for v in veredas_ordenadas:
        print(f" -> {v['name']}: {distancia_euclidiana(ORIGEN, v):.2f} km de distancia")

    # 2. Probar Programación Dinámica (Capacidad de carga de leche = 12 kg)
    capacidad_vehiculo = 12.0
    print(f"\n[2] PROGRAMACIÓN DINÁMICA (Mochila 0/1 - Capacidad: {capacidad_vehiculo} kg):")
    veredas_seleccionadas, valor_maximo = seleccion_carga_dp(veredas_lerida, capacidad_vehiculo)
    print(f" Beneficio total obtenido: ${valor_maximo}")
    print(" Veredas seleccionadas para cargar en el furgón:")
    for v in veredas_seleccionadas:
        print(f"   * {v['name']} (Demanda: {v['weight']} kg, Valor: ${v['value']})")

    # 3. Probar Algoritmo Voraz
    print(f"\n[3] ALGORITMO VORAZ (Ruta Inicial de Reparto):")
    ruta_v, dist_v = ruta_voraz_leche(veredas_seleccionadas)
    print(f" Distancia estimada (Voraz): {dist_v:.2f} km")
    print(" Secuencia:", " -> ".join([p['name'] for p in ruta_v]))

    # 4. Probar Backtracking con Poda
    print(f"\n[4] BACKTRACKING CON PODA (Ruta Óptima Exacta):")
    ruta_opt, dist_opt, podas = resolver_tsp_backtracking(veredas_seleccionadas)
    print(f" Distancia exacta óptima: {dist_opt:.2f} km")
    print(f" Ramas eliminadas por poda: {podas}")
    print(" Secuencia óptima final:", " -> ".join([p['name'] for p in ruta_opt]))
    print("=" * 60)