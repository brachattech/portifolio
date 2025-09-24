#----------------------------
# AI Accountability Auditor
# ---------------------------

# This script implements an automated audit system for artificial intelligence,
# focused on the principle of **Accountability**.
#
# Purpose:
# - Analyze metadata files, decision logs, and audit evidence from the AI system.
# - Check compliance with legal and regulatory frameworks such as Brazil's LGPD, EU's GDPR, and ethical standards like IEEE Ethically Aligned Design.
# - Detect running AI-related processes and identify accountability risks.
# - Generate structured (JSON) reports for auditing and compliance tracking.
#
# Audited principle:
# - **Accountability**: ensures AI systems are transparent, responsible, and monitorable,
#   allowing automated decisions to be traced, explained, and verified by humans.


# ---------------------------
# Standard library imports
# ---------------------------
import os # Operating system interfaces
import json # JSON encoding and decoding
import logging # Logging framework for audit trail
import numpy as np # Numerical computing for vector operations
from datetime import datetime # Date and time manipulation
from pathlib import Path # Object-oriented filesystem paths
import hashlib # Secure hash algorithms (SHA256)
import platform # Platform identification
import socket # Networking interface
import getpass # Get current username
import uuid # Unique identifiers
import stat # File permission constants
import psutil # System and process monitoring
import argparse # Command-line argument parsing
import importlib # Dynamic module importing
import subprocess # Run system commands
import sys # System-specific parameters

Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AccountabilityRunner') # Create logger instance

class AccountabilityRunner:
def init(self, project_root):
"""
Initialize the Accountability Runner with project root directory.
Sets up required folder structure, legal framework, and result template.
"""
# Convert project root to Path object for easier path manipulation
self.project_root = Path(project_root)

text
    # Define the 5 required folders for accountability compliance as per ADR
    self.required_folders = [
        "decision_logs",        # Folder for automated decision logs and records
        "audit_evidence",       # Folder for audit evidence and compliance documentation
        "model_metadata",       # Folder for model metadata and documentation
        "responsible_persons",  # Folder for responsible persons registry
        "monitoring_dashboards" # Folder for monitoring dashboards and visualizations
    ]
    
    # Legal framework mapping for accountability requirements by category
    # Based on LGPD, GDPR, EU AI Act, and other regulations
    self.legal_framework = {
        "decision_logs": [
            {"law": "LGPD - Art. 9º", "requirements": ["Record of automated decisions", "Timestamped logs"]},
            {"law": "EU AI Act - Art. 13", "requirements": ["Human oversight requirements", "Decision tracing"]}
        ],
        "audit_evidence": [
            {"law": "LGPD - Art. 46", "requirements": ["Audit and approval evidence", "Compliance documentation"]},
            {"law": "GDPR - Art. 5º", "requirements": ["Accountability principle", "Documentation evidence"]}
        ],
        "model_metadata": [
            {"law": "LGPD - Lei nº 13.709/2018", "articles": ["Art. 6º", "Art. 17º"],
             "requirements": ["Transparency in automated decisions", "Security and governance measures"]},
            {"law": "GDPR - Art. 5º, Art. 22", "requirements": ["Right to explanation", "Model documentation"]}
        ],
        "responsible_persons": [
            {"law": "LGPD - Art. 6º", "requirements": ["Responsible for automated decisions", "Contact information"]},
            {"law": "Marco Civil da Internet - Art. 7º", "requirements": ["Liability for damages", "Assigned responsibilities"]}
        ],
        "monitoring_dashboards": [
            {"law": "OECD AI Principles", "requirements": ["Robustness, security and safety", "Monitoring systems"]},
            {"law": "EU AI Act - Art. 13", "requirements": ["Human oversight", "Real-time monitoring"]}
        ]
    }
    
    # Initialize results structure with default values as defined in ADR
    self.results = {
        "principle": "Accountability",
        "status": "pending",
        "timestamp": datetime.now().isoformat(),
        "structural_validation": {},
        "semantic_validation": {
            "decision_logs_score": 0.0,
            "decision_logs_feedback": "",
            "audit_evidence_score": 0.0,
            "audit_evidence_feedback": "",
            "model_metadata_score": 0.0,
            "model_metadata_feedback": "",
            "responsible_persons_score": 0.0,
            "responsible_persons_feedback": "",
            "monitoring_dashboards_score": 0.0,
            "monitoring_dashboards_feedback": ""
        },
        "legal_compliance": {},
        "required_actions": [],
        "system_info": {},
        "integrity_checks": {},
        "risk_configuration": {},  # Added from second code
        "compliance_summary": {},  # Added from second code
        "risk_based_recommendations": []  # Added from second code
    }
    
    # Initialize embedding model and semantic analyzer
    self.setup_embedding_model()
    self.semantic_analyzer = SemanticAnalyzer()
    
    # Ensure all required packages are installed
    self.ensure_dependencies()

def ensure_dependencies(self):
    """Ensure all required Python packages are installed."""
    REQUIRED_PACKAGES = [
        ("numpy", None),
        ("pandas", None),
        ("scikit-learn", "sklearn"),
        ("sentence-transformers", "sentence_transformers"),
        ("psutil", None),
    ]
    
    for pkg, imp in REQUIRED_PACKAGES:
        self.ensure_package(pkg, imp)

def ensure_package(self, pkg_name, import_name=None):
    """Dynamically ensure a Python package is installed."""
    import_name = import_name or pkg_name
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        logger.info(f"Package '{pkg_name}' not found. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            logger.info(f"Package '{pkg_name}' installed successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to install {pkg_name}: {e}")
            return False

def setup_embedding_model(self):
    """Initialize the BAAI embedding model for semantic similarity analysis."""
    try:
        from sentence_transformers import SentenceTransformer
        # Use BAAI model as requested
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        logger.info("BAAI/bge-small-en-v1.5 embedding model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        self.model = None

def get_embedding(self, text):
    """Generate embedding vector for input text using BAAI model."""
    if self.model is None or not text:
        return None
    try:
        return self.model.encode(text, normalize_embeddings=True)
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return None

def cosine_similarity(self, vec1, vec2):
    """Compute cosine similarity between two vectors."""
    if vec1 is None or vec2 is None:
        return 0.0
    try:
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    except:
        return 0.0

def safe_path_join(self, base_path, target_path):
    """Safely join paths to prevent directory traversal attacks."""
    base_path = os.path.abspath(base_path)
    target_path = os.path.normpath(target_path)
    if os.path.commonprefix([base_path, os.path.abspath(os.path.join(base_path, target_path))]) != base_path:
        raise ValueError(f"Path traversal attempt detected: {target_path}")
    return os.path.join(base_path, target_path)

def compute_file_hash(self, filepath):
    """Compute SHA256 hash for file integrity verification."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def read_file_text(self, filepath):
    """Read UTF-8 text content of file; return empty string on error."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def check_file_permissions(self, filepath):
    """Check if critical files have appropriate permissions and security settings."""
    try:
        st = os.stat(filepath)
        return {
            "readable": bool(st.st_mode & stat.S_IRUSR),
            "writable": bool(st.st_mode & stat.S_IWUSR),
            "executable": bool(st.st_mode & stat.S_IXUSR),
            "others_readable": bool(st.st_mode & stat.S_IROTH),
            "others_writable": bool(st.st_mode & stat.S_IWOTH),
            "file_size": st.st_size,
            "last_modified": datetime.fromtimestamp(st.st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to check permissions for {filepath}: {e}")
        return None

def check_ai_processes(self):
    """Check for running AI-related processes on the system."""
    ai_keywords = ["model", "ai", "ml", "inference", "training", "tensorflow", "pytorch", "scikit"]
    ai_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
        try:
            process_info = proc.info
            if any(keyword in ' '.join(process_info.get('cmdline', [])).lower() for keyword in ai_keywords):
                ai_processes.append({
                    "pid": process_info['pid'],
                    "name": process_info['name'],
                    "cmdline": process_info.get('cmdline', []),
                    "user": process_info.get('username', 'unknown'),
                    "accountability_risk": "high" if "model" in ' '.join(process_info.get('cmdline', [])).lower() else "medium"
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return ai_processes

def check_system_utilization(self):
    """Check system resource utilization metrics."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "active_processes": len(psutil.pids())
    }

def classify_risk_level(self):
    """Classify AI system into HIGH/MEDIUM/LOW risk based on model_info.json."""
    model_info_path = self.project_root / "model_info.json"
    default_config = {
        "risk_category": "medium_risk",
        "compliance_threshold": 0.7,
        "required_checks": ["model_metadata", "decision_logs"],
        "description": "Default medium risk classification"
    }
    
    high_risk_keywords = ["medical", "diagnosis", "healthcare", "credit", "scoring", 
                         "hiring", "employment", "criminal", "justice", "sentencing"]
    medium_risk_keywords = ["recommendation", "personalization", "content", "moderation",
                           "loan", "insurance", "advertising", "targeting"]
    
    if not model_info_path.exists():
        logger.warning("model_info.json not found, using default risk classification")
        return default_config
    
    try:
        with open(model_info_path, 'r') as f:
            model_info = json.load(f)
        
        intended_use = model_info.get("intended_use", "").lower()
        impact_level = model_info.get("impact_level", "").lower()
        
        if any(keyword in intended_use for keyword in high_risk_keywords) or impact_level == "high":
            return {
                "risk_category": "high_risk",
                "compliance_threshold": 0.9,
                "required_checks": ["model_metadata", "decision_logs", "audit_evidence", "responsible_persons", "monitoring_dashboards"],
                "description": "High risk system - medical, financial, employment, or criminal justice applications"
            }
        elif any(keyword in intended_use for keyword in medium_risk_keywords) or impact_level == "medium":
            return {
                "risk_category": "medium_risk",
                "compliance_threshold": 0.7,
                "required_checks": ["model_metadata", "decision_logs", "responsible_persons"],
                "description": "Medium risk system - recommendations, content moderation, personalization"
            }
        else:
            return {
                "risk_category": "low_risk",
                "compliance_threshold": 0.5,
                "required_checks": ["model_metadata"],
                "description": "Low risk system - spam filtering, translation, basic utilities"
            }
            
    except Exception as e:
        logger.error(f"Risk classification error: {e}")
        return default_config

def validate_structure(self):
    """Validate the existence of required folder structure for accountability."""
    logger.info("Validating folder structure for Accountability")
    
    structural_results = {}
    all_folders_exist = True
    
    for folder in self.required_folders:
        folder_path = self.project_root / folder
        exists = folder_path.exists() and folder_path.is_dir()
        structural_results[f"{folder}_exists"] = exists
        
        if not exists:
            all_folders_exist = False
            self.results["required_actions"].append(f"Create folder: {folder}/")
            logger.warning(f"Missing required folder: {folder}")
    
    self.results["structural_validation"] = structural_results
    return all_folders_exist

def analyze_file_content(self, filepath, expected_keywords, category):
    """Analyze file content semantically and check legal compliance."""
    result = {
        "found_keywords": [],
        "missing_keywords": [],
        "semantic_score": 0.0,
        "hash": self.compute_file_hash(filepath),
        "legal_basis": self.legal_framework.get(category, []),
        "permissions": self.check_file_permissions(filepath)
    }
    
    if not os.path.exists(filepath):
        result["missing_keywords"] = expected_keywords
        return result
    
    content = self.read_file_text(filepath).lower()
    if not content:
        result["missing_keywords"] = expected_keywords
        return result
    
    content_embedding = self.get_embedding(content)
    scores = []
    
    for keyword in expected_keywords:
        kw_embedding = self.get_embedding(keyword.lower())
        similarity = self.cosine_similarity(content_embedding, kw_embedding)
        scores.append(similarity)
        
        if similarity >= 0.7:
            result["found_keywords"].append(keyword)
        else:
            result["missing_keywords"].append(keyword)
    
    if scores:
        result["semantic_score"] = float(np.mean(scores))
    
    return result

def calculate_legal_compliance(self, file_analysis, category):
    """Check which legal requirements are unmet based on found keywords."""
    compliance = []
    for law_info in self.legal_framework.get(category, []):
        unmet = []
        for req in law_info.get("requirements", []):
            if not any(req.lower() in kw.lower() for kw in file_analysis.get("found_keywords", [])):
                unmet.append(req)
        compliance.append({
            "law": law_info.get("law"),
            "articles": law_info.get("articles", []),
            "unmet_requirements": unmet
        })
    return compliance

def validate_semantic_content(self):
    """Validate semantic content of each folder using specialized embeddings."""
    logger.info("Validating semantic content for Accountability")
    
    folder_requirements = {
        "decision_logs": {
            "files": ["decisions.json", "decision_log.csv", "audit_trail.json"],
            "keywords": ["timestamp", "input", "output", "model_version", "responsible_person", "dataset_hash"]
        },
        "audit_evidence": {
            "files": ["approval.pdf", "compliance_report.md", "ethics_approval.json"],
            "keywords": ["approval", "ethics_committee", "compliance", "review", "signature"]
        },
        "model_metadata": {
            "files": ["model_card.yaml", "model_info.json", "performance_metrics.json"],
            "keywords": ["algorithm", "hyperparameters", "metrics", "bias", "version", "limitations"]
        },
        "responsible_persons": {
            "files": ["responsibles.json", "governance_structure.csv", "contacts.yaml"],
            "keywords": ["name", "position", "role", "contact", "assigned_date", "responsibility"]
        },
        "monitoring_dashboards": {
            "files": ["dashboard.html", "monitoring.json", "alerts.yaml"],
            "keywords": ["performance", "alert", "anomaly", "monitoring", "dashboard", "metrics"]
        }
    }
    
    semantic_results = {}
    legal_compliance = {}
    
    for category, requirements in folder_requirements.items():
        category_path = self.project_root / category
        semantic_results[category] = {}
        legal_compliance[category] = {}
        
        if not category_path.exists():
            continue
        
        for filename in requirements["files"]:
            filepath = category_path / filename
            if filepath.exists():
                analysis = self.analyze_file_content(
                    filepath, 
                    requirements["keywords"], 
                    category
                )
                
                semantic_results[category][filename] = {
                    "semantic_score": analysis["semantic_score"],
                    "found_keywords": analysis["found_keywords"],
                    "missing_keywords": analysis["missing_keywords"],
                    "file_hash": analysis["hash"],
                    "permissions": analysis["permissions"]
                }
                
                legal_compliance[category][filename] = self.calculate_legal_compliance(analysis, category)
    
    for category in self.required_folders:
        if category in semantic_results and semantic_results[category]:
            scores = [item["semantic_score"] for item in semantic_results[category].values()]
            avg_score = sum(scores) / len(scores)
            
            self.results["semantic_validation"][f"{category}_score"] = avg_score
            
            if avg_score >= 0.75:
                feedback = f"Excellent semantic alignment in {category}"
            elif avg_score >= 0.5:
                feedback = f"Partial semantic alignment in {category}"
            else:
                feedback = f"Inadequate semantic content in {category}"
            
            self.results["semantic_validation"][f"{category}_feedback"] = feedback
    
    self.results["detailed_semantic_analysis"] = semantic_results
    self.results["legal_compliance"] = legal_compliance

def collect_system_info(self):
    """Collect comprehensive system information for audit context."""
    self.results["system_info"] = {
        "user": getpass.getuser(),
        "system": platform.system(),
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "ai_processes": self.check_ai_processes(),
        "system_utilization": self.check_system_utilization(),
        "execution_id": str(uuid.uuid4())
    }

def check_file_integrity(self):
    """Check file integrity through hashing for all accountability files."""
    integrity_checks = {}
    
    for folder in self.required_folders:
        folder_path = self.project_root / folder
        if folder_path.exists():
            file_hashes = {}
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    try:
                        with open(file_path, 'rb') as f:
                            file_hashes[str(file_path.relative_to(self.project_root))] = {
                                "sha256": hashlib.sha256(f.read()).hexdigest(),
                                "size": file_path.stat().st_size,
                                "modified": datetime.fromtimestamp(
                                    file_path.stat().st_mtime
                                ).isoformat()
                            }
                    except Exception as e:
                        logger.warning(f"Could not hash file {file_path}: {e}")
            
            integrity_checks[folder] = file_hashes
    
    self.results["integrity_checks"] = integrity_checks

def generate_recommendations(self):
    """Generate prioritized, risk-aware recommendations based on audit findings."""
    recommendations = []
    risk_category = self.results["risk_configuration"]["risk_category"]
    
    def add_recommendation(severity, category, message, remediation):
        recommendations.append({
            "severity": severity,
            "category": category,
            "message": message,
            "remediation": remediation,
            "risk_category": risk_category
        })
    
    # Analyze missing files
    for category, files in self.results.get("detailed_semantic_analysis", {}).items():
        for filename, file_data in files.items():
            if file_data.get("status") == "missing":
                if risk_category == "high_risk" and category in self.results["risk_configuration"]["required_checks"]:
                    add_recommendation(
                        "critical",
                        "missing_file",
                        f"Required file missing: {filename}",
                        f"Create {filename} with appropriate accountability documentation"
                    )
                elif category in self.results["risk_configuration"]["required_checks"]:
                    add_recommendation(
                        "high",
                        "missing_file",
                        f"Required file missing: {filename}",
                        f"Create {filename} with appropriate accountability documentation"
                    )
    
    # Analyze unmet legal requirements
    for category, files in self.results.get("legal_compliance", {}).items():
        for filename, file_compliance in files.items():
            for law_compliance in file_compliance:
                if law_compliance.get("unmet_requirements"):
                    for requirement in law_compliance["unmet_requirements"]:
                        add_recommendation(
                            "high",
                            "legal_compliance",
                            f"Unmet legal requirement: {requirement} in {filename}",
                            f"Update {filename} to address {requirement} requirement from {law_compliance['law']}"
                        )
    
    # Sort recommendations by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recommendations.sort(key=lambda x: severity_order[x["severity"]])
    
    return recommendations

def determine_overall_status(self):
    """Determine overall audit status based on all validations."""
    structural_valid = all(self.results["structural_validation"].values())
    
    semantic_scores = [
        self.results["semantic_validation"]["decision_logs_score"],
        self.results["semantic_validation"]["audit_evidence_score"],
        self.results["semantic_validation"]["model_metadata_score"],
        self.results["semantic_validation"]["responsible_persons_score"],
        self.results["semantic_validation"]["monitoring_dashboards_score"]
    ]
    
    avg_semantic_score = sum(semantic_scores) / len(semantic_scores) if semantic_scores else 0
    
    legal_issues = 0
    for category in self.results.get("legal_compliance", {}).values():
        for file_compliance in category.values():
            for law in file_compliance:
                legal_issues += len(law.get("unmet_requirements", []))
    
    if avg_semantic_score >= 0.75 and structural_valid and legal_issues == 0:
        self.results["status"] = "approved"
    elif avg_semantic_score >= 0.5 and structural_valid:
        self.results["status"] = "pending"
    else:
        self.results["status"] = "failed"
    
    if legal_issues > 0:
        self.results["required_actions"].append(
            f"Address {legal_issues} unmet legal requirements across accountability documents"
        )

def run_audit(self):
    """Execute complete accountability audit with all validation steps."""
    logger.info(f"Starting Accountability audit for: {self.project_root}")
    
    try:
        # Step 1: Risk classification
        self.results["risk_configuration"] = self.classify_risk_level()
        
        # Step 2: Collect system information
        self.collect_system_info()
        
        # Step 3: Validate folder structure
        structure_valid = self.validate_structure()
        
        # Step 4: Validate semantic content (only if structure exists)
        if structure_valid:
            self.validate_semantic_content()
        
        # Step 5: Check file integrity
        self.check_file_integrity()
        
        # Step 6: Generate recommendations
        self.results["risk_based_recommendations"] = self.generate_recommendations()
        
        # Step 7: Determine overall status
        self.determine_overall_status()
        
        # Step 8: Calculate compliance score
        total_checks = 0
        compliant_checks = 0
        for category in self.results.get("legal_compliance", {}).values():
            for file_result in category.values():
                if file_result:
                    total_checks += 1
                    if all(not law.get("unmet_requirements") for law in file_result):
                        compliant_checks += 1
        
        compliance_score = round((compliant_checks / total_checks * 100) if total_checks > 0 else 0, 2)
        
        self.results["compliance_summary"] = {
            "total_checks": total_checks,
            "compliant_checks": compliant_checks,
            "compliance_score": compliance_score,
            "compliance_status": "compliant" if compliance_score >= self.results["risk_configuration"]["compliance_threshold"] * 100 else "non_compliant"
        }
        
        # Step 9: Save results to JSON file
        self.save_results()
        
        logger.info(f"Accountability audit completed. Status: {self.results['status']}")
        return self.results
        
    except Exception as e:
        logger.error(f"Audit failed with error: {e}")
        self.results["status"] = "failed"
        self.results["error"] = str(e)
        self.save_results()
        return self.results

def save_results(self):
    """Save audit results to JSON file in the expected format for Agent Generator."""
    output_dir = Path("audit/agents/Accountability")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "resultado.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Results saved to: {output_path}")
    return output_path
class SemanticAnalyzer:
"""Local semantic analyzer using sentence-transformers embeddings"""

text
def __init__(self):
    self.model = None
    self.embedding_cache = {}
    
def load_model(self):
    """Load the local sentence-transformers model"""
    try:
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        logger.info("BAAI/bge-small-en-v1.5 embedding model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Embedding model load failed: {e}")
        return False

def get_embedding(self, text):
    """Get embedding for text with caching"""
    if text in self.embedding_cache:
        return self.embedding_cache[text]
    
    if self.model is None:
        if not self.load_model():
            return None
    
    try:
        embedding = self.model.encode(text, convert_to_tensor=False)
        self.embedding_cache[text] = embedding
        return embedding
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return None

def semantic_similarity(self, text1, text2):
    """Calculate cosine similarity between two texts"""
    emb1 = self.get_embedding(text1)
    emb2 = self.get_embedding(text2)
    
    if emb1 is None or emb2 is None:
        return 0.0
    
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    return float(similarity)
def main():
"""Main execution function for command-line usage."""
parser = argparse.ArgumentParser(description="AI Accountability Auditor")
parser.add_argument("--base-path", default=".", help="Base path to audit (default: current directory)")
parser.add_argument("--output-dir", default="audit_reports", help="Output directory for reports")
parser.add_argument("--dry-run", action="store_true", help="Perform dry run without saving reports")
args = parser.parse_args()

text
runner = AccountabilityRunner(args.base_path)
results = runner.run_audit()

print(f"\nAccountability Audit Results:")
print(f"Status: {results['status']}")
print(f"Timestamp: {results['timestamp']}")
print(f"Risk Category: {results['risk_configuration']['risk_category']}")
print(f"Compliance Score: {results['compliance_summary']['compliance_score']}%")

if results['required_actions']:
    print("\nRequired Actions:")
    for action in results['required_actions']:
        print(f"- {action}")

if results['risk_based_recommendations']:
    print("\nRecommendations:")
    for rec in results['risk_based_recommendations']:
        print(f"- [{rec['severity'].upper()}] {rec['message']}")

# Exit code based on compliance and risk
compliance_score = results["compliance_summary"]["compliance_score"]
risk_category = results["risk_configuration"]["risk_category"]

if risk_category == "high_risk" and compliance_score < 90:
    sys.exit(1)
elif risk_category == "medium_risk" and compliance_score < 70:
    sys.exit(1)
else:
    sys.exit(0)
if name == "main":
main()