import time
import random
import math

def generar_instancia_lerida(n, semilla=42):
    random.seed(semilla)
    origen = {'id': 0, 'name': 'Centro Acopio (Lérida)', 'x': 0.0, 'y': 0.0}
    nombres_veredas = [
        'Vereda La Sierra', 'Vereda El Delirio', 'Vereda San Rafael',
        'El Convenio', 'Vereda La Cabaña', 'Vereda Santa Rosa',
        'Vereda El Descanso', 'Vereda Las Margaritas', 'Vereda Alto del Sol'
    ]
    veredas = []
    for i in range(n):
        veredas.append({
            'id': i + 1,
            'name': nombres_veredas[i % len(nombres_veredas)],
            'x': round(random.uniform(-10, 10), 2),
            'y': round(random.uniform(-10, 10), 2)
        })
    return origen, veredas

def dist(p1, p2):
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

def voraz(veredas, origen):
    no_vis = list(veredas)
    actual = origen
    d_total = 0.0
    while no_vis:
        sig = min(no_vis, key=lambda v: dist(actual, v))
        d_total += dist(actual, sig)
        no_vis.remove(sig)
        actual = sig
    return d_total + dist(actual, origen)

def backtracking_benchmark(veredas, origen, usar_poda=True):
    n = len(veredas)
    mejor_dist = voraz(veredas, origen) if usar_poda else float('inf')
    nodos_explorados = 0
    ramas_podadas = 0

    def bt(actual_idx, mask, count, d_actual):
        nonlocal mejor_dist, nodos_explorados, ramas_podadas
        nodos_explorados += 1

        if usar_poda and d_actual >= mejor_dist:
            ramas_podadas += 1
            return

        if count == n:
            d_total = d_actual + dist(veredas[actual_idx], origen)
            if d_total < mejor_dist:
                mejor_dist = d_total
            return

        for sig in range(n):
            if not (mask & (1 << sig)):
                bt(sig, mask | (1 << sig), count + 1, d_actual + dist(veredas[actual_idx], veredas[sig]))

    for i in range(n):
        bt(i, 1 << i, 1, dist(origen, veredas[i]))

    return mejor_dist, nodos_explorados, ramas_podadas

if __name__ == "__main__":
    print("=== 📊 BENCHMARKING OPTILECHE LÉRIDA+ ===")
    print(f"{'N':<4} | {'Voraz (km)':<12} | {'Exacto (km)':<12} | {'T. Sin Poda (ms)':<18} | {'T. Con Poda (ms)':<18} | {'Ramas Podadas':<15}")
    print("-" * 92)
    for n in [5, 6, 7, 8, 9]:
        origen, veredas = generar_instancia_lerida(n)
        
        d_voraz = voraz(veredas, origen)
        
        t0 = time.perf_counter()
        _, _, _ = backtracking_benchmark(veredas, origen, usar_poda=False)
        t_sin_poda = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        d_exacta, _, podadas = backtracking_benchmark(veredas, origen, usar_poda=True)
        t_con_poda = (time.perf_counter() - t0) * 1000

        print(f"{n:<4} | {d_voraz:<12.2f} | {d_exacta:<12.2f} | {t_sin_poda:<18.3f} | {t_con_poda:<18.3f} | {podadas:<15}")