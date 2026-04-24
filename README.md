# 🚚 Dashboard de Coletas

Dashboard interativo para controle financeiro de operações logísticas (coletas), com foco em análise de receitas, custos e lucratividade.

---

## 📊 Sobre o Projeto

Este projeto foi desenvolvido com o objetivo de transformar dados operacionais registrados em uma planilha do Google Sheets em **informações visuais e acionáveis**.

A aplicação realiza:

- Ingestão de dados via Google Sheets API
- Tratamento e padronização de dados
- Cálculo de métricas financeiras
- Visualização interativa com dashboard

O sistema permite uma visão clara da operação diária, ajudando na tomada de decisão.

---

## 🚀 Funcionalidades

- 📥 Integração com Google Sheets
- 🧹 Limpeza e padronização de dados (ETL)
- 💰 Cálculo de métricas:
  - Receita total
  - Gastos totais
  - Lucro líquido
  - Ticket médio por coleta
  - Custo médio por coleta
- 📅 Filtro por mês
- 📈 Gráficos:
  - Receita x Gastos x Lucro
  - Gastos por categoria
- 🧠 Insights automáticos:
  - Melhor dia
  - Pior dia
- 📋 Visualização tabular dos dados

---

## 🛠️ Stack Tecnológica

- **Python**
- **Pandas**
- **Streamlit**
- **Google Sheets API**
- **gspread**

---

## ▶️ Step by Step para rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/luhwithbpd/dashboard-gastos.git
cd dashboard-gastos/dashboard-coletas
2. Crie o ambiente virtual
python -m venv venv
3. Ative o ambiente virtual
Windows PowerShell
.\venv\Scripts\Activate.ps1

Se der erro de permissão:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
Windows CMD
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
4. Instale as dependências
pip install -r requirements.txt
5. Configure as credenciais do Google

Crie a pasta:

mkdir credentials

Coloque o arquivo JSON da Service Account dentro dela com o nome:

google-service-account.json

O caminho final deve ficar assim:

credentials/google-service-account.json
6. Compartilhe a planilha com a Service Account

Abra o arquivo JSON e copie o valor de:

"client_email": "sua-service-account@projeto.iam.gserviceaccount.com"

Depois abra sua planilha no Google Sheets e compartilhe com esse e-mail como Leitor.

7. Configure o ID da planilha

No arquivo:

app/config.py

Configure:

SPREADSHEET_ID = "ID_DA_SUA_PLANILHA"
WORKSHEET_NAME = "NOME_DA_ABA"

O ID fica no link da planilha:

https://docs.google.com/spreadsheets/d/ESSE_TRECHO_AQUI/edit
8. Rode o dashboard
streamlit run app/main.py

Ou:

python -m streamlit run app/main.py
9. Acesse no navegador

Normalmente o Streamlit abre automaticamente. Caso não abra, acesse:

http://localhost:8501