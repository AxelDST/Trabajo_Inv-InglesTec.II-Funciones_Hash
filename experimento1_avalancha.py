"""
Experimento 1: Efecto Avalancha
Calcula los hashes de un texto y de una versión mínimamente alterada,
compara la representación binaria y cuenta cuántos bits difieren.
"""
import hashlib
import json

def to_bin(hex_str):
    """Convierte un string hexadecimal a su representación binaria."""
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def count_diff_bits(bin1, bin2):
    """Cuenta bits diferentes entre dos cadenas binarias de igual longitud."""
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))

def avalanche_test(text_original, text_modified, algorithms):
    """Ejecuta el test de avalancha para múltiples algoritmos."""
    results = []
    for algo_name in algorithms:
        h_orig = hashlib.new(algo_name, text_original.encode('utf-8')).hexdigest()
        h_mod = hashlib.new(algo_name, text_modified.encode('utf-8')).hexdigest()

        bin_orig = to_bin(h_orig)
        bin_mod = to_bin(h_mod)

        total_bits = len(bin_orig)
        diff_bits = count_diff_bits(bin_orig, bin_mod)
        percentage = (diff_bits / total_bits) * 100

        results.append({
            'algorithm': algo_name.upper(),
            'total_bits': total_bits,
            'diff_bits': diff_bits,
            'percentage': round(percentage, 2),
            'hash_original': h_orig,
            'hash_modified': h_mod
        })

        print(f"\n--- {algo_name.upper()} ---")
        print(f"  Texto original:   \"{text_original}\"")
        print(f"  Texto modificado: \"{text_modified}\"")
        print(f"  Hash original:    {h_orig}")
        print(f"  Hash modificado:  {h_mod}")
        print(f"  Bits totales:     {total_bits}")
        print(f"  Bits diferentes:  {diff_bits}")
        print(f"  Porcentaje:       {percentage:.2f}%")

    return results

if __name__ == '__main__':
    text_original = "Hola mundo"
    text_modified = "Hola Mundo"  # Cambio de minúscula a mayúscula en 'm'

    algorithms = ['md5', 'sha1', 'sha256', 'sha512']

    print("=" * 60)
    print("EXPERIMENTO 1: EFECTO AVALANCHA")
    print("=" * 60)
    print(f"\nEntrada original:   \"{text_original}\"")
    print(f"Entrada modificada: \"{text_modified}\"")
    print(f"Cambio: un solo carácter ('m' → 'M')")

    results = avalanche_test(text_original, text_modified, algorithms)

    # Prueba adicional: agregar un punto al final
    text_modified_2 = "Hola mundo."
    print("\n" + "=" * 60)
    print("PRUEBA ADICIONAL: agregar un punto al final")
    print("=" * 60)
    print(f"\nEntrada original:   \"{text_original}\"")
    print(f"Entrada modificada: \"{text_modified_2}\"")

    results_2 = avalanche_test(text_original, text_modified_2, algorithms)

    # Guardar resultados en JSON
    output = {
        'test_1': {
            'original': text_original,
            'modified': text_modified,
            'change_description': "Cambio de 'm' minúscula a 'M' mayúscula",
            'results': results
        },
        'test_2': {
            'original': text_original,
            'modified': text_modified_2,
            'change_description': "Se agregó un punto al final",
            'results': results_2
        }
    }

    with open('resultados_exp1.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n\nResultados guardados en resultados_exp1.json")

