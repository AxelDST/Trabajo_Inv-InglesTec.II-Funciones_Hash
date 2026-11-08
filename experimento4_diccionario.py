"""
Experimento 4: Ataque de diccionario con y sin sal
Simula el almacenamiento de contraseñas con hash simple y con sal,
y luego ejecuta un ataque de diccionario para comparar ambos escenarios.
También mide el costo de un algoritmo lento (PBKDF2) vs hash rápido.
"""
import hashlib
import os
import time
import json

# Base de usuarios ficticios con contraseñas inventadas
USERS = {
    'alice': '123456',
    'bob': 'password',
    'carlos': 'qwerty',
    'diana': 'letmein',
    'elena': 'S3gur4!2026',    # Contraseña fuerte, no estará en el diccionario
    'franco': 'admin',
    'gabriela': 'Xk9$mPz!wQ',  # Contraseña fuerte, no estará en el diccionario
    'hugo': 'iloveyou',
}

# Diccionario de contraseñas comunes (simulado)
DICTIONARY = [
    '123456', 'password', '123456789', 'qwerty', 'abc123',
    '111111', 'letmein', 'admin', 'welcome', 'monkey',
    'master', 'dragon', 'login', 'princess', 'football',
    'shadow', 'sunshine', 'trustno1', 'iloveyou', '1234567',
    'batman', 'access', 'hello', 'charlie', 'donald',
    '654321', 'baseball', 'michael', '696969', 'jordan',
    'superman', 'harley', 'robert', 'daniel', 'hannah',
    'thomas', 'summer', 'george', 'pepper', 'buster',
    'ginger', 'sparky', 'tigger', 'cookie', 'joshua',
    'hunter', 'maverick', 'ranger', 'samantha', 'andrea',
]

def hash_simple(password, algorithm='sha256'):
    """Hash simple de una contraseña (sin sal)."""
    return hashlib.new(algorithm, password.encode('utf-8')).hexdigest()

def hash_with_salt(password, salt, algorithm='sha256'):
    """Hash de una contraseña con sal."""
    return hashlib.new(algorithm, (salt + password).encode('utf-8')).hexdigest()

def generate_salt(length=16):
    """Genera una sal aleatoria."""
    return os.urandom(length).hex()

def pbkdf2_hash(password, salt, iterations=100000):
    """Hash con PBKDF2 (algoritmo lento)."""
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                salt.encode('utf-8'), iterations).hex()

if __name__ == '__main__':
    print("=" * 60)
    print("EXPERIMENTO 4: ATAQUE DE DICCIONARIO CON Y SIN SAL")
    print("=" * 60)

    # --- ESCENARIO 1: Hash simple (sin sal) ---
    print("\n--- ESCENARIO 1: Hash simple (sin sal) ---")
    stored_simple = {}
    for user, pwd in USERS.items():
        stored_simple[user] = hash_simple(pwd)
        print(f"  {user:>10}: {stored_simple[user][:32]}...")

    # Ataque de diccionario contra hash simple
    print("\n  Ejecutando ataque de diccionario...")
    start_time = time.perf_counter()
    hash_calcs_simple = 0
    cracked_simple = {}

    # Precalcular hashes del diccionario (el atacante puede reutilizarlos)
    dict_hashes = {}
    for word in DICTIONARY:
        h = hash_simple(word)
        dict_hashes[h] = word
        hash_calcs_simple += 1

    # Comparar con los hashes almacenados
    for user, stored_hash in stored_simple.items():
        if stored_hash in dict_hashes:
            cracked_simple[user] = dict_hashes[stored_hash]

    time_simple = time.perf_counter() - start_time

    print(f"  Contraseñas recuperadas: {len(cracked_simple)} de {len(USERS)}")
    print(f"  Cálculos de hash: {hash_calcs_simple}")
    print(f"  Tiempo: {time_simple:.6f} s")
    for user, pwd in cracked_simple.items():
        print(f"    ✗ {user}: {pwd}")

    users_not_cracked = [u for u in USERS if u not in cracked_simple]
    print(f"  Contraseñas NO recuperadas ({len(users_not_cracked)}): {', '.join(users_not_cracked)}")

    # --- ESCENARIO 2: Hash con sal ---
    print("\n--- ESCENARIO 2: Hash con sal ---")
    stored_salted = {}
    salts = {}
    for user, pwd in USERS.items():
        salt = generate_salt()
        salts[user] = salt
        stored_salted[user] = hash_with_salt(pwd, salt)
        print(f"  {user:>10}: sal={salt[:16]}... hash={stored_salted[user][:32]}...")

    # Ataque de diccionario contra hash con sal
    print("\n  Ejecutando ataque de diccionario...")
    start_time = time.perf_counter()
    hash_calcs_salted = 0
    cracked_salted = {}

    # Con sal, el atacante debe calcular un hash por cada combinación usuario-palabra
    for user, stored_hash in stored_salted.items():
        salt = salts[user]
        for word in DICTIONARY:
            h = hash_with_salt(word, salt)
            hash_calcs_salted += 1
            if h == stored_hash:
                cracked_salted[user] = word
                break

    time_salted = time.perf_counter() - start_time

    print(f"  Contraseñas recuperadas: {len(cracked_salted)} de {len(USERS)}")
    print(f"  Cálculos de hash: {hash_calcs_salted}")
    print(f"  Tiempo: {time_salted:.6f} s")
    for user, pwd in cracked_salted.items():
        print(f"    ✗ {user}: {pwd}")

    users_not_cracked_salted = [u for u in USERS if u not in cracked_salted]
    print(f"  Contraseñas NO recuperadas ({len(users_not_cracked_salted)}): {', '.join(users_not_cracked_salted)}")

    # --- COMPARACIÓN DE COSTO: SHA-256 simple vs PBKDF2 ---
    print("\n--- COMPARACIÓN: SHA-256 simple vs PBKDF2 ---")
    test_password = "password"
    test_salt = generate_salt()

    # SHA-256 simple: medir tiempo de 1000 cálculos
    n_iterations_test = 1000
    start = time.perf_counter()
    for _ in range(n_iterations_test):
        hash_simple(test_password)
    time_sha256 = (time.perf_counter() - start) / n_iterations_test

    # PBKDF2: medir tiempo de 10 cálculos (es mucho más lento)
    n_iterations_pbkdf2 = 10
    start = time.perf_counter()
    for _ in range(n_iterations_pbkdf2):
        pbkdf2_hash(test_password, test_salt)
    time_pbkdf2 = (time.perf_counter() - start) / n_iterations_pbkdf2

    slowdown_factor = time_pbkdf2 / time_sha256 if time_sha256 > 0 else float('inf')

    print(f"  SHA-256 simple:  {time_sha256:.8f} s por cálculo")
    print(f"  PBKDF2 (100k it): {time_pbkdf2:.6f} s por cálculo")
    print(f"  Factor de lentitud: {slowdown_factor:.0f}x")

    # Guardar resultados
    output = {
        'users_total': len(USERS),
        'dictionary_size': len(DICTIONARY),
        'scenario_simple': {
            'cracked': len(cracked_simple),
            'not_cracked': len(users_not_cracked),
            'hash_calculations': hash_calcs_simple,
            'time_s': round(time_simple, 6),
            'cracked_users': cracked_simple,
            'not_cracked_users': users_not_cracked
        },
        'scenario_salted': {
            'cracked': len(cracked_salted),
            'not_cracked': len(users_not_cracked_salted),
            'hash_calculations': hash_calcs_salted,
            'time_s': round(time_salted, 6),
            'cracked_users': cracked_salted,
            'not_cracked_users': users_not_cracked_salted
        },
        'cost_comparison': {
            'sha256_time_per_hash_s': round(time_sha256, 8),
            'pbkdf2_time_per_hash_s': round(time_pbkdf2, 6),
            'slowdown_factor': round(slowdown_factor, 0),
            'pbkdf2_iterations': 100000
        }
    }

    with open('resultados_exp4.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\nResultados guardados en resultados_exp4.json")

