# Complete Manual for Junior Developers — Enhanced Accountability Audit Runner for AI Systems (Risk-Aware Version)

This document explains every part of the Accountability Audit Runner in plain English, now upgraded to include **AI Risk Assessment**. No code is shown — only clear, practical explanations designed for junior developers to understand the full logic, flow, and purpose of the system.

---

## 🎯 OVERVIEW — NOW WITH RISK INTELLIGENCE

This script is no longer just an auditor — it’s a **risk-aware compliance engine**.

It doesn’t treat all AI systems the same. Instead, it:

✅ Classifies the AI system into one of three risk levels:  
 → **High Risk** (e.g., medical diagnosis, credit approval, hiring)  
 → **Medium Risk** (e.g., recommendation engines, content moderation)  
 → **Low Risk** (e.g., spell check, spam filters)

✅ Adjusts the audit strictness based on that risk level:  
 → High risk = stricter thresholds, more required checks  
 → Low risk = lighter checks, lower thresholds

✅ Generates tailored recommendations based on risk:  
 → High risk = urgent actions, human oversight, traceability  
 → Medium risk = documentation improvements, version tracking  
 → Low risk = basic hygiene checks

✅ Produces a risk report inside the final audit output, highlighting:  
 → Compliance score adjusted for risk  
 → Critical findings  
 → Recommended next steps

It’s like having a legal and technical auditor who reads your system’s purpose, understands how dangerous a mistake could be, and adjusts their checklist accordingly.

---

## 🧩 SECTION 1: RISK CATEGORIES — THE RULES OF STRICTNESS

At the heart of the new system is a risk classification dictionary. It defines:

### High Risk
- **Description**: Systems that make critical decisions with significant human impact (health, finance, justice, employment).
- **Examples**: Medical diagnosis tools, loan approval engines, criminal risk scoring, hiring algorithms.
- **Audit Strictness**: Highest — requires 90% semantic match for keywords.
- **Required Checks**: Full audit — metadata, decision logs, audit evidence, responsible persons, version control.

### Medium Risk
- **Description**: Systems with moderate impact on user rights or experience.
- **Examples**: Personalized recommendations, content classifiers, customer service chatbots.
- **Audit Strictness**: Medium — 70% semantic match required.
- **Required Checks**: Core audit — metadata, decision logs, responsible persons.

### Low Risk
- **Description**: Systems with minimal or no significant consequences.
- **Examples**: Spam filters, auto-translation, grammar correction.
- **Audit Strictness**: Light — 50% semantic match required.
- **Required Checks**: Basic — only model metadata is audited.

This ensures the system doesn’t waste time over-auditing a spell checker — but goes full forensic mode on a hiring algorithm.

---

## 🔍 SECTION 2: RISK DETECTION — HOW IT KNOWS THE DANGER LEVEL

The system automatically determines the risk category by reading the `model_info.json` file.

It looks for:

- The **intended use** of the model (e.g., “medical diagnosis”, “credit scoring”)
- The **impact level** declared by the team (e.g., “high”, “medium”, “low”)

It scans the “intended use” text for risk keywords:

- High-risk triggers: “medical”, “financial”, “legal”, “criminal”, “hiring”, “credit”
- Medium-risk triggers: “recommendation”, “content”, “personalized”, “advertising”

If it finds a high-risk keyword — or if impact_level = “high” — it classifies the system as High Risk.

If no clear signal is found, it defaults to Medium Risk (safe assumption).

If the file is missing or unreadable, it logs a warning and still defaults to Medium Risk — no crash, no stop.

---

## 📊 SECTION 3: RISK-AWARE AUDIT — THE SMART CHECKLIST

Once the risk level is known, the audit adapts.

It:

- Loads the correct **compliance threshold** (0.9, 0.7, or 0.5)
- Only runs **required checks** for that risk level (skips irrelevant ones)
- Tracks **compliance metrics**:
  - Total checks performed
  - Passed vs failed checks
  - Final compliance score (passed / total)

For example:
→ A High Risk system must pass checks in 5 categories.  
→ If 4/5 pass with ≥90% match, compliance score = 80%.  
→ A Low Risk system only checks 1 category — if it passes with ≥50%, score = 100%.

This score is not absolute — it’s relative to the risk level. An 80% score on a High Risk system might still need urgent fixes. The same score on a Low Risk system might be perfectly acceptable.

---

## 🚨 SECTION 4: RISK-BASED RECOMMENDATIONS — SMART ACTION ITEMS

After the audit, the system generates a list of recommendations — prioritized by risk and severity.

### General Recommendations
- If overall compliance score is below 70%, it flags:  
  → “Low compliance. Urgent review required.”  
  → With action items: full audit, document gaps, create action plan.

### High Risk Recommendations
- Focus on **traceability** and **human oversight**:
  → “Implement detailed decision logs with immutability”
  → “Establish formal human review process for critical decisions”
  → “Assign responsible persons and escalation paths”

### Medium Risk Recommendations
- Focus on **documentation** and **transparency**:
  → “Improve technical documentation of model decisions”
  → “Document model limitations and version history”

### Low Risk Recommendations
- Usually minimal — unless compliance is very low, then it suggests basic hygiene improvements.

Each recommendation includes:
- Severity (HIGH, MEDIUM, LOW)
- Category (e.g., DECISION_TRACEABILITY, DOCUMENTATION)
- Clear recommendation text
- Concrete action items

This turns the audit from a “pass/fail” report into an **actionable roadmap**.

---

## 📈 SECTION 5: RISK REPORT — THE EXECUTIVE SUMMARY

The system bundles all risk intelligence into a dedicated “risk_report” section inside the final audit context.

It includes:

- **Risk Category**: e.g., “high_risk”
- **Description**: Plain-English explanation of what this means
- **Compliance Score**: Adjusted for risk level
- **Risk Level Label**: “ALTO”, “MÉDIO”, or “BAIXO” (for easy reading)
- **Critical Findings**: Filters only HIGH severity recommendations — so leaders see the fires that need putting out first

This report is embedded in the main JSON output — no extra files, no confusion.

---

## 🚀 SECTION 6: MAIN EXECUTION — NOW RISK-AWARE

When you run the script, here’s the new flow:

### Step 1: Define Expected Structure (Same as Before)
Still maps categories to files and keywords — but now, not all categories will be checked, depending on risk.

### Step 2: Set Audit Location
Still starts at `/var/data` (or your configured base path).

### Step 3: Detect Risk Level
→ Reads `model_info.json`  
→ Extracts intended use and impact level  
→ Classifies as high/medium/low risk  
→ Logs the decision

### Step 4: Run Risk-Adapted Audit
→ Uses the correct compliance threshold  
→ Only audits required categories  
→ Tracks pass/fail per check  
→ Calculates risk-adjusted compliance score  
→ Adds system process and resource info

### Step 5: Generate Risk-Based Recommendations
→ Creates prioritized list of fixes and improvements  
→ Embeds them in the context

### Step 6: Build Risk Report
→ Summarizes risk level, score, and critical findings  
→ Adds it to the context

### Step 7: Generate & Save Audit Report
→ Creates trace JSON with:
  - Unique ID, timestamp, user, system info
  - Full analysis context (now including risk data)
  - Execution metadata flagging this as a “risk_aware_audit”
  - Count of generated recommendations

### Step 8: Send to Orchestrator (Optional)
→ Same as before — saves to `/var/orchestrator_inputs` if configured

---

## ✅ SECTION 7: OUTPUT STRUCTURE — WHAT YOU GET

The final JSON trace now includes these new sections:

```json
{
  "risk_category": "high_risk",
  "compliance_summary": {
    "total_checks": 15,
    "passed_checks": 12,
    "failed_checks": 3,
    "compliance_score": 0.8
  },
  "risk_report": {
    "risk_level": "ALTO",
    "critical_findings": [
      {
        "severity": "HIGH",
        "category": "DECISION_TRACEABILITY",
        "recommendation": "Implementar logs detalhados de todas as decisões automatizadas"
      }
    ]
  },
  "risk_based_recommendations": [
    // Full list of prioritized action items
  ],
  "execution_metadata": {
    "risk_aware_audit": true,
    "risk_assessment_performed": true,
    "recommendations_generated": 5
  }
}