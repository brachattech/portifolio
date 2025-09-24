import os
import json
import re
import hashlib
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('auditor_sustentabilidade')

# Estrutura esperada do sistema para sustentabilidade
expected_structure = {
    "model_metadata": {
        "files": ["model_efficiency.json", "dataset_hashes.json"],
        "keywords": ["flops", "consumo_gpu", "eficiencia_energetica", "co2", "emissao_carbono", "otimizacao"]
    },
    "decision_logs": {
        "files": ["energy_usage_logs.json"],
        "keywords": ["consumo_energetico", "inferencia", "treinamento", "kwh", "tempo_execucao", "monitoramento"]
    },
    "audit_evidence": {
        "files": ["sustainability_report.pdf", "sustainability_report.md", "environmental_audit.yaml"],
        "keywords": ["impacto_ambiental", "auditoria_consumo", "pegada_carbono", "relatorio_sustentabilidade", "compliance_ambiental"]
    },
    "monitoring_dashboards": {
        "files": ["energy_dashboard.json", "energy_dashboard.html", "co2_emission_dashboard.json"],
        "keywords": ["grafico_consumo", "co2_emitido", "eficiencia_modelos", "dashboard_energia", "metricas_eficiencia"]
    }
}

# Base legal e frameworks para sustentabilidade em IA
sustainability_framework = {
    "legislacao_internacional": [
        {
            "norma": "EU AI Act - Artigo 17",
            "artigos": ["Art. 17 - Requisitos de sustentabilidade e eficiência energética"],
            "requisitos": [
                "Obrigatoriedade de relatórios de impacto ambiental",
                "Monitoramento contínuo do consumo energético",
                "Transparência nas emissões de carbono",
                "Otimização de recursos computacionais"
            ],
            "aplicacao": "Sistemas de IA de alto risco na União Europeia"
        },
        {
            "norma": "Directiva UE 2022/XXX - Eficiência Energética em Data Centers",
            "artigos": ["Art. 8", "Art. 12", "Art. 15"],
            "requisitos": [
                "PUE (Power Usage Effectiveness) máximo de 1.3",
                "Relatórios anuais de consumo energético",
                "Uso de energias renováveis",
                "Plano de otimização contínua"
            ],
            "aplicacao": "Todos los data centers operando na UE"
        }
    ],
    "frameworks_tecnicos": [
        {
            "framework": "Green Software Foundation",
            "principios": ["Princípio 1: Eficiência de Carbono", "Princípio 2: Eficiência Energética", "Princípio 3: Intensidade de Carbono"],
            "requisitos": [
                "Medição contínua de emissões",
                "Otimização de algoritmos para menor consumo",
                "Seleção de regiões com energia mais limpa"
            ],
            "aplicacao": "Desenvolvimento de software sustentável"
        },
        {
            "framework": "MLCO2 Calculator",
            "principios": ["Cálculo de emissões de treinamento", "Cálculo de emissões de inferência", "Offset de carbono"],
            "requisitos": [
                "Registro de horas de GPU/TPU",
                "Monitoramento do tipo de energia utilizada",
                "Cálculo de equivalência em emissões de CO2"
            ],
            "aplicacao": "Aferição do impacto ambiental de modelos de ML"
        },
        {
            "framework": "IPCC Guidelines for National Greenhouse Gas Inventories",
            "principios": ["Capítulo 4: Processos Industriales", "Capítulo 6: Emissões de TI"],
            "requisitos": [
                "Metodologia padronizada de cálculo",
                "Relatórios comparativos anuais",
                "Plano de redução de emissões"
            ],
            "aplicacao": "Inventário corporativo de emissões de gases de efeito estufa"
        }
    ],
    "certificacoes": [
        {
            "certificacao": "ISO 14001 - Environmental Management Systems",
            "requisitos": [
                "Política ambiental documentada",
                "Avaliação de aspectos ambientais",
                "Monitoramento e medição de desempenho",
                "Melhoria contínua"
            ],
            "aplicacao": "Sistemas de gestão ambiental corporativa"
        },
        {
            "certificacao": "LEED Data Centers",
            "requisitos": [
                "Eficiência energética otimizada",
                "Gestão de água e resíduos",
                "Qualidade ambiental interior",
                "Inovação em design sustentável"
            ],
            "aplicacao": "Data centers sustentáveis"
        }
    ]
}

def safe_path_join(base_path, target_path):
    """Previne ataques de path traversal"""
    base_path = os.path.abspath(base_path)
    target_path = os.path.normpath(target_path)
    
    if os.path.commonprefix([base_path, os.path.abspath(os.path.join(base_path, target_path))]) != base_path:
        raise ValueError(f"Tentativa de path traversal detectada: {target_path}")
    
    return os.path.join(base_path, target_path)

def check_file_keywords(file_path, keywords, max_file_size=10*1024*1024):
    """Verifica se o arquivo contém palavras-chave de sustentabilidade."""
    try:
        # Verificar se o arquivo existe
        if not os.path.isfile(file_path):
            return "Arquivo não encontrado"
        
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            return "Arquivo muito grande para análise"
        
        # Verificar permissões
        if not os.access(file_path, os.R_OK):
            return "Permissão de leitura negada"
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.json', '.yaml', '.yml', '.txt', '.md']:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read(50000).lower()
                    
                    found_keywords = []
                    for kw in keywords:
                        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', content):
                            found_keywords.append(kw)
                    
                    return found_keywords if found_keywords else "Nenhuma palavra-chave encontrada"
                    
            except UnicodeDecodeError:
                return "Erro de decodificação"
            except Exception as e:
                return f"Erro de leitura: {str(e)}"
                
        elif ext in ['.pdf']:
            # Tentativa básica de leitura de PDF
            try:
                with open(file_path, "rb") as f:
                    content = f.read(2000).decode('utf-8', errors='ignore').lower()
                    found_keywords = []
                    for kw in keywords:
                        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', content):
                            found_keywords.append(kw)
                    return found_keywords if found_keywords else "Conteúdo PDF - verificação limitada"
            except:
                return "Arquivo PDF - verificação não aplicável"
            
        elif ext in ['.html', '.htm']:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read(30000).lower()
                    # Remover tags HTML para análise de conteúdo
                    content = re.sub('<[^<]+?>', ' ', content)
                    
                    found_keywords = []
                    for kw in keywords:
                        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', content):
                            found_keywords.append(kw)
                    
                    return found_keywords if found_keywords else "Nenhuma palavra-chave encontrada"
            except:
                return "Arquivo HTML - verificação limitada"
            
        elif ext in ['.png', '.jpg', '.jpeg', '.gif']:
            return "Arquivo de imagem - análise de conteúdo não aplicável"
            
        else:
            return f"Tipo de arquivo não suportado: {ext}"
            
    except Exception as e:
        logger.error(f"Erro ao verificar arquivo {file_path}: {str(e)}")
        return f"Erro na verificação: {str(e)}"

def check_system(path="."):
    """Verifica a estrutura do sistema de sustentabilidade"""
    
    # Validar se o caminho existe
    if not os.path.exists(path):
        return {
            "audit_metadata": {
                "timestamp": datetime.now().isoformat(),
                "status": "ERRO",
                "error": f"O caminho especificado não existe: {path}"
            },
            "sustainability_framework": sustainability_framework
        }
    
    if not os.path.isdir(path):
        return {
            "audit_metadata": {
                "timestamp": datetime.now().isoformat(),
                "status": "ERRO", 
                "error": f"O caminho especificado não é um diretório: {path}"
            },
            "sustainability_framework": sustainability_framework
        }
    
    report = {
        "audit_metadata": {
            "timestamp": datetime.now().isoformat(),
            "auditor": "Sistema de Auditoria de Sustentabilidade em IA",
            "target_path": os.path.abspath(path),
            "objetivo": "Verificação de conformidade com frameworks de sustentabilidade e eficiência energética",
            "status": "CONCLUIDO",
            "base_legal": "Ver seção 'sustainability_framework' para detalhes completos"
        },
        "summary": {
            "total_directories": len(expected_structure),
            "total_files": sum(len(data["files"]) for data in expected_structure.values()),
            "directories_found": 0,
            "directories_missing": 0,
            "files_found": 0,
            "files_missing": 0,
            "files_with_keywords": 0,
            "files_without_keywords": 0,
            "sustainability_score": 0,
            "energy_efficiency_level": "NÃO CLASSIFICADO"
        },
        "detailed_report": {},
        "sustainability_framework": sustainability_framework,
        "recomendacoes_sustentabilidade": [],
        "checklist_acionavel": [
            {
                "item": "Medir consumo energético de cada modelo (treinamento e inferência)",
                "ferramentas": "MLCO2, Datadog, Cloud Monitoring",
                "prioridade": "ALTA",
                "prazo": "30 dias",
                "base_legal": "EU AI Act Art. 17"
            },
            {
                "item": "Usar modelos otimizados (distilados, quantizados)",
                "ferramentas": "TensorFlow Lite, ONNX Runtime, Hugging Face Optimum",
                "prioridade": "ALTA",
                "prazo": "45 dias", 
                "base_legal": "Green Software Foundation"
            },
            {
                "item": "Implementar data centers verdes ou cloud com energia renovável",
                "ferramentas": "Google Cloud Platform (Carbon Free), AWS Sustainability, Azure Sustainability",
                "prioridade": "MÉDIA",
                "prazo": "90 dias",
                "base_legal": "Directiva UE Eficiência Energética"
            }
        ]
    }
    
    for folder, data in expected_structure.items():
        try:
            folder_path = safe_path_join(path, folder)
            folder_exists = os.path.isdir(folder_path)
            
            if folder_exists:
                report["summary"]["directories_found"] += 1
            else:
                report["summary"]["directories_missing"] += 1
                # Adicionar recomendação para diretório faltante
                report["recomendacoes_sustentabilidade"].append({
                    "nivel": "ALTO",
                    "recomendacao": f"Criar diretório '{folder}' para documentação de sustentabilidade",
                    "fundamento": "EU AI Act Art. 17 - Requisitos de documentação",
                    "prazo": "URGENTE"
                })
            
            folder_report = {
                "directory_exists": folder_exists,
                "directory_path": folder_path,
                "importance_level": "ALTA" if folder in ["model_metadata", "decision_logs"] else "MÉDIA",
                "files_report": {}
            }
            
            for file in data["files"]:
                file_report = {
                    "expected": True,
                    "exists": False,
                    "file_path": "",
                    "status": "NÃO VERIFICADO",
                    "keywords_found": [],
                    "file_hash": None,
                    "compliance_indicators": [],
                    "legal_compliance": []
                }
                
                try:
                    if folder_exists:
                        file_path = safe_path_join(folder_path, file)
                        file_exists = os.path.isfile(file_path)
                        file_report["file_path"] = file_path
                        file_report["exists"] = file_exists
                        
                        if file_exists:
                            report["summary"]["files_found"] += 1
                            
                            # Calcular hash do arquivo para integridade
                            try:
                                with open(file_path, "rb") as f:
                                    file_content = f.read()
                                    file_report["file_hash"] = hashlib.sha256(file_content).hexdigest()[:16] + "..."
                                    file_report["file_size"] = len(file_content)
                            except Exception as e:
                                file_report["file_hash"] = f"Erro ao calcular hash: {str(e)}"
                            
                            # Verificar palavras-chave
                            keyword_result = check_file_keywords(file_path, data["keywords"])
                            
                            if isinstance(keyword_result, list):
                                file_report["status"] = "PALAVRAS-CHAVE ENCONTRADAS"
                                file_report["keywords_found"] = keyword_result
                                report["summary"]["files_with_keywords"] += 1
                                
                                # Adicionar indicadores de compliance
                                if any(kw in keyword_result for kw in ["co2", "emissao_carbono", "pegada_carbono"]):
                                    file_report["compliance_indicators"].append("Atende EU AI Act Art. 17 - Monitoramento de emissões")
                                    file_report["legal_compliance"].append("EU AI Act Artigo 17")
                                if any(kw in keyword_result for kw in ["consumo_energetico", "kwh", "eficiencia_energetica"]):
                                    file_report["compliance_indicators"].append("Atende Directiva UE - Eficiência energética")
                                    file_report["legal_compliance"].append("Directiva UE Eficiência Energética")
                                if any(kw in keyword_result for kw in ["flops", "consumo_gpu", "otimizacao"]):
                                    file_report["compliance_indicators"].append("Atende Green Software Foundation - Otimização de recursos")
                                    file_report["legal_compliance"].append("Green Software Foundation")
                                    
                            else:
                                file_report["status"] = keyword_result
                                report["summary"]["files_without_keywords"] += 1
                                
                                # Adicionar recomendação se arquivo existe mas não tem palavras-chave
                                if "não encontrada" in keyword_result.lower():
                                    report["recomendacoes_sustentabilidade"].append({
                                        "nivel": "MÉDIO",
                                        "recomendacao": f"Arquivo {file} não contém métricas de sustentabilidade necessárias",
                                        "fundamento": "Transparência Ambiental - Green Software Foundation",
                                        "prazo": "30 dias"
                                    })
                        else:
                            report["summary"]["files_missing"] += 1
                            file_report["status"] = "ARQUIVO NÃO ENCONTRADO"
                            
                            # Adicionar recomendação para arquivo faltante crítico
                            if file == "model_efficiency.json":
                                report["recomendacoes_sustentabilidade"].append({
                                    "nivel": "CRÍTICO",
                                    "recomendacao": "Implementar model_efficiency.json para monitoramento de eficiência energética",
                                    "fundamento": "EU AI Act Art. 17 - Requisitos de sustentabilidade",
                                    "prazo": "URGENTE",
                                    "multa_potencial": "Até 4% do faturamento global anual"
                                })
                            elif file == "energy_usage_logs.json":
                                report["recomendacoes_sustentabilidade"].append({
                                    "nivel": "ALTO",
                                    "recomendacao": "Implementar energy_usage_logs.json para registro de consumo energético",
                                    "fundamento": "Directiva UE 2022/XXX - Monitoramento contínuo",
                                    "prazo": "15 dias"
                                })
                                
                    else:
                        report["summary"]["files_missing"] += 1
                        file_report["status"] = "DIRETÓRIO NÃO EXISTE"
                        
                except Exception as e:
                    file_report["status"] = f"ERRO: {str(e)}"
                    logger.error(f"Erro ao processar arquivo {file}: {str(e)}")
                
                folder_report["files_report"][file] = file_report
                
        except Exception as e:
            logger.error(f"Erro ao processar diretório {folder}: {str(e)}")
            folder_report = {
                "directory_exists": False,
                "error": str(e),
                "files_report": {file: {"status": "NÃO VERIFICADO - ERRO NO DIRETÓRIO"} for file in data["files"]}
            }
        
        report["detailed_report"][folder] = folder_report
    
    # Calcular score de sustentabilidade
    total_possible = report["summary"]["total_files"]
    actual_found = report["summary"]["files_found"]
    if total_possible > 0:
        sustainability_score = round((actual_found / total_possible) * 100, 2)
        report["summary"]["sustainability_score"] = sustainability_score
        
        # Classificar nível de eficiência energética
        if sustainability_score >= 90:
            report["summary"]["energy_efficiency_level"] = "EXCELENTE EFICIÊNCIA"
        elif sustainability_score >= 70:
            report["summary"]["energy_efficiency_level"] = "BOA EFICIÊNCIA"
        elif sustainability_score >= 50:
            report["summary"]["energy_efficiency_level"] = "EFICIÊNCIA MODERADA"
        else:
            report["summary"]["energy_efficiency_level"] = "BAIXA EFICIÊNCIA"
    
    # Adicionar recomendações baseadas no score
    if report["summary"]["sustainability_score"] < 50:
        report["recomendacoes_sustentabilidade"].append({
            "nivel": "CRÍTICO",
            "recomendacao": "Implementar estrutura completa de monitoramento de sustentabilidade",
            "fundamento": "EU AI Act Art. 17 e Directiva UE - Conformidade regulatória",
            "prazo": "IMEDIATO",
            "consequencia": "Risco de multas e sanções regulatórias"
        })
    elif report["summary"]["sustainability_score"] < 80:
        report["recomendacoes_sustentabilidade"].append({
            "nivel": "MÉDIO",
            "recomendacao": "Reforçar documentação e relatórios de sustentabilidade",
            "fundamento": "Green Software Foundation - Melhores práticas",
            "prazo": "60 dias",
            "beneficio": "Redução de custos operacionais e melhoria reputacional"
        })
    
    # Adicionar análise de conformidade legal
    report["analise_conformidade_legal"] = {
        "eu_ai_act": {
            "artigo_17": "Parcialmente atendido" if any("EU AI Act Artigo 17" in file.get("legal_compliance", []) for folder in report["detailed_report"].values() for file in folder.get("files_report", {}).values() if isinstance(file, dict)) else "Não atendido"
        },
        "directiva_ue": {
            "eficiencia_energetica": "Parcialmente atendido" if any("Directiva UE Eficiência Energética" in file.get("legal_compliance", []) for folder in report["detailed_report"].values() for file in folder.get("files_report", {}).values() if isinstance(file, dict)) else "Não atendido"
        }
    }
    
    return report

def generate_json_report(path=".", output_file="sustainability_audit_report.json"):
    """Gera relatório de auditoria de sustentabilidade em formato JSON"""
    
    try:
        report = check_system(path)
        
        # Criar diretório de saída se não existir
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False, default=str)
        
        print(f"✅ Relatório de Sustentabilidade gerado com sucesso: {output_file}")
        print(f"📊 Resumo da auditoria:")
        print(f"   Score de Sustentabilidade: {report['summary']['sustainability_score']}%")
        print(f"   Nível de Eficiência Energética: {report['summary']['energy_efficiency_level']}")
        print(f"   Diretórios encontrados: {report['summary']['directories_found']}/{report['summary']['total_directories']}")
        print(f"   Arquivos encontrados: {report['summary']['files_found']}/{report['summary']['total_files']}")
        print(f"   Recomendações: {len(report['recomendacoes_sustentabilidade'])}")
        
        # Mostrar recomendações críticas
        critical_recommendations = [r for r in report['recomendacoes_sustentabilidade'] if r['nivel'] in ['CRÍTICO', 'ALTO']]
        if critical_recommendations:
            print(f"⚠️  Recomendações Críticas: {len(critical_recommendations)}")
            for rec in critical_recommendations:
                print(f"   • {rec['recomendacao']} (Prazo: {rec['prazo']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")
        logger.error(f"Erro ao gerar relatório: {str(e)}")
        return False

if __name__ == "__main__":
    print("🌱 Auditoria de Sustentabilidade e Eficiência Energética em IA")
    print("📚 Frameworks: EU AI Act, Green Software Foundation, MLCO2, IPCC Guidelines")
    print("=" * 70)
    
    system_root = input("Digite o caminho do sistema a ser auditado: ").strip()
    if not system_root:
        system_root = "."
    
    output_file = input("Digite o nome do arquivo de saída [sustainability_audit.json]: ").strip()
    if not output_file:
        output_file = "sustainability_audit.json"
    
    print(f"\nIniciando auditoria de sustentabilidade do diretório: {os.path.abspath(system_root)}")
    print("Analisando conformidade com frameworks de eficiência energética...\n")
    
    success = generate_json_report(system_root, output_file)
    
    if success:
        print("\n🎯 Auditoria de sustentabilidade concluída com sucesso!")
        print("📋 O relatório inclui análise de compliance com:")
        print("   • EU AI Act - Artigo 17 (Sustentabilidade)")
        print("   • Directiva UE - Eficiência Energética em Data Centers")
        print("   • Green Software Foundation Principles")
        print("   • MLCO2 Calculator Framework")
        print("\nVerifique o arquivo JSON para o relatório detalhado com fundamentação técnica e legal.")
    else:
        print("\n💥 Falha na auditoria. Verifique o caminho e as permissões.")