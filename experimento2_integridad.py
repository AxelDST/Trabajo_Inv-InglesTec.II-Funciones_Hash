"""
Experimento 2: Verificación de integridad de un archivo
Calcula el hash de un archivo, modifica un byte de una copia y verifica
que el hash cambia, demostrando la detección de alteraciones.
"""
import hashlib
import os
import shutil
import json

def hash_file(filepath, algorithm='sha256'):
    """Calcula el hash de un archivo."""
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def create_test_file(filepath, content=None):
    """Crea un archivo de prueba con contenido conocido."""
    if content is None:
        content = (
            "Este es un archivo de prueba para el experimento de verificación de integridad.\n"
            "Contiene texto que será verificado mediante funciones hash criptográficas.\n"
            "Cualquier modificación, por mínima que sea, debería producir un hash completamente diferente.\n"
            "Universidad Nacional - Proyecto de Investigación 2026\n"
            "Seguridad Informática - Funciones Hash\n"
        )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return content

def modify_one_byte(src_path, dst_path):
    """Copia un archivo y modifica un único byte."""
    shutil.copy2(src_path, dst_path)
    with open(dst_path, 'r+b') as f:
        f.seek(10)  # Posición arbitraria
        original_byte = f.read(1)
        f.seek(10)
        # Cambiar el byte (XOR con 1 para invertir el último bit)
        modified_byte = bytes([original_byte[0] ^ 1])
        f.write(modified_byte)
    return original_byte, modified_byte

if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENTO 2: VERIFICACIÓN DE INTEGRIDAD DE ARCHIVO")
    print("=" * 60)

    original_file = 'archivo_prueba_original.txt'
    modified_file = 'archivo_prueba_modificado.txt'

    # Crear archivo de prueba
    content = create_test_file(original_file)
    file_size = os.path.getsize(original_file)
    print(f"\nArchivo de prueba creado: {original_file}")
    print(f"Tamaño: {file_size} bytes")

    algorithms = ['md5', 'sha1', 'sha256', 'sha512']

    # Calcular hashes del archivo original
    print("\n--- Hashes del archivo original ---")
    original_hashes = {}
    for algo in algorithms:
        h = hash_file(original_file, algo)
        original_hashes[algo] = h
        print(f"  {algo.upper():>8}: {h}")

    # Modificar un byte
    orig_byte, mod_byte = modify_one_byte(original_file, modified_file)
    print(f"\n--- Modificación ---")
    print(f"  Byte en posición 10: {orig_byte.hex()} → {mod_byte.hex()}")
    print(f"  (1 solo bit invertido)")

    # Calcular hashes del archivo modificado
    print("\n--- Hashes del archivo modificado ---")
    modified_hashes = {}
    for algo in algorithms:
        h = hash_file(modified_file, algo)
        modified_hashes[algo] = h
        print(f"  {algo.upper():>8}: {h}")

    # Comparación
    print("\n--- Comparación ---")
    results = []
    for algo in algorithms:
        match = original_hashes[algo] == modified_hashes[algo]
        print(f"  {algo.upper():>8}: {'COINCIDE ✗ (peligro)' if match else 'NO COINCIDE ✓ (alteración detectada)'}")
        results.append({
            'algorithm': algo.upper(),
            'hash_original': original_hashes[algo],
            'hash_modified': modified_hashes[algo],
            'match': match
        })

    # Guardar resultados
    output = {
        'file': original_file,
        'file_size_bytes': file_size,
        'modification': f"Byte en posición 10: {orig_byte.hex()} → {mod_byte.hex()} (1 bit invertido)",
        'results': results
    }

    with open('resultados_exp2.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Limpiar archivos temporales
    os.remove(original_file)
    os.remove(modified_file)

    print("\nResultados guardados en resultados_exp2.json")

