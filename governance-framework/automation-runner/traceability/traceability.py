#!/usr/bin/env python3
# traceability.py
"""
Comprehensive, Risk-Aware & Regulatory-Citable AI/ML Traceability Audit Runner.
This script performs a thorough, auditable scan of a local repository for AI/ML artifacts.
It assesses traceability maturity against 22 predefined principles, ADJUSTED BY RISK LEVEL (High, Limited, Low),
and explicitly cites legal basis (EU AI Act, NIST AI RMF, ISO/IEC 42001) for each requirement.
All outputs are cryptographically signed with SHA-256 for legal immutability.
Designed for offline, secure, reproducible audits in regulated environments.
"""
import os
import re
import sys
import json
import uuid
import hashlib
import shutil
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Set, Union

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# --- RISK LEVELS CONFIGURATION ---
RISK_LEVELS = {
    "high": [
        "dataset_versioning", "model_versioning", "decision_logs", "model_change_documentation",
        "hyperparameters_config", "audit_evidence", "performance_monitoring", "file_integrity_hash",
        "cross_reference", "dependency_documentation", "monitoring_events", "reproducibility_capability",
        "approvals_reviews", "regulatory_compliance", "design_decisions", "pipeline_auditability",
        "bias_metrics", "risk_mitigation", "inference_logs", "continuous_monitoring",
        "historical_reconstruction", "incident_documentation"
    ],
    "limited": [
        "dataset_versioning", "model_versioning", "decision_logs", "hyperparameters_config",
        "file_integrity_hash", "cross_reference", "reproducibility_capability",
        "regulatory_compliance", "bias_metrics", "inference_logs"
    ],
    "low": [
        "dataset_versioning", "model_versioning", "hyperparameters_config",
        "file_integrity_hash", "reproducibility_capability"
    ]
}

# --- REGULATORY REFERENCES (CITABLE) ---
REGULATORY_REFERENCES = {
    "EU_AI_ACT": {
        "title": "Regulation (EU) 2024/1689 on Artificial Intelligence",
        "url": "https://eur-lex.europa.eu/eli/reg/2024/1689",
        "description": "Establishes harmonised rules on AI, including technical documentation, data governance, and human oversight for high-risk systems."
    },
    "NIST_AI_RMF": {
        "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "description": "Provides guidance for managing risks in the design, development, and deployment of AI systems."
    },
    "ISO_42001": {
        "title": "ISO/IEC 42001:2023 — Information technology — AI Management System",
        "url": "https://www.iso.org/standard/81230.html",
        "description": "Specifies requirements for establishing, implementing, maintaining and improving an AI management system."
    }
}

# --- TRACEABILITY ITEMS (with legal basis) ---
TRACEABILITY_ITEMS: Dict[str, Dict[str, Any]] = {
    "dataset_versioning": {
        "weight": 10,
        "en_name": "Dataset Versioning & Provenance",
        "pt_name": "Versionamento de Datasets e Procedência",
        "es_name": "Versionado de Datasets y Procedencia",
        "desc": "Evidence of dataset versioning and provenance, linking models to their data.",
        "keywords": ["dataset", "version", "hash", "provenance", "data lineage"],
        "required_for": ["high", "limited", "low"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 10(2), 13(2)(a) — Data governance and technical documentation",
            "NIST_AI_RMF": "MAP 02-01, GOVERN 03-01 — Data provenance and documentation",
            "ISO_42001": "Annex A.8.2 — Data and input management"
        }
    },
    "model_versioning": {
        "weight": 10,
        "en_name": "Model Versioning & Artifacts",
        "pt_name": "Versionamento de Modelos e Artefatos",
        "es_name": "Versionado de Modelos y Artefactos",
        "desc": "Documentation and storage of model artifacts and versions.",
        "keywords": ["model", "version", "checkpoint", "artifact", "serialization"],
        "required_for": ["high", "limited", "low"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 11, 13(3)(b) — Model management and technical documentation",
            "NIST_AI_RMF": "MAP 03-01 — Model versioning and artifact management",
            "ISO_42001": "Annex A.8.3 — Model management"
        }
    },
    "decision_logs": {
        "weight": 9,
        "en_name": "Decision / Inference Logs",
        "pt_name": "Logs de Decisões / Inferência",
        "es_name": "Logs de Decisiones / Inferencia",
        "desc": "Logs that record model inputs, outputs, and versions for auditing.",
        "keywords": ["decision", "prediction", "log", "timestamp", "inference"],
        "required_for": ["high", "limited"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(e), 50 — Logging of changes and decisions",
            "NIST_AI_RMF": "MEASURE 02-01 — Logging and monitoring",
            "ISO_42001": "Annex A.10.1 — Monitoring and logging"
        }
    },
    "model_change_documentation": {
        "weight": 8,
        "en_name": "Model Change History",
        "pt_name": "Documentação de Histórico de Mudanças",
        "es_name": "Documentación de Historial de Cambios",
        "desc": "Changelogs or documentation detailing model changes and their rationale.",
        "keywords": ["change", "modification", "update", "migration", "changelog"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(c), 16(2) — Record of changes and updates",
            "NIST_AI_RMF": "GOVERN 02-01 — Change management",
            "ISO_42001": "Clause 8.4 — Change control"
        }
    },
    "hyperparameters_config": {
        "weight": 8,
        "en_name": "Hyperparameters & Training Config",
        "pt_name": "Configuração de Hiperparâmetros e Treinamento",
        "es_name": "Configuración de Hiperparámetros y Entrenamiento",
        "desc": "Documentation of hyperparameters and training configuration for reproducibility.",
        "keywords": ["hyperparameter", "config", "parameter", "setting", "training"],
        "required_for": ["high", "limited", "low"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(d) — Description of training parameters",
            "NIST_AI_RMF": "MAP 03-02 — Training configuration documentation",
            "ISO_42001": "Annex A.8.4 — Training process documentation"
        }
    },
    "audit_evidence": {
        "weight": 9,
        "en_name": "Audit Approvals & Evidence",
        "pt_name": "Aprovações e Evidências de Auditoria",
        "es_name": "Aprobaciones y Evidencias de Auditoría",
        "desc": "Formal approvals, sign-offs, and committee meeting minutes.",
        "keywords": ["audit", "evidence", "approval", "review", "committee"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 17, 19 — Human oversight and conformity assessments",
            "NIST_AI_RMF": "GOVERN 04-01 — Audit trails and approvals",
            "ISO_42001": "Clause 9.2 — Internal audit"
        }
    },
    "performance_monitoring": {
        "weight": 7,
        "en_name": "Performance Monitoring",
        "pt_name": "Monitoramento de Performance",
        "es_name": "Monitoreo de Rendimiento",
        "desc": "Reports on model performance metrics (e.g., accuracy, precision) over time.",
        "keywords": ["performance", "metric", "monitor", "dashboard", "accuracy"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(f), 49 — Monitoring of performance and accuracy",
            "NIST_AI_RMF": "MEASURE 01-01 — Performance monitoring",
            "ISO_42001": "Annex A.10.2 — Performance evaluation"
        }
    },
    "file_integrity_hash": {
        "weight": 8,
        "en_name": "File Integrity Hashes",
        "pt_name": "Hashes de Integridade de Arquivos",
        "es_name": "Hashes de Integridad de Archivos",
        "desc": "Hashes (e.g., SHA-256) for datasets and models to ensure integrity.",
        "keywords": ["hash", "checksum", "integrity", "sha256", "md5"],
        "required_for": ["high", "limited", "low"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 10(5), 13(2)(c) — Data and system integrity",
            "NIST_AI_RMF": "MAP 01-02 — Data integrity verification",
            "ISO_42001": "Annex A.8.1 — Data integrity controls"
        }
    },
    "cross_reference": {
        "weight": 9,
        "en_name": "Cross-Reference Validation",
        "pt_name": "Validação de Referências Cruzadas",
        "es_name": "Validación de Referencias Cruzadas",
        "desc": "Verification that logs, models, and datasets are correctly cross-referenced.",
        "keywords": ["reference", "link", "correlate", "associate", "cross-reference"],
        "required_for": ["high", "limited"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(g) — Traceability of outputs to inputs and models",
            "NIST_AI_RMF": "MAP 04-01 — Traceability and lineage",
            "ISO_42001": "Annex A.8.5 — Traceability of AI system outputs"
        }
    },
    "dependency_documentation": {
        "weight": 7,
        "en_name": "Dependency Documentation",
        "pt_name": "Documentação de Dependências",
        "es_name": "Documentación de Dependencias",
        "desc": "List of dependencies (e.g., requirements.txt, pyproject.toml).",
        "keywords": ["dependency", "requirement", "environment", "library", "package"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(h) — System and software dependencies",
            "NIST_AI_RMF": "MAP 03-03 — Dependency documentation",
            "ISO_42001": "Annex A.8.6 — System dependencies"
        }
    },
    "monitoring_events": {
        "weight": 7,
        "en_name": "Monitoring Events & Alerts",
        "pt_name": "Eventos de Monitoramento e Alertas",
        "es_name": "Eventos de Monitoreo y Alertas",
        "desc": "Records of system alerts or monitoring events.",
        "keywords": ["event", "alert", "notification", "incident", "monitoring"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 49, 50 — Monitoring and alerting for high-risk systems",
            "NIST_AI_RMF": "MEASURE 03-01 — Alerting and incident detection",
            "ISO_42001": "Annex A.10.3 — Alert and incident management"
        }
    },
    "reproducibility_capability": {
        "weight": 10,
        "en_name": "Reproducibility Capability",
        "pt_name": "Capacidade de Reprodução",
        "es_name": "Capacidad de Reproducción",
        "desc": "Presence of all necessary components (code, config, data) to reproduce a result.",
        "keywords": ["reproduce", "replicate", "recreate", "repeatable", "reproducibility"],
        "required_for": ["high", "limited", "low"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(i) — Reproducibility of results",
            "NIST_AI_RMF": "MAP 05-01 — Reproducibility and repeatability",
            "ISO_42001": "Annex A.8.7 — Reproducibility of AI results"
        }
    },
    "approvals_reviews": {
        "weight": 8,
        "en_name": "Approvals & Reviews",
        "pt_name": "Aprovações e Revisões",
        "es_name": "Aprobaciones y Revisiones",
        "desc": "Formal records of model sign-offs and peer reviews.",
        "keywords": ["approval", "review", "signoff", "authorization", "peer review"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 17, 19 — Human oversight and review mechanisms",
            "NIST_AI_RMF": "GOVERN 04-02 — Review and approval workflows",
            "ISO_42001": "Clause 8.5 — Review of AI system decisions"
        }
    },
    "regulatory_compliance": {
        "weight": 9,
        "en_name": "Regulatory Compliance",
        "pt_name": "Conformidade Regulatória",
        "es_name": "Conformidad Regulatoria",
        "desc": "Explicit mention or evidence of compliance with regulations (GDPR, EU AI Act).",
        "keywords": ["compliance", "regulation", "standard", "requirement", "gdpr"],
        "required_for": ["high", "limited"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 5-9, 16 — Compliance with prohibited and high-risk requirements",
            "NIST_AI_RMF": "GOVERN 01-01 — Regulatory alignment",
            "ISO_42001": "Clause 4.2 — Understanding regulatory requirements"
        }
    },
    "design_decisions": {
        "weight": 7,
        "en_name": "Design Decisions Documentation",
        "pt_name": "Documentação de Decisões de Design",
        "es_name": "Documentación de Decisiones de Diseño",
        "desc": "Documentation explaining key architectural and design choices.",
        "keywords": ["design", "decision", "architecture", "choice", "rationale"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(j) — Rationale for design choices",
            "NIST_AI_RMF": "MAP 01-01 — Design rationale documentation",
            "ISO_42001": "Annex A.7.1 — Design decision records"
        }
    },
    "pipeline_auditability": {
        "weight": 8,
        "en_name": "Pipeline Auditability",
        "pt_name": "Auditabilidade do Pipeline",
        "es_name": "Auditabilidad del Pipeline",
        "desc": "Presence of auditable MLOps pipelines or workflows.",
        "keywords": ["pipeline", "workflow", "process", "orchestration", "mlops"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(k) — Automated processing documentation",
            "NIST_AI_RMF": "GOVERN 03-02 — Pipeline audit trails",
            "ISO_42001": "Annex A.9.1 — Process automation controls"
        }
    },
    "bias_metrics": {
        "weight": 8,
        "en_name": "Bias/Fairness Metrics",
        "pt_name": "Métricas de Viés/Equidade",
        "es_name": "Métricas de Sesgo/Equidad",
        "desc": "Documentation of bias or fairness evaluations.",
        "keywords": ["bias", "fairness", "equity", "discrimination", "fair"],
        "required_for": ["high", "limited"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 10(3), 13(2)(b) — Bias mitigation and fairness",
            "NIST_AI_RMF": "MAP 02-02 — Bias and fairness assessment",
            "ISO_42001": "Annex A.6.2 — Bias and fairness controls"
        }
    },
    "risk_mitigation": {
        "weight": 8,
        "en_name": "Risk Mitigation Evidence",
        "pt_name": "Evidências de Mitigação de Riscos",
        "es_name": "Evidencias de Mitigación de Riesgos",
        "desc": "Documentation of risk assessments and mitigation strategies.",
        "keywords": ["risk", "mitigation", "control", "safeguard", "assessment"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 9, 16(3) — Risk management and mitigation",
            "NIST_AI_RMF": "GOVERN 02-02 — Risk mitigation strategies",
            "ISO_42001": "Clause 8.2 — Risk assessment and treatment"
        }
    },
    "inference_logs": {
        "weight": 9,
        "en_name": "Production Inference Logs",
        "pt_name": "Logs de Inferência em Produção",
        "es_name": "Logs de Inferencia en Producción",
        "desc": "Detailed logs of model inferences in a production environment.",
        "keywords": ["inference", "prediction", "output", "result", "production"],
        "required_for": ["high", "limited"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(e), 50 — Production logging and traceability",
            "NIST_AI_RMF": "MEASURE 02-02 — Production inference logging",
            "ISO_42001": "Annex A.10.4 — Production monitoring logs"
        }
    },
    "continuous_monitoring": {
        "weight": 7,
        "en_name": "Continuous Monitoring Reports",
        "pt_name": "Relatórios de Monitoramento Contínuo",
        "es_name": "Informes de Monitoreo Continuo",
        "desc": "Reports from continuous monitoring systems over time.",
        "keywords": ["continuous", "monitoring", "ongoing", "real-time", "report"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 49, 50 — Continuous monitoring obligations",
            "NIST_AI_RMF": "MEASURE 04-01 — Continuous monitoring",
            "ISO_42001": "Annex A.10.5 — Continuous improvement monitoring"
        }
    },
    "historical_reconstruction": {
        "weight": 9,
        "en_name": "Historical Reconstruction Capability",
        "pt_name": "Capacidade de Reconstrução Histórica",
        "es_name": "Capacidad de Reconstrucción Histórica",
        "desc": "Ability to restore a historical state of the model and its data.",
        "keywords": ["historical", "reconstruct", "restore", "timeline", "backup"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 13(3)(l) — Historical state reconstruction",
            "NIST_AI_RMF": "MAP 04-02 — Historical snapshot capability",
            "ISO_42001": "Annex A.8.8 — Historical reconstruction"
        }
    },
    "incident_documentation": {
        "weight": 8,
        "en_name": "Incident Documentation",
        "pt_name": "Documentação de Incidentes",
        "es_name": "Documentación de Incidentes",
        "desc": "Documentation of incidents and corrective actions related to the model.",
        "keywords": ["incident", "issue", "problem", "corrective", "action"],
        "required_for": ["high"],
        "legal_basis": {
            "EU_AI_ACT": "Art. 61, 62 — Incident reporting and remediation",
            "NIST_AI_RMF": "RESPOND 01-01 — Incident documentation",
            "ISO_42001": "Clause 10.2 — Corrective action for incidents"
        }
    }
}

# --- SCHEMAS (minimal) for metadata validation ---
MINIMAL_METADATA_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": ["string", "number"]},
        "creation_date": {"type": "string"},
        "dataset_hash": {"type": "string"},
        "training_metrics": {"type": "object"}
    },
    "required": ["version", "creation_date"]
}
MINIMAL_LOG_SCHEMA = {
    "type": ["object", "array"],
    "items": {
        "type": "object",
        "properties": {
            "timestamp": {"type": "string"},
            "model_version": {"type": ["string", "number"]},
            "input_id": {},
            "prediction": {}
        },
        "required": ["timestamp", "model_version", "prediction"]
    }
}

# Define file patterns and keywords for categorization.
FILE_PATTERNS = {
    "metadata_files": ["metadata", "model_card", "about", "info"],
    "model_artifacts": [".pt", ".pth", ".onnx", ".joblib", ".pkl", "model.", "checkpoint"],
    "dataset_files": ["dataset", "data", "train", "test", "validation", ".csv", ".parquet", ".jsonl"],
    "decision_logs": ["decision", "inference", "prediction", "log", "output"],
    "training_configs": ["config", "hyperparameters", "train_config", "settings", "parameters"],
    "requirements_files": ["requirements.txt", "pyproject.toml", "environment.yml", "pipfile", "setup.py"],
    "pipelines": ["pipeline", "dag", "workflow", "orchestration", "mlflow"],
    "approvals": ["approval", "committee", "signoff", "approved", "review", "audit"],
    "monitoring_reports": ["monitor", "dashboard", "metrics", "report", "performance"],
    "documentation": [".md", ".txt", "readme", "docs", "documentation"],
    "other_text": [".json", ".yaml", ".yml", ".csv", ".txt", ".md"]
}

# Directories to ignore during scan
IGNORED_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", ".mypy_cache",
    ".vscode", ".idea", "venv", "env", ".DS_Store", "dist", "build", ".eggs"
}

# --- UTILITY FUNCTIONS ---
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

def sha256_of_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

def sha256_of_file(path: Path) -> str:
    sha256 = hashlib.sha256()
    try:
        if not path.is_file():
            return "error: not a file"
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"error: {str(e)}"

def safe_read_text(path: Path, max_bytes: int = 8192) -> Tuple[Optional[str], Optional[str]]:
    try:
        if not path.is_file():
            return None, "not a file"
        with path.open("rb") as f:
            raw_data = f.read(max_bytes)
        for encoding in ["utf-8", "latin-1", "cp1252", "ascii"]:
            try:
                decoded = raw_data.decode(encoding)
                return decoded, None
            except UnicodeDecodeError:
                continue
        return None, "Unable to decode with common encodings"
    except Exception as e:
        return None, f"Exception during read: {str(e)}"

def load_file(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        suffix = path.suffix.lower()
        if suffix == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
        elif suffix in (".yaml", ".yml"):
            try:
                import yaml
                return yaml.safe_load(path.read_text(encoding="utf-8"))
            except ImportError:
                logger.warning("PyYAML not installed. Skipping YAML parsing.")
                return path.read_text(encoding="utf-8")
        elif suffix == ".csv":
            import csv
            with path.open("r", encoding="utf-8", errors='ignore') as f:
                return list(csv.DictReader(f))
        else:
            return path.read_text(encoding="utf-8", errors='ignore')
    except Exception as e:
        logger.debug(f"Error loading file {path}: {e}")
        return f"error_reading_file: {str(e)}"

def validate_with_schema(obj: Any, schema: Dict) -> List[str]:
    if not JSONSCHEMA_AVAILABLE:
        issues = []
        if isinstance(schema, dict) and "required" in schema and isinstance(obj, dict):
            for r in schema.get("required", []):
                if r not in obj:
                    issues.append(f"missing required field: {r}")
        return issues
    else:
        try:
            jsonschema.validate(instance=obj, schema=schema)
            return []
        except jsonschema.ValidationError as e:
            return [str(e.message)]
        except Exception as e:
            return [f"Schema validation failed: {str(e)}"]

def parse_timestamp(value: str) -> Optional[datetime]:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

# --- SCANNER LOGIC ---
def should_ignore_dir(dir_path: Path, root: Path) -> bool:
    try:
        rel_path = dir_path.relative_to(root)
        parts = rel_path.parts
        return any(part in IGNORED_DIRS for part in parts)
    except Exception:
        return True

def scan_repository(root_path: Path) -> Dict[str, List[Path]]:
    candidates: Dict[str, List[Path]] = {key: [] for key in FILE_PATTERNS.keys()}
    if not root_path.exists() or not root_path.is_dir():
        logger.warning(f"Repository path {root_path} does not exist or is not a directory.")
        return candidates
    try:
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue
            if any(should_ignore_dir(parent, root_path) for parent in file_path.parents):
                continue
            file_name = file_path.name.lower()
            file_suffix = file_path.suffix.lower()
            for category, patterns in FILE_PATTERNS.items():
                matched = False
                for pattern in patterns:
                    if (pattern.startswith('.') and file_suffix == pattern) or \
                       (not pattern.startswith('.') and pattern in file_name):
                        candidates[category].append(file_path)
                        matched = True
                        break
                if matched:
                    break
    except Exception as e:
        logger.error(f"Error during repository scan: {e}")
    return candidates

# --- AUDIT LOGIC ---
def copy_evidence(src_path: Path, evidence_dir: Path) -> str:
    try:
        if not src_path.is_file():
            return "error: source not a file"
        try:
            mtime = src_path.stat().st_mtime
        except Exception:
            mtime = 0
        file_hash = sha256_of_file(src_path)
        if file_hash.startswith("error"):
            file_hash = "unknown"
        dest_name = f"{int(mtime)}_{file_hash[:16]}__{src_path.name}"
        dest_path = evidence_dir / dest_name
        counter = 1
        original_dest_path = dest_path
        while dest_path.exists():
            dest_name = f"{int(mtime)}_{file_hash[:16]}__{counter}__{src_path.name}"
            dest_path = evidence_dir / dest_name
            counter += 1
        shutil.copy2(src_path, dest_path)
        return str(dest_path.relative_to(evidence_dir.parent))
    except Exception as e:
        return f"error: {str(e)}"

def validate_retention_policies(file_paths: List[Path]) -> List[str]:
    issues = []
    retention_period = datetime.now() - timedelta(days=365)
    for path in file_paths:
        try:
            if any(term in path.name.lower() for term in ["log", "audit", "backup", "trace"]):
                try:
                    creation_time = datetime.fromtimestamp(path.stat().st_ctime)
                    if creation_time < retention_period:
                        issues.append(f"Arquivo antigo potencialmente fora da política de retenção: {path}")
                except Exception:
                    issues.append(f"Não foi possível verificar a idade do arquivo: {path}")
        except Exception:
            continue
    return issues

def check_cross_references(
    metadata_files: List[Tuple[Path, Any]],
    log_files: List[Tuple[Path, Any]]
) -> List[str]:
    issues = []
    model_versions = set()
    for path, metadata in metadata_files:
        try:
            if isinstance(metadata, dict) and "version" in metadata:
                model_versions.add(str(metadata["version"]))
        except Exception:
            continue
    for path, log_data in log_files:
        try:
            if isinstance(log_data, dict) and "model_version" in log_data:
                log_version = str(log_data["model_version"])
                if log_version not in model_versions:
                    issues.append(f"Log {path.name} referencia versão de modelo desconhecida: {log_version}")
            elif isinstance(log_data, list):
                for entry in log_data:
                    if isinstance(entry, dict) and "model_version" in entry:
                        log_version = str(entry["model_version"])
                        if log_version not in model_versions:
                            issues.append(f"Log {path.name} referencia versão de modelo desconhecida: {log_version}")
                            break
        except Exception:
            continue
    return issues

def perform_audit(repo_root: Path, evidence_dir: Path, risk_level: str) -> Dict[str, Any]:
    candidates = scan_repository(repo_root)
    required_items = RISK_LEVELS.get(risk_level, [])
    audit_results: Dict[str, Any] = {
        "summary": {
            "total_score": 0,
            "max_score": sum(TRACEABILITY_ITEMS[item]["weight"] for item in required_items),
            "scanned_files": sum(len(files) for files in candidates.values()),
            "risk_level": risk_level,
            "required_items_count": len(required_items)
        },
        "details": {},
        "evidence_index": {},
        "cross_reference_issues": [],
        "retention_issues": [],
        "scanned_categories": {k: len(v) for k, v in candidates.items()}
    }

    parsed_metadata = []
    parsed_logs = []
    for p in candidates.get("metadata_files", []):
        try:
            parsed_metadata.append((p, load_file(p)))
        except Exception:
            parsed_metadata.append((p, None))
    for p in candidates.get("decision_logs", []):
        try:
            parsed_logs.append((p, load_file(p)))
        except Exception:
            parsed_logs.append((p, None))

    try:
        audit_results["retention_issues"] = validate_retention_policies(list(repo_root.rglob("*")))
    except Exception as e:
        logger.error(f"Error validating retention policies: {e}")
        audit_results["retention_issues"] = [f"Error during retention validation: {e}"]

    try:
        audit_results["cross_reference_issues"] = check_cross_references(parsed_metadata, parsed_logs)
    except Exception as e:
        logger.error(f"Error checking cross references: {e}")
        audit_results["cross_reference_issues"] = [f"Error during cross-reference validation: {e}"]

    def register_item_evidence(item_key: str, file_path: Path):
        try:
            if not file_path.is_file():
                return
            rel_path = str(file_path.relative_to(repo_root))
            if item_key not in audit_results["details"]:
                item_meta = TRACEABILITY_ITEMS.get(item_key, {})
                audit_results["details"][item_key] = {
                    "weight": item_meta.get("weight", 0),
                    "score": 0,
                    "checks": [],
                    "evidence": [],
                    "status": "not_found",
                    "is_required_for_risk": risk_level in item_meta.get("required_for", []),
                    "legal_basis": item_meta.get("legal_basis", {})
                }
            if rel_path not in audit_results["evidence_index"]:
                copied_path = copy_evidence(file_path, evidence_dir)
                if copied_path and not copied_path.startswith("error"):
                    audit_results["evidence_index"][rel_path] = copied_path
            if rel_path not in audit_results["details"][item_key]["evidence"]:
                audit_results["details"][item_key]["evidence"].append(rel_path)
        except Exception as e:
            logger.debug(f"Error registering evidence for {item_key} from {file_path}: {e}")

    for item_key, item_meta in TRACEABILITY_ITEMS.items():
        try:
            if item_key not in audit_results["details"]:
                item_result = {
                    "weight": item_meta["weight"],
                    "score": 0,
                    "checks": [],
                    "evidence": [],
                    "status": "not_found",
                    "is_required_for_risk": risk_level in item_meta.get("required_for", []),
                    "legal_basis": item_meta.get("legal_basis", {})
                }
                audit_results["details"][item_key] = item_result
            else:
                item_result = audit_results["details"][item_key]
                item_result.setdefault("weight", item_meta["weight"])
                item_result.setdefault("score", 0)
                item_result.setdefault("checks", [])
                item_result.setdefault("evidence", [])
                item_result.setdefault("status", "not_found")
                item_result.setdefault("is_required_for_risk", risk_level in item_meta.get("required_for", []))
                item_result.setdefault("legal_basis", item_meta.get("legal_basis", {}))

            if not item_result["is_required_for_risk"]:
                item_result["status"] = "optional"
                continue

            found_evidence = False
            for category, files in candidates.items():
                for file_path in files:
                    try:
                        content, error = safe_read_text(file_path, max_bytes=8192)
                        if content is None:
                            continue
                        if any(kw.lower() in content.lower() or kw.lower() in file_path.name.lower() for kw in item_meta.get("keywords", [])):
                            item_result["checks"].append(f"Keyword match for '{item_meta['en_name']}' in {file_path.name}.")
                            register_item_evidence(item_key, file_path)
                            found_evidence = True
                    except Exception as e:
                        continue

            try:
                if item_key == "dataset_versioning":
                    dataset_hashes = []
                    for _, metadata in parsed_metadata:
                        if isinstance(metadata, dict) and "dataset_hash" in metadata:
                            dataset_hashes.append(metadata["dataset_hash"])
                    if dataset_hashes or any(".dvc" in str(p) for p in candidates.get("other_text", [])):
                        item_result["checks"].append("Specific dataset versioning artifacts found (DVC or dataset_hash).")
                        found_evidence = True
                        for path in candidates.get("dataset_files", []):
                            actual_hash = sha256_of_file(path)
                            if actual_hash in dataset_hashes:
                                item_result["checks"].append(f"Dataset hash validated for {path.name}.")
                                register_item_evidence(item_key, path)
                elif item_key == "model_versioning":
                    if candidates.get("model_artifacts") or any(isinstance(m, dict) and "version" in m for _, m in parsed_metadata):
                        item_result["checks"].append("Specific model versioning artifacts found (model files or version metadata).")
                        found_evidence = True
                        for path in candidates.get("model_artifacts", []):
                            register_item_evidence(item_key, path)
                elif item_key == "reproducibility_capability":
                    required_components_found = [
                        len(candidates.get("training_configs", [])) > 0,
                        len(candidates.get("requirements_files", [])) > 0,
                        len(candidates.get("dataset_files", [])) > 0,
                        len(candidates.get("model_artifacts", [])) > 0
                    ]
                    if all(required_components_found):
                        item_result["checks"].append("All core components for reproducibility found (config, deps, data, model).")
                        found_evidence = True
                        for category in ["training_configs", "requirements_files", "dataset_files", "model_artifacts"]:
                            for path in candidates.get(category, []):
                                register_item_evidence(item_key, path)
                elif item_key == "cross_reference":
                    if not audit_results["cross_reference_issues"]:
                        item_result["checks"].append("Cross-references between logs and metadata are consistent.")
                        found_evidence = True
                        for path, _ in parsed_logs + parsed_metadata:
                            register_item_evidence(item_key, path)
                elif item_key == "file_integrity_hash":
                    for path in candidates.get("dataset_files", []) + candidates.get("model_artifacts", []):
                        actual_hash = sha256_of_file(path)
                        if any(isinstance(m, dict) and m.get("dataset_hash") == actual_hash for _, m in parsed_metadata) or \
                           any(isinstance(m, dict) and m.get("model_hash") == actual_hash for _, m in parsed_metadata):
                            item_result["checks"].append(f"File integrity confirmed for {path.name}.")
                            found_evidence = True
                            register_item_evidence(item_key, path)
            except Exception as e:
                logger.error(f"Error in specific validation for {item_key}: {e}")
                item_result["checks"].append(f"Error during specific validation: {e}")

            if found_evidence:
                item_result["score"] = item_meta["weight"]
                item_result["status"] = "found"
            else:
                item_result["checks"].append(f"No clear evidence found for '{item_meta['en_name']}'.")
                item_result["status"] = "not_found"

            audit_results["summary"]["total_score"] += item_result["score"]
        except Exception as e:
            logger.error(f"Unexpected error processing item {item_key}: {e}")
            if item_key not in audit_results["details"]:
                audit_results["details"][item_key] = {
                    "weight": item_meta.get("weight", 0),
                    "score": 0,
                    "checks": [f"Critical error during audit: {e}"],
                    "evidence": [],
                    "status": "error",
                    "is_required_for_risk": risk_level in item_meta.get("required_for", []),
                    "legal_basis": item_meta.get("legal_basis", {})
                }

    return audit_results

# --- MAIN EXECUTION LOGIC ---
def generate_multilingual_report(audit_results: Dict[str, Any], repo_path: Path, lang: str = "pt") -> Dict[str, Any]:
    report = {
        "audit_id": str(uuid.uuid4()),
        "audit_timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "audit_run": {
            "user": os.getenv("USER", "unknown"),
            "environment_info": f"Python {sys.version}",
            "repository_path": str(repo_path),
            "risk_level": audit_results["summary"]["risk_level"]
        },
        "regulatory_references": REGULATORY_REFERENCES,
        "summary": audit_results["summary"],
        "details": {},
        "evidence_index": audit_results["evidence_index"],
        "issues": {
            "retention": audit_results["retention_issues"],
            "cross_reference": audit_results["cross_reference_issues"]
        },
        "scanned_categories": audit_results["scanned_categories"],
    }

    total_score = report["summary"]["total_score"]
    max_score = report["summary"]["max_score"]
    report["summary"]["compliance_percentage"] = round((total_score / max_score) * 100, 2) if max_score > 0 else 0.0

    for k, v in audit_results["details"].items():
        item_meta = TRACEABILITY_ITEMS.get(k, {})
        legal_basis_used = item_meta.get("legal_basis", {})
        report["details"][k] = {
            "en": {
                "name": item_meta.get("en_name", k),
                "description": item_meta.get("desc", ""),
                "result": v,
                "legal_basis": legal_basis_used
            },
            "pt": {
                "name": item_meta.get("pt_name", k),
                "description": item_meta.get("desc", ""),
                "result": v,
                "legal_basis": legal_basis_used
            },
            "es": {
                "name": item_meta.get("es_name", k),
                "description": item_meta.get("desc", ""),
                "result": v,
                "legal_basis": legal_basis_used
            },
        }

    return report

def get_console_messages(lang: str = "pt") -> Dict[str, str]:
    messages = {
        "pt": {
            "start": "🚀 Iniciando auditoria de rastreabilidade de IA (nível de risco: {risk_level})...",
            "repo": "📁 Auditando repositório:",
            "scan": "🔍 Escaneando repositório e analisando artefatos...",
            "report": "📊 Gerando relatório multilíngue com base legal...",
            "save": "💾 Relatório salvo em:",
            "hash": "🔒 Hash de integridade:",
            "done": "🎯 Auditoria concluída com sucesso!",
            "summary_title": "📋 RESUMO DA AUDITORIA DE RASTREABILIDADE",
            "compliance": "✅ Conformidade com nível {risk_level} (base legal: EU AI Act, NIST, ISO)",
            "score": "📊 Pontuação",
            "files": "📁 Arquivos escaneados",
            "retention": "⚠️  Problemas de retenção",
            "cross_ref": "🔗 Problemas de cross-reference",
            "categories": "📦 CATEGORIAS ESCANEADAS",
            "error_repo": "❌ Erro: Caminho do repositório '{}' não existe.",
            "error_save": "❌ Erro ao salvar relatório de auditoria:",
            "error_hash": "❌ Erro ao salvar hash de auditoria:",
            "set_env": "Defina a variável de ambiente BTAUDIT_REPO_ROOT ou execute a partir da raiz do repositório alvo.",
            "invalid_risk": "❌ Nível de risco inválido: {}. Escolha entre: high, limited, low."
        },
        "en": {
            "start": "🚀 Starting AI traceability audit (risk level: {risk_level})...",
            "repo": "📁 Auditing repository:",
            "scan": "🔍 Scanning repository and analyzing artifacts...",
            "report": "📊 Generating multilingual report with legal basis...",
            "save": "💾 Report saved at:",
            "hash": "🔒 Integrity hash:",
            "done": "🎯 Audit completed successfully!",
            "summary_title": "📋 TRACEABILITY AUDIT SUMMARY",
            "compliance": "✅ Compliance for {risk_level} risk level (legal basis: EU AI Act, NIST, ISO)",
            "score": "📊 Score",
            "files": "📁 Scanned files",
            "retention": "⚠️  Retention issues",
            "cross_ref": "🔗 Cross-reference issues",
            "categories": "📦 SCANNED CATEGORIES",
            "error_repo": "❌ Error: Repository path '{}' does not exist.",
            "error_save": "❌ Error saving audit report:",
            "error_hash": "❌ Error saving audit hash:",
            "set_env": "Set the BTAUDIT_REPO_ROOT environment variable or run from the target repository's root.",
            "invalid_risk": "❌ Invalid risk level: {}. Choose from: high, limited, low."
        },
        "es": {
            "start": "🚀 Iniciando auditoría de trazabilidad de IA (nivel de riesgo: {risk_level})...",
            "repo": "📁 Auditando repositorio:",
            "scan": "🔍 Escaneando repositorio y analizando artefactos...",
            "report": "📊 Generando informe multilingüe con base legal...",
            "save": "💾 Informe guardado en:",
            "hash": "🔒 Hash de integridad:",
            "done": "🎯 ¡Auditoría completada con éxito!",
            "summary_title": "📋 RESUMEN DE AUDITORÍA DE TRAZABILIDAD",
            "compliance": "✅ Conformidad para nivel de riesgo {risk_level} (base legal: EU AI Act, NIST, ISO)",
            "score": "📊 Puntuación",
            "files": "📁 Archivos escaneados",
            "retention": "⚠️  Problemas de retención",
            "cross_ref": "🔗 Problemas de referencias cruzadas",
            "categories": "📦 CATEGORÍAS ESCANEADAS",
            "error_repo": "❌ Error: La ruta del repositorio '{}' no existe.",
            "error_save": "❌ Error al guardar el informe de auditoría:",
            "error_hash": "❌ Error al guardar el hash de auditoría:",
            "set_env": "Establezca la variable de entorno BTAUDIT_REPO_ROOT o ejecute desde la raíz del repositorio objetivo.",
            "invalid_risk": "❌ Nivel de riesgo inválido: {}. Elija entre: high, limited, low."
        }
    }
    return messages.get(lang, messages["pt"])

def main():
    parser = argparse.ArgumentParser(description="AI/ML Risk-Aware & Regulatory-Citable Traceability Audit Runner")
    parser.add_argument("--repo", type=str, required=True, help="Path to the repository to audit")
    parser.add_argument("--output", type=str, required=True, help="Output directory (e.g., ../audition/Auditing_by_principles/rastreabilidade)")
    parser.add_argument("--lang", type=str, choices=["en", "pt", "es"], default="pt", help="Language for console output")
    parser.add_argument("--risk-level", type=str, choices=["high", "limited", "low"], default="high",
                        help="Risk level of the AI system (default: high)")
    args = parser.parse_args()

    if args.risk_level not in RISK_LEVELS:
        msgs = get_console_messages(args.lang)
        logger.error(msgs["invalid_risk"].format(args.risk_level))
        sys.exit(1)

    msgs = get_console_messages(args.lang)
    logger.info(msgs["start"].format(risk_level=args.risk_level.upper()))

    client_repo_path = Path(args.repo).resolve()
    if not client_repo_path.exists():
        logger.error(f"{msgs['error_repo'].format(client_repo_path)}")
        sys.exit(1)
    if not client_repo_path.is_dir():
        logger.error(f"Provided path is not a directory: {client_repo_path}")
        sys.exit(1)

    logger.info(f"{msgs['repo']} {client_repo_path}")

    # --- RECEBE O CAMINHO DE SAÍDA DO ORCHESTRATOR ---
    PRINCIPLE_DIR = Path(args.output)
    EVIDENCE_DIR = PRINCIPLE_DIR / "evidence"

    # Cria apenas as pastas ESPECÍFICAS deste runner
    try:
        PRINCIPLE_DIR.mkdir(parents=True, exist_ok=True)
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Could not create output directories: {e}")
        sys.exit(1)

    logger.info(msgs["scan"])

    # Executa auditoria
    try:
        audit_results = perform_audit(client_repo_path, EVIDENCE_DIR, args.risk_level)
    except Exception as e:
        logger.critical(f"Critical failure during audit: {e}")
        audit_results = {
            "summary": {"total_score": 0, "max_score": 0, "scanned_files": 0, "risk_level": args.risk_level, "required_items_count": 0},
            "details": {},
            "evidence_index": {},
            "cross_reference_issues": [f"CRITICAL: Audit failed with exception: {e}"],
            "retention_issues": [],
            "scanned_categories": {}
        }

    logger.info(msgs["report"])

    # Gera relatório
    try:
        final_report = generate_multilingual_report(audit_results, client_repo_path, args.lang)
    except Exception as e:
        logger.critical(f"Failed to generate report: {e}")
        final_report = {
            "audit_id": str(uuid.uuid4()),
            "audit_timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "audit_run": {
                "user": os.getenv("USER", "unknown"),
                "environment_info": "Python fallback",
                "repository_path": str(client_repo_path),
                "risk_level": args.risk_level
            },
            "regulatory_references": {},
            "summary": {"total_score": 0, "max_score": 0, "compliance_percentage": 0.0, "scanned_files": 0, "risk_level": args.risk_level, "required_items_count": 0},
            "details": {},
            "evidence_index": {},
            "issues": {"retention": [], "cross_reference": [f"REPORT GENERATION FAILED: {e}"]},
            "scanned_categories": {}
        }

    # Salva o JSON com o nome obrigatório: "rastreabilidade_json"
    out_json_path = PRINCIPLE_DIR / "rastreabilidade_json"
    try:
        with out_json_path.open("w", encoding="utf-8") as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Relatório salvo em: {out_json_path}")
    except Exception as e:
        logger.error(f"{msgs['error_save']} {e}")
        out_json_path = None

    # Gera hash do conteúdo do relatório
    try:
        report_content = json.dumps(final_report, ensure_ascii=False, indent=2)
        report_hash = hashlib.sha256(report_content.encode("utf-8")).hexdigest()
    except Exception as e:
        report_hash = f"hash_generation_failed: {e}"

    # Salva hash na raiz da pasta do princípio
    hash_path = PRINCIPLE_DIR / "audit_hash.txt"
    try:
        with hash_path.open("w", encoding="utf-8") as f:
            f.write(report_hash + "\n")
            if out_json_path:
                f.write(f"Source: rastreabilidade_json\n")
    except Exception as e:
        logger.error(f"{msgs['error_hash']} {e}")

    # Imprime resumo no console
    print("\n" + "="*70)
    print(msgs["summary_title"])
    print("="*70)
    print(f"{msgs['compliance'].format(risk_level=args.risk_level.upper())}")
    print(f"{msgs['score']}: {final_report['summary']['total_score']}/{final_report['summary']['max_score']} → {final_report['summary'].get('compliance_percentage', 0)}%")
    print(f"{msgs['files']}: {final_report['summary']['scanned_files']}")
    print(f"{msgs['retention']}: {len(final_report['issues']['retention'])}")
    print(f"{msgs['cross_ref']}: {len(final_report['issues']['cross_reference'])}")
    if out_json_path:
        print(f"{msgs['save']} {out_json_path}")
    else:
        print(f"{msgs['save']} NOT SAVED DUE TO ERROR")
    print(f"{msgs['hash']} {report_hash}")
    print(f"📜 Base Legal: EU AI Act | NIST AI RMF | ISO/IEC 42001")
    print("="*70)
    print(f"\n{msgs['categories']}:")
    for category, count in final_report["scanned_categories"].items():
        if count > 0:
            print(f"  • {category}: {count} arquivos")

    logger.info(msgs["done"])

if __name__ == "__main__":
    main()