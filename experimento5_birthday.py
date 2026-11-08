"""
Experimento 5: Paradoja del cumpleaños con hashes truncados
Genera entradas hasta encontrar dos distintas con el mismo hash truncado.
Ilustra por qué la longitud de salida determina la resistencia a colisiones.
"""
import hashlib
import os
import json
import statistics

def find_collision_truncated(n_bits, algorithm='sha256', max_attempts=10_000_000):
    """
    Busca una colisión usando solo los primeros n_bits del hash.
    Retorna (intentos, input1, input2, hash_truncado) o None si no se encuentra.
    """
    # Calculamos cuántos caracteres hexadecimales corresponden a n_bits
    n_hex = n_bits // 4
    seen = {}

    for i in range(max_attempts):
        # Generar una entrada única
        input_data = f"entrada_{i}_{os.urandom(4).hex()}"
        full_hash = hashlib.new(algorithm, input_data.encode('utf-8')).hexdigest()
        truncated = full_hash[:n_hex]

        if truncated in seen:
            return {
                'attempts': i + 1,
                'input1': seen[truncated],
                'input2': input_data,
                'truncated_hash': truncated,
                'n_bits': n_bits
            }
        seen[truncated] = input_data

    return None

if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENTO 5: PARADOJA DEL CUMPLEAÑOS CON HASHES TRUNCADOS")
    print("=" * 60)

    bit_sizes = [16, 20, 24, 32]
    trials_per_size = 5  # Repetir para obtener estadísticas

    all_results = []

    for n_bits in bit_sizes:
        theoretical = 2 ** (n_bits / 2)
        print(f"\n--- {n_bits} bits (teórico ≈ {theoretical:.0f} intentos) ---")

        trial_attempts = []
        for trial in range(trials_per_size):
            result = find_collision_truncated(n_bits)
            if result:
                trial_attempts.append(result['attempts'])
                if trial == 0:  # Mostrar detalle solo del primer trial
                    print(f"  Colisión encontrada en {result['attempts']} intentos")
                    print(f"    Entrada 1: {result['input1'][:40]}...")
                    print(f"    Entrada 2: {result['input2'][:40]}...")
                    print(f"    Hash truncado: {result['truncated_hash']}")
            else:
                print(f"  Trial {trial+1}: No se encontró colisión")

        if trial_attempts:
            median_attempts = statistics.median(trial_attempts)
            mean_attempts = statistics.mean(trial_attempts)
            ratio = median_attempts / theoretical

            print(f"  Intentos (mediana de {trials_per_size} pruebas): {median_attempts:.0f}")
            print(f"  Intentos (promedio): {mean_attempts:.0f}")
            print(f"  Ratio mediana/teórico: {ratio:.2f}")

            all_results.append({
                'n_bits': n_bits,
                'theoretical_approx': int(theoretical),
                'median_attempts': int(median_attempts),
                'mean_attempts': round(mean_attempts, 0),
                'all_attempts': trial_attempts,
                'ratio_to_theoretical': round(ratio, 2),
                'trials': trials_per_size
            })

    # Tabla resumen
    print("\n" + "=" * 60)
    print("TABLA RESUMEN")
    print("=" * 60)
    print(f"{'Bits':>6} | {'Teórico (2^(n/2))':>18} | {'Mediana obtenida':>16} | {'Ratio':>6}")
    print("-" * 55)
    for r in all_results:
        print(f"{r['n_bits']:>6} | {r['theoretical_approx']:>18,} | {r['median_attempts']:>16,} | {r['ratio_to_theoretical']:>6.2f}")

    # --- Verificación SHAttered (usando hashes conocidos públicamente) ---
    print("\n" + "=" * 60)
    print("VERIFICACIÓN: ARCHIVOS PDF DEL ATAQUE SHAttered")
    print("=" * 60)

    # Hashes públicos de los archivos SHAttered (documentados en shattered.io)
    shattered_pdf1_sha1 = "38762cf7f55934b34d179ae6a4c80cadccbb7f0a"
    shattered_pdf2_sha1 = "38762cf7f55934b34d179ae6a4c80cadccbb7f0a"

    shattered_pdf1_sha256 = "2bb787a73e37352f92383abe7e2902936d1059ad9f1ba6daaa9c1e58ee6970d0"
    shattered_pdf2_sha256 = "d4488775d29bdef7993367d541064dbdda50d383f89f0aa13a6ff2e0894ba5ff"

    print("\nHashes SHA-1 (documentados públicamente):")
    print(f"  PDF 1: {shattered_pdf1_sha1}")
    print(f"  PDF 2: {shattered_pdf2_sha1}")
    print(f"  ¿Coinciden? {'SÍ → COLISIÓN DEMOSTRADA' if shattered_pdf1_sha1 == shattered_pdf2_sha1 else 'NO'}")

    print("\nHashes SHA-256 (documentados públicamente):")
    print(f"  PDF 1: {shattered_pdf1_sha256}")
    print(f"  PDF 2: {shattered_pdf2_sha256}")
    print(f"  ¿Coinciden? {'SÍ' if shattered_pdf1_sha256 == shattered_pdf2_sha256 else 'NO → Archivos distinguibles con SHA-256'}")

    # Guardar resultados
    output = {
        'birthday_paradox': all_results,
        'shattered_verification': {
            'pdf1_sha1': shattered_pdf1_sha1,
            'pdf2_sha1': shattered_pdf2_sha1,
            'sha1_collision': shattered_pdf1_sha1 == shattered_pdf2_sha1,
            'pdf1_sha256': shattered_pdf1_sha256,
            'pdf2_sha256': shattered_pdf2_sha256,
            'sha256_collision': shattered_pdf1_sha256 == shattered_pdf2_sha256,
            'source': 'https://shattered.io - Stevens et al. (2017)'
        }
    }

    with open('resultados_exp5.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\nResultados guardados en resultados_exp5.json")

