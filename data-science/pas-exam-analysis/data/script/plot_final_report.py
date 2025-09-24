import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import torch
from sentence_transformers import SentenceTransformer

# 1. Definição da estrutura de matérias e submatérias
keywords_hierarchy = {
    "biologia": {
        "bioquímica": ["moléculas orgânicas", "enzimas", "metabolismo celular"],
        "citologia": ["célula animal", "célula vegetal", "organelas", "membrana celular"],
        "metabolismo energético": ["fotossíntese", "respiração celular", "fermentação"],
        "ecologia": ["cadeias alimentares", "ciclos biogeoquímicos", "ecossistemas", "população", "biodiversidade", "impacto ambiental"]
    },
    "química": {
        "química geral": ["matéria", "átomos", "moléculas", "propriedades físicas e químicas", "misturas homogêneas e heterogêneas", "métodos de separação"],
        "leis ponderais": ["Lei de Lavoisier", "Lei de Proust"],
        "tabela periódica": ["grupos", "períodos", "família", "metais", "ametais", "semimetais"],
        "ligações químicas": ["iônica", "covalente", "metálica", "forças intermoleculares"],
        "estequiometria": ["reação química", "mol", "massa molecular", "balanceamento"],
        "química ambiental": ["poluição", "reações de combustão", "tratamento de resíduos"]
    },
    "física": {
        "cinemática": ["movimento retilíneo", "movimento uniformemente variado", "gráfico de posição", "velocidade"],
        "dinâmica": ["leis de Newton", "força", "massa", "aceleração", "atrito", "impulso"],
        "hidrostática": ["pressão", "empuxo", "princípio de Pascal", "princípio de Arquimedes"],
        "estática": ["equilíbrio de corpos", "torque", "centro de massa"],
        "gravitação": ["lei da gravitação universal", "peso", "órbitas"]
    },
    "matemática": {
        "matemática básica": ["operações", "frações", "porcentagem"],
        "conjuntos": ["união", "interseção", "subconjuntos", "diagramas de Venn"],
        "funções": ["função afim", "função quadrática", "função exponencial", "domínio", "imagem"],
        "logaritmo": ["propriedades", "mudança de base"],
        "progressões": ["PA e PG", "razões", "termos gerais"],
        "geometria plana": ["ângulos", "triângulos", "polígonos", "circunferência", "área", "perímetro"]
    },
    "história": {
        "idade antiga": ["Grecia antiga - democracia", "mitologia", "Roma antiga - república", "império", "direito romano"],
        "idade média": ["feudalismo", "cruzadas", "sociedade medieval"],
        "renascimento": ["humanismo", "arte renascentista", "ciência"],
        "reformas religiosas": ["luteranismo", "calvinismo", "anglicanismo"],
        "idade moderna": ["absolutismo", "mercantilismo", "revoluções", "liberalismo", "iluminismo"],
        "brasil colonial": ["colonização", "capitanias hereditárias", "sociedade colonial", "escravidão"]
    },
    "geografia": {
        "regionalização": ["divisão política", "geopolítica"],
        "geografia urbana": ["urbanização", "migrações", "favelas"],
        "demografia": ["crescimento populacional", "estrutura etária", "migrações"],
        "geografia agrária": ["agricultura", "tipos de agricultura", "reforma agrária"],
        "cartografia": ["mapas", "escalas", "projeções"],
        "geografia ambiental": ["meio ambiente", "biomas", "recursos naturais", "sustentabilidade"]
    },
    "filosofia": {
        "pré-socráticos": ["teses básicas", "cosmologia", "Tales de Mileto", "Anaximandro", "Heráclito", "Parmênides"],
        "Sócrates": ["maiêutica", "ética", "dialética"],
        "Platão": ["mundo das ideias", "alegoria da caverna"],
        "Aristóteles": ["lógica", "ética", "política"],
        "filosofia helenística": ["estoicismo", "epicurismo", "ceticismo"]
    },
    "português": {
        "elementos da comunicação": ["emissor", "receptor", "mensagem"],
        "funções da linguagem": ["referencial", "emotiva", "conativa", "metalinguística", "fática", "poética"],
        "figuras de linguagem": ["metáfora", "metonímia", "ironia", "hipérbole"],
        "gêneros e tipologias textuais": ["narrativo", "dissertativo", "injuntivo"],
        "variações linguísticas": ["sociolinguística", "regional", "formal e informal"],
        "coesão e coerência": ["conectivos", "progressão textual"],
        "interpretação de texto": ["análise", "inferência"]
    },
    "literatura": {
        "gêneros literários": ["poesia", "prosa", "teatro"],
        "quinhentismo": ["literatura de informação e jesuítica"],
        "barroco": ["antítese", "hipérbole", "literatura religiosa"],
        "arcadismo": ["neoclassicismo - idealização da natureza", "simplicidade"],
        "obras literárias específicas": ["poemas e textos de Carlos Drummond de Andrade", "Clarice Lispector", "entre outros"]
    },
    "artes": {
        "artes cênicas": ["teatro", "dramaturgia"],
        "artes visuais": ["pintura", "escultura", "fotografia"],
        "música": ["ritmo", "melodia", "estilos musicais"]
    },
    "língua estrangeira": {
        "inglês, espanhol ou francês": ["compreensão textual", "interpretação", "vocabulário", "gramática básica"]
    },
    "educação física": {
        "fundamentos do movimento": ["fundamentos do movimento"],
        "esportes coletivos e individuais": ["esportes coletivos e individuais"],
        "saúde e qualidade de vida": ["saúde e qualidade de vida"]
    },
    "sociologia": {
        "sociedade": ["sociedade"],
        "cultura": ["cultura"],
        "grupos sociais": ["grupos sociais"],
        "estratificação social": ["estratificação social"],
        "cidadania": ["cidadania"]
    }
}

# 2. Mapear palavras-chave para a estrutura
keyword_to_subject = {}
for subject, submatters in keywords_hierarchy.items():
    for submatter, keywords in submatters.items():
        for keyword in keywords:
            keyword_to_subject[keyword] = (subject.capitalize(), submatter.capitalize())

keyword_to_subject['temas e conteúdos fundamentais relacionados a cada submatéria do PAS 1 da UnB'] = ('Geral', 'Conteúdos Fundamentais')
keyword_to_subject['Essas palavras-chave cobrem os conceitos'] = ('Geral', 'Conteúdos Fundamentais')
keyword_to_subject['gêneros literários'] = ('Literatura', 'Gêneros Literários')
keyword_to_subject['sociedade'] = ('Sociologia', 'Sociedade')
keyword_to_subject['cultura'] = ('Sociologia', 'Cultura')
keyword_to_subject['grupos sociais'] = ('Sociologia', 'Grupos Sociais')
keyword_to_subject['estratificação social'] = ('Sociologia', 'Estratificação Social')
keyword_to_subject['cidadania'] = ('Sociologia', 'Cidadania')


# 3. Carregar os embeddings e o dicionário de palavras-chave
try:
    print("Carregando embeddings e dicionário...")
    combined_embeddings = np.load('combined_embeddings.npy')
    keyword_dictionary = np.load('keyword_dictionary.npy', allow_pickle=True).item()
    keyword_list = list(keyword_dictionary.keys())
    
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    keyword_embeddings = model.encode(keyword_list)

except FileNotFoundError:
    print("❌ Erro: Arquivos de embeddings ou dicionário não encontrados.")
    print("Certifique-se de que os arquivos 'combined_embeddings.npy' e 'keyword_dictionary.npy' estão na pasta 'embendings'.")
    exit()

# 4. Calcular a similaridade
print("Calculando similaridade entre o texto das provas e as palavras-chave...")
scores = np.dot(combined_embeddings, keyword_embeddings.T)

# 5. Analisar e contar as ocorrências
top_n = 5
submatter_counts = defaultdict(int)

for i in range(scores.shape[0]):
    scores_tensor = torch.from_numpy(scores[i])
    top_scores, top_indices = torch.topk(scores_tensor, k=top_n)

    for j in range(top_n):
        score = top_scores[j].item()
        if score > 0.2:
            keyword = keyword_list[top_indices[j]]
            if keyword in keyword_to_subject:
                submatter = keyword_to_subject[keyword][1]
                submatter_counts[submatter] += 1

# Remover submatérias com zero ocorrências
submatter_counts = {k: v for k, v in submatter_counts.items() if v > 0}

# 6. Preparar dados para o gráfico
sorted_submatters = sorted(submatter_counts.items(), key=lambda item: item[1], reverse=True)
labels = [item[0] for item in sorted_submatters]
counts = [item[1] for item in sorted_submatters]

# 7. Criar e mostrar o gráfico
plt.style.use('ggplot')
plt.figure(figsize=(14, 12))
plt.barh(labels, counts, color='teal')
plt.xlabel("Número de Ocorrências (24 Provas)", fontsize=12)
plt.ylabel("Submatéria", fontsize=12)
plt.title("Guia de Estudos PAS 1: Tópicos Mais Frequentes", fontsize=16, pad=20)
plt.gca().invert_yaxis()  # Inverte o eixo Y para colocar a maior barra no topo

# Adicionar os valores nas barras para maior clareza
for index, value in enumerate(counts):
    plt.text(value, index, f' {value}', va='center')

plt.tight_layout()
plt.show()

print("O gráfico foi gerado com sucesso!")
print("Uma nova janela com a visualização do gráfico será aberta.")
