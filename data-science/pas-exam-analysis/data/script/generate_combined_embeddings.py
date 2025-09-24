import numpy as np
import os
from sentence_transformers import SentenceTransformer

# 1. Carregar o modelo de embedding
print("Carregando o modelo de linguagem. Isso pode levar alguns segundos...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Define o nome e o caminho do arquivo de texto combinado
# Ele agora procura na pasta atual, onde você está.
text_file_path = 'combined_text.txt'

if not os.path.exists(text_file_path):
    print(f"❌ Erro: O arquivo '{text_file_path}' não foi encontrado.")
    print("Execute o script 'process_all_pdfs.py' primeiro para criar o arquivo.")
    exit()

# 2. Ler o texto e dividir em parágrafos
with open(text_file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Dividir o texto em parágrafos e remover espaços extras
paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

print(f"✅ Texto lido com sucesso! Total de parágrafos para processar: {len(paragraphs)}")
print("Gerando embeddings (isso pode demorar, dependendo do número de provas)...")

# 3. Gerar embeddings para cada parágrafo
embeddings = model.encode(paragraphs, show_progress_bar=True)

# 4. Salvar os embeddings e o texto original
np.save('combined_paragraphs.npy', paragraphs, allow_pickle=True)
np.save('combined_embeddings.npy', embeddings, allow_pickle=True)

print("\n✅ Processo concluído!")
print(f"Embeddings salvos em 'combined_embeddings.npy'")
print(f"Parágrafos originais salvos em 'combined_paragraphs.npy'")
