"""
Experimento 3: Comparación de algoritmos
Mide la longitud de salida y el tiempo de cálculo para MD5, SHA-1, SHA-256 y SHA-512
procesando un bloque de datos de tamaño fijo, repitiendo la medición varias veces.
"""
import hashlib
import time
import os
import statistics
import json

def measure_hash_time(algorithm, data, repetitions=100):
    """Mide el tiempo de cálculo de un hash repetido varias veces."""
    times = []
    for _ in range(repetitions):
        start = time.perf_counter()
        hashlib.new(algorithm, data).hexdigest()
        end = time.perf_counter()
        times.append(end - start)
    return times

if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENTO 3: COMPARACIÓN DE ALGORITMOS")
    print("=" * 60)

    # Generar datos de prueba: 10 MB de datos aleatorios
    data_size_mb = 10
    data_size_bytes = data_size_mb * 1024 * 1024
    print(f"\nGenerando {data_size_mb} MB de datos aleatorios...")
    data = os.urandom(data_size_bytes)
    print(f"Datos generados: {len(data)} bytes")

    algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    repetitions = 50

    print(f"\nRepeticiones por algoritmo: {repetitions}")
    print(f"Tamaño de datos: {data_size_mb} MB")

    results = []

    for algo in algorithms:
        # Información del hash
        sample_hash = hashlib.new(algo, b"test").hexdigest()
        output_bits = len(sample_hash) * 4  # Cada carácter hex = 4 bits
        hex_chars = len(sample_hash)

        # Medir tiempos
        times = measure_hash_time(algo, data, repetitions)
        median_time = statistics.median(times)
        mean_time = statistics.mean(times)
        stdev_time = statistics.stdev(times) if len(times) > 1 else 0
        speed_mbps = data_size_mb / median_time if median_time > 0 else float('inf')

        result = {
            'algorithm': algo.upper(),
            'output_bits': output_bits,
            'hex_chars': hex_chars,
            'median_time_s': round(median_time, 6),
            'mean_time_s': round(mean_time, 6),
            'stdev_time_s': round(stdev_time, 6),
            'speed_mb_s': round(speed_mbps, 2),
            'repetitions': repetitions,
            'data_size_mb': data_size_mb
        }
        results.append(result)

        print(f"\n--- {algo.upper()} ---")
        print(f"  Salida:           {output_bits} bits ({hex_chars} caracteres hex)")
        print(f"  Tiempo mediano:   {median_time:.6f} s")
        print(f"  Tiempo promedio:  {mean_time:.6f} s")
        print(f"  Desv. estándar:   {stdev_time:.6f} s")
        print(f"  Velocidad:        {speed_mbps:.2f} MB/s")

    # Tabla resumen
    print("\n" + "=" * 60)
    print("TABLA RESUMEN")
    print("=" * 60)
    print(f"{'Algoritmo':>10} | {'Bits':>6} | {'Hex chars':>9} | {'Mediana (s)':>12} | {'MB/s':>10}")
    print("-" * 60)
    for r in results:
        print(f"{r['algorithm']:>10} | {r['output_bits']:>6} | {r['hex_chars']:>9} | {r['median_time_s']:>12.6f} | {r['speed_mb_s']:>10.2f}")

    # Guardar resultados
    output = {
        'data_size_mb': data_size_mb,
        'data_size_bytes': data_size_bytes,
        'repetitions': repetitions,
        'results': results
    }

    with open('resultados_exp3.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\nResultados guardados en resultados_exp3.json")

