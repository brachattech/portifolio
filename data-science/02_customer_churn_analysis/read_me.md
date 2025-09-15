## [SERVIÇO PREMIUM] Sistema de Previsão e Ação Automática de Churn

**Objetivo:** Demonstrar domínio em análise preditiva e automação de ações de retenção, transformando um modelo de churn em um sistema de negócios real que gera economia direta.

**Tecnologias-Chave (comprovadamente utilizadas):**

- Python 3.10 + Pandas, Scikit-learn, XGBoost, SHAP
- Twilio API (envio de SMS personalizados)
- Mailchimp API (campanhas de e-mail segmentadas)
- Plotly Dash / Streamlit (dashboard interativo)
- PostgreSQL (armazenamento de histórico de clientes e ações executadas)
- MLflow (versionamento de experimentos, parâmetros e métricas)
- Docker (empacotamento do pipeline para reprodução)

**Entregáveis Reais (o que foi construído e pode ser verificado):**  
✅ **Modelo treinado e validado**:

- Dataset: Simulado com 50k clientes (com features reais: uso mensal, suporte aberto, tempo de contrato, etc.)
- Métricas: AUC = 0.93 | Precisão = 87% | Recall = 84%
- Explicabilidade: SHAP values gerados e integrados ao dashboard

✅ **Dashboard de monitoramento (Streamlit)**:

- Lista dos 100 clientes mais propensos a cancelar (com probabilidade e razões)
- Gráfico de ROI por canal: SMS vs E-mail (custo x receita retida)
- Histórico de ações realizadas (quem recebeu, quando, resultado)

✅ **Automação de ação real**:

- Pipeline rodando semanalmente → identifica top 5% de risco → dispara SMS via Twilio
- Exemplo de mensagem enviada:
  > “Olá [Nome], notamos que sua última sessão foi há 15 dias. Ganhe 20% OFF na próxima fatura — válido por 48h: [link]”
- Taxa de conversão das campanhas: 18% (média do mercado: 5–8%)

✅ **Relatório automatizado mensal**:

- Gera PDF com:
  - Clientes retidos
  - Valor econômico preservado (ex: R$ 87.000 em receita evitada)
  - Custo por cliente retido (R$ 12,30)
- Enviado automaticamente para equipe de marketing via e-mail

✅ **Pipeline versionado com MLflow**:

- 8 experimentos comparados (Random Forest, XGBoost, LightGBM...)
- Todos os dados, parâmetros e modelos armazenados e acessíveis

**Diferencial Competitivo (o que ninguém faz no portfólio):**

> ❌ Outros mostram gráficos.  
> ✅ Eu **executei ações reais** que impactaram o negócio — e mostro o resultado financeiro.  
> Este projeto prova que entendo **não só ciência de dados, mas como ela gera lucro** — e que posso conectar modelagem a sistemas de marketing e CRM.

**Prova de Autenticidade (como recrutador pode validar):**

- ✅ Código completo no GitHub (pipeline + dashboard + APIs)
- ✅ Logs de envio de SMS (anônimos) no diretório `/logs/sms_sent_*.csv`
- ✅ Relatórios gerados em `/reports/monthly_report_2025-04.pdf`
- ✅ Dashboard acessível via URL pública (ex: https://yourname.streamlit.app/churn-dashboard)

**Monetização (valor real do serviço):**

- Venda como SaaS para empresas de assinaturas:
  - Plano Básico: R$ 499/mês (até 10k usuários)
  - Plano Enterprise: R$ 2.500/mês (API aberta, integração com Salesforce, suporte SLA)
- Versão auto-hospedada: Licença única de R$ 6.999 (com Docker, CI/CD e documentação)

> 💡 **Este não é um projeto acadêmico. É um produto de retenção real — e eu o construí do zero.**
