import os
import json
import re
import hashlib
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('auditor_risco_ia')

# Estruturas por nível de risco conforme EU AI Act
risk_structures = {
    "unacceptable_risk": {
        "name": "Risco Inaceitável",
        "description": "Sistemas proibidos: manipulação subliminar, exploração de vulnerabilidades, scoring social pelos governos",
        "requirements": {
            "model_metadata": {
                "files": ["prohibition_justification.json", "ethical_review.pdf", "legal_approval.yaml"],
                "keywords": ["prohibition_exception", "fundamental_rights", "ethical_waiver", "legal_authorization"]
            },
            "audit_evidence": {
                "files": ["government_approval.pdf", "ethical_board_review.md", "human_rights_assessment.pdf"],
                "keywords": ["national_security", "strict_necessity", "democratic_safeguards", "judicial_oversight"]
            }
        }
    },
    "high_risk": {
        "name": "Alto Risco",
        "description": "Sistemas críticos: infraestrutura, educação, emprego, serviços essenciais, aplicação da lei",
        "requirements": {
            "model_metadata": {
                "files": ["conformity_assessment.json", "risk_management.yaml", "data_governance.json", "quality_management.json"],
                "keywords": ["conformity_assessment", "risk_management", "data_governance", "quality_management"]
            },
            "decision_logs": {
                "files": ["human_oversight_logs.json", "incident_reports.json", "accuracy_metrics.json"],
                "keywords": ["human_oversight", "incident_reporting", "accuracy_metrics", "performance_monitoring"]
            },
            "audit_evidence": {
                "files": ["fundamental_rights_impact.pdf", "technical_documentation.pdf", "quality_management_certificate.pdf"],
                "keywords": ["fundamental_rights", "technical_documentation", "quality_management", "compliance_certificate"]
            },
            "monitoring_dashboards": {
                "files": ["risk_dashboard.html", "performance_monitoring.json", "compliance_tracking.yaml"],
                "keywords": ["risk_monitoring", "performance_tracking", "compliance_status", "real_time_alerts"]
            }
        }
    },
    "limited_risk": {
        "name": "Risco Limitado",
        "description": "Sistemas com obrigações de transparência: chatbots, deepfakes, emotion recognition",
        "requirements": {
            "model_metadata": {
                "files": ["transparency_disclosure.json", "user_communication.yaml"],
                "keywords": ["transparency_disclosure", "ai_generated", "user_notification", "communication_protocol"]
            },
            "audit_evidence": {
                "files": ["user_consent_records.json", "disclosure_compliance.pdf"],
                "keywords": ["user_consent", "disclosure_compliance", "transparency_verification"]
            }
        }
    },
    "minimal_risk": {
        "name": "Risco Mínimo",
        "description": "Sistemas livres de uso: filtros de spam, recomendação de conteúdo, jogos",
        "requirements": {
            "model_metadata": {
                "files": ["voluntary_code_compliance.json"],
                "keywords": ["voluntary_compliance", "ethical_guidelines", "best_practices"]
            }
        }
    }
}

# Framework legal baseado no EU AI Act
legal_framework = {
    "eu_ai_act": {
        "title": "Regulation (EU) 2024/XXXX on Artificial Intelligence",
        "risk_levels": {
            "unacceptable_risk": {
                "article": "Article 5",
                "prohibitions": [
                    "Subliminal manipulation",
                    "Exploitation of vulnerabilities",
                    "Social scoring by public authorities",
                    "Real-time remote biometric identification in public spaces"
                ]
            },
            "high_risk": {
                "article": "Articles 6-51",
                "requirements": [
                    "Fundamental rights impact assessment",
                    "Quality management system",
                    "Data governance",
                    "Technical documentation",
                    "Human oversight",
                    "Accuracy and cybersecurity"
                ]
            },
            "limited_risk": {
                "article": "Article 52",
                "requirements": [
                    "Transparency obligations",
                    "User notification",
                    "Disclosure of AI-generated content"
                ]
            },
            "minimal_risk": {
                "article": "No specific obligations",
                "requirements": [
                    "Voluntary compliance with codes of conduct"
                ]
            }
        }
    }
}

def detect_ai_risk_level(system_path):
    """
    Detecta automaticamente o nível de risco do sistema de IA
    baseado em heurísticas e metadados encontrados
    """
    risk_indicators = {
        "unacceptable_risk": 0,
        "high_risk": 0,
        "limited_risk": 0,
        "minimal_risk": 0
    }
    
    # Heurísticas para detecção de nível de risco
    try:
        # Verificar se há menção a aplicações de alto risco
        for root, dirs, files in os.walk(system_path):
            for file in files:
                if file.endswith(('.json', '.yaml', '.yml', '.md', '.txt')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            
                            # Indicadores de risco inaceitável
                            if any(keyword in content for keyword in ['social_scoring', 'biometric_identification', 'subliminal', 'exploitation']):
                                risk_indicators["unacceptable_risk"] += 3
                                
                            # Indicadores de alto risco
                            if any(keyword in content for keyword in ['critical_infrastructure', 'education', 'employment', 'law_enforcement', 'medical_device']):
                                risk_indicators["high_risk"] += 2
                                
                            # Indicadores de risco limitado
                            if any(keyword in content for keyword in ['chatbot', 'deepfake', 'emotion_recognition', 'transparency_disclosure']):
                                risk_indicators["limited_risk"] += 1
                                
                    except:
                        continue
        
        # Determinar nível de risco predominante
        max_risk = max(risk_indicators, key=risk_indicators.get)
        
        # Se nenhum indicador forte, assumir alto risco por padrão (approach conservador)
        if risk_indicators[max_risk] == 0:
            return "high_risk"
            
        return max_risk
        
    except Exception as e:
        logger.warning(f"Erro na detecção automática de risco: {e}")
        return "high_risk"  # Padrão conservador

def safe_path_join(base_path, target_path):
    """Previne ataques de path traversal"""
    base_path = os.path.abspath(base_path)
    target_path = os.path.normpath(target_path)
    
    if os.path.commonprefix([base_path, os.path.abspath(os.path.join(base_path, target_path))]) != base_path:
        raise ValueError(f"Tentativa de path traversal detectada: {target_path}")
    
    return os.path.join(base_path, target_path)

def check_file_keywords(file_path, keywords, max_file_size=10*1024*1024):
    """Verifica se o arquivo contém palavras-chave relevantes."""
    try:
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            return "Arquivo muito grande para análise"
        
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
                
        elif ext in ['.pdf']:
            # Verificação básica de PDF
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
                    content = re.sub('<[^<]+?>', ' ', content)
                    
                    found_keywords = []
                    for kw in keywords:
                        if re.search(r'\b' + re.escape(kw.lower()) + r'\b', content):
                            found_keywords.append(kw)
                    
                    return found_keywords if found_keywords else "Nenhuma palavra-chave encontrada"
            except:
                return "Arquivo HTML - verificação limitada"
            
        else:
            return f"Tipo de arquivo não suportado: {ext}"
            
    except Exception as e:
        return f"Erro na verificação: {str(e)}"

def check_system(path="."):
    """Verifica a estrutura do sistema baseado no nível de risco detectado"""
    
    if not os.path.exists(path):
        return {
            "audit_metadata": {
                "timestamp": datetime.now().isoformat(),
                "status": "ERRO",
                "error": f"O caminho especificado não existe: {path}"
            },
            "legal_framework": legal_framework
        }
    
    if not os.path.isdir(path):
        return {
            "audit_metadata": {
                "timestamp": datetime.now().isoformat(),
                "status": "ERRO", 
                "error": f"O caminho especificado não é um diretório: {path}"
            },
            "legal_framework": legal_framework
        }
    
    # Detectar nível de risco automaticamente
    risk_level = detect_ai_risk_level(path)
    risk_config = risk_structures[risk_level]
    
    report = {
        "audit_metadata": {
            "timestamp": datetime.now().isoformat(),
            "auditor": "Sistema de Auditoria Baseada em Risco de IA",
            "target_path": os.path.abspath(path),
            "detected_risk_level": risk_level,
            "risk_level_name": risk_config["name"],
            "risk_description": risk_config["description"],
            "status": "CONCLUIDO",
            "base_legal": "EU AI Act - Regulamento Europeu de Inteligência Artificial"
        },
        "summary": {
            "total_directories": len(risk_config["requirements"]),
            "total_files": sum(len(data["files"]) for data in risk_config["requirements"].values()),
            "directories_found": 0,
            "directories_missing": 0,
            "files_found": 0,
            "files_missing": 0,
            "files_with_keywords": 0,
            "files_without_keywords": 0,
            "compliance_score": 0,
            "risk_assessment": "NÃO CLASSIFICADO"
        },
        "detailed_report": {},
        "legal_framework": {
            "applicable_regulation": legal_framework["eu_ai_act"],
            "risk_level_requirements": legal_framework["eu_ai_act"]["risk_levels"][risk_level]
        },
        "recommendations": [],
        "compliance_requirements": []
    }
    
    # Adicionar requisitos específicos do nível de risco
    if risk_level == "high_risk":
        report["compliance_requirements"] = [
            "Realizar avaliação de impacto em direitos fundamentais",
            "Implementar sistema de gestão de qualidade",
            "Manter documentação técnica completa",
            "Garantir supervisão humana adequada",
            "Implementar medidas de precisão e cybersecurity"
        ]
    elif risk_level == "limited_risk":
        report["compliance_requirements"] = [
            "Garantir transparência e divulgação adequada",
            "Notificar usuários sobre interação com IA",
            "Disclosure de conteúdo gerado por IA"
        ]
    elif risk_level == "unacceptable_risk":
        report["compliance_requirements"] = [
            "Obter autorização excepcional específica",
            "Garantir salvaguardas democráticas adequadas",
            "Manter supervisão judicial contínua"
        ]
    
    for folder, data in risk_config["requirements"].items():
        try:
            folder_path = safe_path_join(path, folder)
            folder_exists = os.path.isdir(folder_path)
            
            if folder_exists:
                report["summary"]["directories_found"] += 1
            else:
                report["summary"]["directories_missing"] += 1
            
            folder_report = {
                "directory_exists": folder_exists,
                "directory_path": folder_path,
                "compliance_level": "OBRIGATÓRIO" if risk_level in ["high_risk", "unacceptable_risk"] else "RECOMENDADO",
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
                    "compliance_indicators": []
                }
                
                try:
                    if folder_exists:
                        file_path = safe_path_join(folder_path, file)
                        file_exists = os.path.isfile(file_path)
                        file_report["file_path"] = file_path
                        file_report["exists"] = file_exists
                        
                        if file_exists:
                            report["summary"]["files_found"] += 1
                            
                            # Calcular hash do arquivo
                            try:
                                with open(file_path, "rb") as f:
                                    file_report["file_hash"] = hashlib.sha256(f.read()).hexdigest()[:16] + "..."
                            except:
                                file_report["file_hash"] = "Erro ao calcular hash"
                            
                            # Verificar palavras-chave
                            keyword_result = check_file_keywords(file_path, data["keywords"])
                            
                            if isinstance(keyword_result, list):
                                file_report["status"] = "PALAVRAS-CHAVE ENCONTRADAS"
                                file_report["keywords_found"] = keyword_result
                                report["summary"]["files_with_keywords"] += 1
                                
                                # Adicionar indicadores de compliance baseados no risco
                                if risk_level == "high_risk":
                                    if any(kw in keyword_result for kw in ["risk_management", "quality_management"]):
                                        file_report["compliance_indicators"].append("Atende EU AI Act - Gestão de Risco e Qualidade")
                                    if any(kw in keyword_result for kw in ["human_oversight", "incident_reporting"]):
                                        file_report["compliance_indicators"].append("Atende EU AI Act - Supervisão Humana")
                                        
                            else:
                                file_report["status"] = keyword_result
                                report["summary"]["files_without_keywords"] += 1
                        else:
                            report["summary"]["files_missing"] += 1
                            file_report["status"] = "ARQUIVO NÃO ENCONTRADO"
                            
                            # Adicionar recomendações baseadas no risco
                            if risk_level == "high_risk":
                                report["recommendations"].append({
                                    "level": "ALTO",
                                    "recommendation": f"Implementar {file} para conformidade com EU AI Act",
                                    "deadline": "URGENTE",
                                    "legal_basis": f"EU AI Act {legal_framework['eu_ai_act']['risk_levels']['high_risk']['article']}"
                                })
                                
                    else:
                        report["summary"]["files_missing"] += 1
                        file_report["status"] = "DIRETÓRIO NÃO EXISTE"
                        
                except Exception as e:
                    file_report["status"] = f"ERRO: {str(e)}"
                
                folder_report["files_report"][file] = file_report
                
        except Exception as e:
            folder_report = {
                "directory_exists": False,
                "error": str(e),
                "files_report": {file: {"status": "NÃO VERIFICADO - ERRO NO DIRETÓRIO"} for file in data["files"]}
            }
        
        report["detailed_report"][folder] = folder_report
    
    # Calcular score de compliance
    total_possible = report["summary"]["total_files"]
    actual_found = report["summary"]["files_found"]
    if total_possible > 0:
        compliance_score = round((actual_found / total_possible) * 100, 2)
        report["summary"]["compliance_score"] = compliance_score
        
        # Classificar nível de risco baseado no compliance
        if compliance_score >= 90:
            report["summary"]["risk_assessment"] = "BAIXO RISCO"
        elif compliance_score >= 70:
            report["summary"]["risk_assessment"] = "RISCO MODERADO"
        elif compliance_score >= 50:
            report["summary"]["risk_assessment"] = "ALTO RISCO"
        else:
            report["summary"]["risk_assessment"] = "RISCO CRÍTICO"
    
    # Adicionar recomendações baseadas no nível de risco e compliance
    if report["summary"]["risk_assessment"] in ["ALTO RISCO", "RISCO CRÍTICO"]:
        report["recommendations"].append({
            "level": "CRÍTICO",
            "recommendation": "Implementar medidas urgentes de conformidade com EU AI Act",
            "deadline": "IMEDIATO",
            "legal_basis": "EU AI Act - Conformidade Mandatória"
        })
    
    return report

def generate_risk_based_report(path=".", output_file="risk_based_audit_report.json"):
    """Gera relatório de auditoria baseado em risco em formato JSON"""
    
    try:
        report = check_system(path)
        
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False, default=str)
        
        print(f"✅ Relatório Baseado em Risco gerado com sucesso: {output_file}")
        print(f"📊 Resumo da auditoria:")
        print(f"   Nível de Risco Detectado: {report['audit_metadata']['risk_level_name']}")
        print(f"   Score de Conformidade: {report['summary']['compliance_score']}%")
        print(f"   Avaliação de Risco: {report['summary']['risk_assessment']}")
        print(f"   Arquivos Encontrados: {report['summary']['files_found']}/{report['summary']['total_files']}")
        
        # Mostrar requisitos legais aplicáveis
        risk_level = report['audit_metadata']['detected_risk_level']
        legal_req = legal_framework['eu_ai_act']['risk_levels'][risk_level]
        print(f"📋 Requisitos Legais Aplicáveis ({legal_req['article']}):")
        for req in legal_req['requirements']:
            print(f"   • {req}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Auditoria de IA Baseada em Nível de Risco")
    print("📚 Framework: EU AI Act - Regulamento Europeu de IA")
    print("=" * 60)
    
    system_root = input("Digite o caminho do sistema a ser auditado: ").strip()
    if not system_root:
        system_root = "."
    
    output_file = input("Digite o nome do arquivo de saída [risk_audit.json]: ").strip()
    if not output_file:
        output_file = "risk_audit.json"
    
    print(f"\nIniciando auditoria baseada em risco do diretório: {os.path.abspath(system_root)}")
    print("Detectando nível de risco e aplicando requisitos correspondentes...\n")
    
    success = generate_risk_based_report(system_root, output_file)
    
    if success:
        print("\n🎯 Auditoria baseada em risco concluída com sucesso!")
        print("📋 O relatório considera:")
        print("   • Nível de risco automático detectado")
        print("   • Requisitos específicos do EU AI Act")
        print("   • Recomendações personalizadas por nível de risco")
        print("\nVerifique o arquivo JSON para análise detalhada.")
    else:
        print("\n💥 Falha na auditoria. Verifique o caminho e as permissões.")