## [SERVIÇO PREMIUM] ETL Financeiro com Delta Lake e Unity Catalog — Pipeline Automatizado para Instituições Financeiras

**Objetivo:** Demonstrar domínio completo da certificação Databricks Data Engineer Associate, construindo um pipeline de ETL robusto, seguro e governado para dados financeiros — utilizando Delta Lake para confiabilidade, Unity Catalog para governança e automação via Jobs e DBT. Este não é um notebook. É um sistema de produção real usado por bancos e fintechs.

**Tecnologias-Chave (comprovadamente utilizadas):**  
- **Databricks Workspace (Unity Engine)**: Ambiente unificado para ingestão, transformação e análise  
- **Delta Lake**: Tabelas ACID-compliant com versionamento, time travel e schema evolution  
- **Unity Catalog**: Governança centralizada de metadados, permissões e auditoria (RBAC)  
- **Auto Loader**: Ingestão incremental de arquivos CSV/JSON em tempo real do cloud storage  
- **DBT (Data Build Tool)**: Transformações SQL baseadas em modelos com testes e documentação  
- **PySpark**: Engenharia de features complexas com DataFrame API  
- **Databricks Jobs**: Agendamento semanal de pipelines com alertas de falha  
- **Databricks SQL**: Consultas OLAP e dashboards interativos  
- **Python 3.10**, Pandas, PyTest (testes de integridade dos dados)  
- **Git + Databricks Repos**: Versionamento de código no GitHub integrado ao workspace  

**Entregáveis Reais (o que foi construído e pode ser verificado no repositório):**  
✅ **Pipeline de ingestão automatizada (Auto Loader)**:  
   - Fonte: Arquivos CSV diários de transações bancárias armazenados no Azure Blob Storage / S3  
   - Schema inferido automaticamente com validação estrita  
   - Ingestão incremental: apenas novos arquivos processados (não reprocessa tudo!)  
   - Dados escritos em tabela Delta: `finance.raw_transactions`  
   - Log de ingestão armazenado em tabela audit: `audit.ingestion_log` (data_hora, file_name, records_processed, status)

✅ **Modelagem com Delta Lake e Time Travel**:  
   - Tabela principal: `finance.clean_transactions` (limpa, enriquecida, normalizada)  
   - Colunas: `transaction_id`, `account_id`, `amount`, `currency`, `timestamp`, `merchant_category`, `is_fraud_flag`  
   - Histórico de versões acessível:  
     ```sql
     SELECT * FROM finance.clean_transactions TIMESTAMP AS OF '2025-04-01T10:00:00Z'
     ```
   - Schema evolution suportada: novo campo `payment_method` adicionado sem quebrar pipelines

✅ **Governança com Unity Catalog**:  
   - Esquema `finance` criado no Unity Catalog  
   - Permissões definidas por grupo:  
     - Analistas: `SELECT` apenas em tabelas limpas  
     - Engenheiros: `SELECT`, `INSERT`, `UPDATE` nas tabelas raw  
     - Administradores: acesso total  
   - Auditoria ativada: todos os acessos registrados em `system.access.audit_logs`  
   - Metadados completos: descrição das colunas, proprietário, data de criação

✅ **Transformações com DBT (Data Build Tool)**:  
   - Modelos SQL organizados em `/models/`:  
     - `stg_transactions.sql` → staging  
     - `int_daily_summary.sql` → agregação di