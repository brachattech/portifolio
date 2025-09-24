import numpy as np
import os

# Define a pasta onde os arquivos estão
data_folder = 'provas_pas'

# Define os nomes dos arquivos
embeddings_file = os.path.join(data_folder, 'combined_embeddings.npy')
paragraphs_file = os.path.join(data_folder, 'combined_paragraphs.npy')

# Verifica se os arquivos existem
if not os.path.exists(embeddings_file) or not os.path.exists(paragraphs_file):
    print(f"❌ Erro: Arquivos '{embeddings_file}' ou '{paragraphs_file}' não encontrados.")
    print("Por favor, certifique-se de que o script 'generate_combined_embeddings.py' foi executado corretamente.")
    exit()

# Carrega os arquivos
print("✅ Verificando arquivos...")
try:
    embeddings = np.load(embeddings_file)
    paragraphs = np.load(paragraphs_file, allow_pickle=True)
    
    print("✅ Arquivos carregados com sucesso!")
    print(f"Número de parágrafos encontrados: {len(paragraphs)}")
    print(f"Formato da matriz de embeddings: {embeddings.shape}")
    
    # Exibe os 3 primeiros parágrafos para uma verificação rápida
    print("\n--- Primeiros 3 Parágrafos ---")
    for i in range(min(3, len(paragraphs))):
        print(f"Parágrafo {i+1}: {paragraphs[i][:100]}...") # Mostra os primeiros 100 caracteres
    
except Exception as e:
    print(f"❌ Erro ao carregar os arquivos: {e}")
