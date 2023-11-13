import hashlib

def calcular_hash_arquivo(nome_arquivo):
    with open(nome_arquivo, 'rb') as arquivo:
        conteudo = arquivo.read()
        hash_md5 = hashlib.md5(conteudo).hexdigest()
        hash_sha256 = hashlib.sha256(conteudo).hexdigest()
    
    return hash_md5, hash_sha256

nome_arquivo_pcap = 'captura.pcap'
hash_md5, hash_sha256 = calcular_hash_arquivo(nome_arquivo_pcap)

print("Hash MD5:", hash_md5)
print("Hash SHA-256:", hash_sha256)