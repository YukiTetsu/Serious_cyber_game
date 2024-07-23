import hashlib

def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Informations d'identification
login_user = 'pierre'
login_pass = 'T3rminat0r'

# Générer les hash des identifiants
hashed_login_user = generate_hash(login_user)
hashed_login_pass = generate_hash(login_pass)

# Afficher les hash
print(f'Hashed Login: {hashed_login_user}')
print(f'Hashed Password: {hashed_login_pass}')

# Stocker les hash dans un fichier (optionnel)
with open('hashed_config.txt', 'w') as f:
    f.write(f'{hashed_login_user}\n')
    f.write(f'{hashed_login_pass}\n')