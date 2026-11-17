import math

# ==========================================
# 🥛 DATASET: OPTILECHE LÉRIDA+
# ==========================================
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
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

# ==========================================
# 3. ALGORITMO VORAZ (Cota Superior Inicial)
# ==========================================
def ruta_voraz_leche(veredas_asignadas):
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

    distancia_total += distancia_euclidiana(actual, ORIGEN)
    ruta.append(ORIGEN)
    return ruta, distancia_total

# ==========================================
# 4. BACKTRACKING CON PODA (TSP Exacto)
# ==========================================
def resolver_tsp_backtracking(veredas_asignadas):
    """
    Encuentra la ruta óptima exacta (Ciclo Hamiltoniano) visitando todas las
    veredas asignadas y regresando al centro de acopio de Lérida, utilizando Backtracking y Poda.
    """
    n = len(veredas_asignadas)
    if n == 0:
        return [ORIGEN, ORIGEN], 0.0, 0

    mejor_ruta = []
    # Usamos la solución voraz como cota superior para la poda
    _, distancia_voraz = ruta_voraz_leche(veredas_asignadas)
    mejor_distancia = distancia_voraz
    ramas_podadas = 0

    def backtrack(actual_idx, visitados_mask, ruta_actual, dist_actual):
        nonlocal mejor_distancia, mejor_ruta, ramas_podadas

        # Poda: Si la distancia parcial supera o iguala la mejor ruta encontrada, abortar rama
        if dist_actual >= mejor_distancia:
            ramas_podadas += 1
            return

        # Si ya visitamos todas las veredas, cerrar el ciclo regresando a Lérida urbano
        if len(ruta_actual) == n:
            dist_total = dist_actual + distancia_euclidiana(veredas_asignadas[actual_idx], ORIGEN)
            if dist_total < mejor_distancia:
                mejor_distancia = dist_total
                mejor_ruta = list(ruta_actual) + [ORIGEN]
            return

        # Explorar veredas no visitadas
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
# PRUEBA DEL MÓDULO DE BACKTRACKING
# ==========================================
if __name__ == "__main__":
    print("=== PRUEBA DE BACKTRACKING CON PODA (OPTILECHE LÉRIDA+) ===")
    
    # Supongamos un subconjunto de 5 veredas para la prueba del hito intermedio
    veredas_prueba = veredas_lerida[:5]
    
    _, dist_v = ruta_voraz_leche(veredas_prueba)
    print(f"Distancia inicial (Voraz - Cota Superior): {dist_v:.2f} km")

    ruta_optima, dist_optima, podas = resolver_tsp_backtracking(veredas_prueba)
    
    print(f"Distancia óptima exacta (Backtracking): {dist_optima:.2f} km")
    print(f"Ramas podadas (ahorro computacional): {podas}")
    print("Secuencia de ruta óptima:", " -> ".join([p['name'] for p in ruta_optima]))