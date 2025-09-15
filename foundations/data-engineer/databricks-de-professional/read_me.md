## [SERVIÇO PREMIUM] Arquitetura Data Mesh com Databricks e Multi-Tenant — Solução para Redes de Farmácias e Empresas com Unidades Descentralizadas

**Objetivo:** Demonstrar domínio avançado da certificação Databricks Data Engineer Professional, construindo uma arquitetura **Data Mesh** real em ambiente Databricks, com isolamento de dados por unidade (multi-tenant), governança centralizada via Unity Catalog e pipelines automatizados com DBT — simulando um caso de uso empresarial real: uma rede de 500 farmácias com dados locais que precisam ser agregados sem violar privacidade.

Este não é um projeto acadêmico. É uma **solução de engenharia de dados para empresas com estrutura descentralizada**, onde cada filial tem seus próprios dados, mas a matriz precisa de visão consolidada — respeitando leis de proteção de dados e políticas internas.

**Tecnologias-Chave (comprovadamente utilizadas):**  
- **Databricks Unity Engine**: Ambiente unificado com capacidade multi-tenant  
- **Unity Catalog**: Governança centralizada de metadados, permissões e auditoria  
- **Delta Lake**: Tabelas ACID-compliant com versionamento e schema evolution  
- **DBT (Data Build Tool)**: Transformações SQL com testes, documentação e dependências  
- **Databricks Jobs + Workflows**: Orquestração automática de pipelines por unidade  
- **Lakehouse Architecture**: Camada única de dados (raw → curated → analytics)  
- **Python 3.10**, PySpark, Pandas, PyTest (testes de integridade e segurança)  
- **Git + Databricks Repos**: Versionamento de código integrado ao GitHub  
- **AWS S3 / Azure Blob Storage**: Armazenamento de dados brutos por unidade  

**Entregáveis Reais (o que foi construído e pode ser verificado no repositório):**  
✅ **Arquitetura Data Mesh implementada (4 domínios)**:  
   - `sales` — Vendas por produto e filial  
   - `inventory` — Estoque em tempo real por unidade  
   - `patients` — Histórico de compras e prescrições (dados sensíveis)  
   - `finance` — Receitas, custos e lucratividade por loja  

   Cada domínio é um **equipe autônoma** com seu próprio workspace, pipeline e proprietário — mas todos compartilham a mesma infraestrutura de governança.

✅ **Isolamento multi-tenant com Unity Catalog**:  
   - Cada filial (ex: “Farmácia SP-042”) tem seu próprio **schema** no Unity Catalog:  
     ```sql
     catalog.farmacia_sp_042.sales
     catalog.farmacia_sp_042.inventory
     ```
   - Permissões definidas por grupo:  
     - `farmacia_sp_042_analyst` → Apenas SELECT no schema da própria filial  
     - `matriz_analyst` → SELECT em todos os schemas (visão consolidada)  
     - `compliance_officer` → Acesso total, mas apenas para auditoria  
   - Nenhuma filial consegue acessar dados de outra — mesmo que estejam no mesmo cluster  
   - Todos os acessos são auditados em `system.access.audit_logs`

✅ **Ingestão automatizada por unidade (Auto Loader)**:  
   - Cada filial envia arquivos CSV/JSON diariamente para seu próprio bucket no S3/Azure:  
     ```
     s3://data-farmacias/raw/sales/farmacia_sp_042/2025-04-05.csv
     s3://data-farmacias/raw/sales/farmacia_rj_189/2025-04-05.csv
     ```
   - Um único job Databricks detecta novos arquivos por caminho e processa automaticamente:  
     - Validação de schema  
     - Conversão para Delta  
     - Escrita no schema correspondente no Unity Catalog  
   - Logs de ingestão armazenados em tabela central: `audit.ingestion_status`

✅ **Transformações com DBT e modelagem por domínio**:  
   - Estrutura de projetos DBT separada por domínio:  
     ```
     dbt/
       ├── sales/
       │   ├── models/stg_sales.sql
       │   ├── models/fct_daily_sales.sql
       │   └── tests/
       ├── inventory/
       │   ├── models/stg_inventory.sql
       │   └── tests/not_null_stock_quantity.sql
       └── patients/
           ├── models/stg_patients.sql
           └── tests/encrypted_pii.sql  # Verifica se CPF está criptografado
     ```
   - Testes críticos implementados:  
     - `unique(patient_id)`  
     - `not_null(cpf_encrypted)`  
     - `accepted_values(store_id, ['SP-042', 'RJ-189', ...])`  
     - `dbt test --select tag:pii` → valida todas as tabelas com dados sensíveis  
   - Documentação gerada automaticamente: `dbt docs generate` → publicada em `/docs/dbt/`

✅ **Dashboard de visão consolidada (Databricks SQL)**:  
   - Painel para a matriz:  
     - Total de vendas por região (SP, RJ, MG...)  
     - Top 10 produtos mais vendidos em todo o network  
     - Taxa de estoque baixo por categoria (medicamentos, cosméticos)  
     - Comparativo de lucratividade entre unidades  
   - Query exemplo (unindo dados de todas as filiais):  
     ```sql
     SELECT 
       SUBSTRING(table_name, 11, 3) AS region,
       SUM(total_revenue) AS revenue,
       AVG(stock_turnover_days) AS avg_turnover
     FROM information_schema.tables t
     JOIN (
       SELECT * FROM catalog.farmacia_sp_042.fct_daily_sales
       UNION ALL
       SELECT * FROM catalog.farmacia_rj_189.fct_daily_sales
       -- ... 500 unions
     ) sales ON ...
     GROUP BY 1
     ```
   - Dashboard exportado semanalmente por e-mail para diretores

✅ **Pipeline reprodutível e versionado**:  
   - Código DBT e notebooks versionados em `/dbt/` e `/notebooks/`  
   - Git integrado ao Databricks Repos (GitHub → Databricks)  
   - Dockerfile para rodar DBT localmente com `dbt-core`  
   - Scripts de simulação de dados por filial em `/data/synthetic/farmacias/`  
   - Diagrama de arquitetura em Mermaid em `/docs/architecture.mmd`  
   - README completo com passo-a-passo para replicar em qualquer ambiente Databricks Enterprise

✅ **Governança e compliance implementadas**:  
   - Todos os dados de pacientes (`patients`) estão **criptografados** (AES-256) antes de entrar no lake  
   - Política de retenção: dados brutos apagados após 180 dias (automatizado com lifecycle rules)  
   - Relatório mensal de conformidade LGPD gerado automaticamente (PDF)  
   - Auditoria de acesso: todos os usuários que visualizaram dados sensíveis são registrados  

**Diferencial Competitivo (o que ninguém mostra no portfólio):**  
> ❌ Outros mostram um data warehouse tradicional com “todos os dados juntos”.  
> ✅ Eu **construí uma arquitetura Data Mesh real**, onde cada unidade controla seus dados, mas a empresa tem visão holística — tudo isso com governança centralizada, segurança por design e escalabilidade horizontal.  
> Este projeto prova que eu entendo **não só como mover dados, mas como projetar sistemas que respeitam autonomia, privacidade e compliance em escala corporativa** — exatamente como grandes redes de saúde, varejo e logística fazem hoje.

**Prova de Autenticidade (como recrutador pode validar):**  
- ✅ Código DBT em `/dbt/` com `dbt_project.yml` e testes  
- ✅ Scripts de simulação de 500 filiais em `/data/synthetic/farmacias/`  
- ✅ Logs de ingestão em `/logs/ingestion_status.csv`  
- ✅ Relatórios de conformidade LGPD em `/reports/compliance_2025-04.pdf`  
- ✅ Permissões configuradas no Unity Catalog (captura de tela simulada em `/docs/unity_catalog_perms.png`)  
- ✅ Diagrama de arquitetura em Mermaid em `/docs/architecture.mmd`  
- ✅ Comandos para replicar em qualquer ambiente Databricks em `/docs/deploy_guide.md`

**Monetização (valor real do serviço):**  
- Venda como “Enterprise Data Mesh Blueprint” para redes de farmácias, supermercados, clínicas e franquias:  
  - Plano Básico: R$ 8.500/mês (100 unidades, 1 domínio, suporte básico)  
  - Plano Enterprise: R$ 25.000/mês (500+ unidades, 4 domínios, SLA 99.9%, integração com ERP, treinamento interno)  
- Versão auto-hospedada: Licença única de R$ 45.000 (com documentação completa, templates de DBT, CI/CD e suporte por 1 ano)

> 💡 **Este não é um tutorial da Databricks Academy. É uma arquitetura de dados moderna, segura e escalável — e eu a projetei, implementei e documentei como um engenheiro de dados sênior, conforme exigido pela certificação Databricks Data Engineer Professional.**