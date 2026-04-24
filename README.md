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

## ▶️ Como rodar o projeto (Step by Step)

### 📥 1. Clone o repositório
git clone https://github.com/luhwithbpd/dashboard-gastos.git
cd dashboard-gastos/dashboard-coletas

### 🐍 2. Crie o ambiente virtual
python -m venv venv

### ⚡ 3. Ative o ambiente virtual

Windows (PowerShell)
.\venv\Scripts\Activate.ps1

Se der erro:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

Windows (CMD)
venv\Scripts\activate

Linux / Mac
source venv/bin/activate

### 📦 4. Instale as dependências
pip install -r requirements.txt

### 🔐 5. Configure as credenciais do Google
mkdir credentials

Coloque o arquivo:
credentials/google-service-account.json

### 🔗 6. Compartilhe a planilha
Copie do JSON:
"client_email": "seu-email@projeto.iam.gserviceaccount.com"

Depois compartilhe no Google Sheets como leitor.

### ⚙️ 7. Configure o ID da planilha
Arquivo: app/config.py

SPREADSHEET_ID = "SEU_ID"
WORKSHEET_NAME = "SUA_ABA"

### 🚀 8. Execute o dashboard
streamlit run app/main.py

ou

python -m streamlit run app/main.py

### 🌐 9. Acesse no navegador
http://localhost:8501