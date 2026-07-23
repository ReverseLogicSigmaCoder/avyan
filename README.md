# 🛡️ PROJECT AVYAN: Autonomous Sovereign Cyber Defense Platform

> **Scanning Engine:** SUDARSHAN | **AI Assistant:** SARATHI  
> **Mission:** Sovereign Cyber Threat Intelligence, Passive Monitoring & SOAR Pipeline

---

## 🏛️ System Architecture & Workflow

Project AVYAN is an automated threat intelligence gathering and incident logging framework designed for passive infrastructure assessment and standardized security reporting.
+-------------------------------------------------------------------+
|                     EXTERNAL THREAT SOURCES                       |
|   (Certificate Transparency Logs, Threat Feeds, Open APIs)        |
+-------------------------------------------------------------------+
|
v
+-------------------------------------------------------------------+
|                     SUDARSHAN SOAR ENGINE                         |
|   - Multi-Source Data Ingestion                                   |
|   - Indicator Deduplication & Normalization                       |
|   - Standardized Severity Classification                          |
+-------------------------------------------------------------------+
|
+----------------+----------------+
|                                 |
v                                 v
+---------------------------------+ +-------------------------------+
|    JSON Incident Logger         | |     Telegram Alert Hub        |
|  (CERT-In Format Compliance)    | |  (Real-Time SOC Dispatch)   |
+---------------------------------+ +-------------------------------+
---

## ✨ Key Features

- **Passive Reconnaissance Engine:** Queries Certificate Transparency (CT) logs and public indicators without aggressive scanning.
- **Automated SOAR Pipeline:** Executes scheduled cloud runs via GitHub Actions for continuous monitoring.
- **CERT-In Compliant Reporting:** Formats raw security logs into structured JSON incident reports for audit readiness.
- **Real-Time Notification Dispatch:** Integrates with Telegram API for instant SOC alert broadcasting.

---

## 📂 Repository Structure

- `sudarshan_soar_engine.py`: Core Threat Intelligence aggregation and SOAR pipeline.
- `cert_in_reporter.py`: CERT-In compliant JSON incident report generator.
- `.github/workflows/`: Automated CI/CD scheduled workflows for background monitoring.
- `reports/`: Audit logs and encrypted incident files.

---

## 🔒 Ethical & Legal Compliance

Project AVYAN strictly adheres to **Coordinated Vulnerability Disclosure (CVD)** guidelines, passive OSINT principles, and non-intrusive threat monitoring practices.
