import numpy as np
from collections import Counter, defaultdict
import torch
from sentence_transformers import SentenceTransformer

# 1. Definição da estrutura de matérias e submatérias
# Essa estrutura é a mesma que você forneceu.
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
        "pré-socráticos": ["teses básicas", "cosmologia"],
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
    
    # Carregar modelo para embeddings das keywords
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    keyword_embeddings = model.encode(keyword_list)

except FileNotFoundError:
    print("❌ Erro: Arquivos de embeddings ou dicionário não encontrados.")
    print("Certifique-se de que os arquivos 'combined_embeddings.npy' e 'keyword_dictionary.npy' estão na pasta 'embendings'.")
    exit()

# 4. Calcular a similaridade
print("Calculando similaridade entre o texto das provas e as palavras-chave...")
# Usa o produto escalar para a similaridade do cosseno
scores = np.dot(combined_embeddings, keyword_embeddings.T)

# 5. Analisar e contar as ocorrências
top_n = 5
submatter_counts = defaultdict(int)
total_relevant_keywords = 0

for i in range(scores.shape[0]):
    scores_tensor = torch.from_numpy(scores[i])
    top_scores, top_indices = torch.topk(scores_tensor, k=top_n)

    for j in range(top_n):
        score = top_scores[j].item()
        # Considera apenas scores acima de um limiar
        if score > 0.2:
            keyword = keyword_list[top_indices[j]]
            if keyword in keyword_to_subject:
                submatter = keyword_to_subject[keyword][1]
                submatter_counts[submatter] += 1
                total_relevant_keywords += 1

# 6. Exibir o relatório
print("\n✅ Relatório de Distribuição de Conteúdo (24 Provas):")
print("-----------------------------------------------------")

for subject, submatters in keywords_hierarchy.items():
    print(f"\n--- {subject.capitalize()} ---")
    subject_total = sum(submatter_counts[sm.capitalize()] for sm in submatters.keys())
    
    if subject_total > 0:
        for submatter, keywords in submatters.items():
            count = submatter_counts[submatter.capitalize()]
            if count > 0:
                percentage = (count / total_relevant_keywords) * 100
                print(f"  - {submatter.capitalize()}: {percentage:.2f}% ({count} ocorrência{'s' if count > 1 else ''})")
    else:
        print("  - Nenhuma submatéria relevante encontrada.")
    # Adiciona a categoria geral se houver
    if subject == "geral" and "Conteúdos Fundamentais" in submatter_counts:
        count = submatter_counts["Conteúdos Fundamentais"]
        percentage = (count / total_relevant_keywords) * 100
        print(f"  - Conteúdos Fundamentais: {percentage:.2f}% ({count} ocorrência{'s' if count > 1 else ''})")
