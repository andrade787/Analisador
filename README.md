# Aanalisador


## Sobre
Este projeto tem como objetivo analisar o histórico de dividendos de ativos, calcular preços justos usando modelos financeiros, e recomendar ações ou fundos imobiliários (FII) com base em suas cotações atuais e modelos de valuation.


## Funcionalidades
- Coleta de dados históricos de dividendos de ativos usando a biblioteca yfinance.
- Cálculo do preço justo de ativos usando os modelos de Gordon e Bazin.
- Recomendação de compra com base nos preços calculados.
- Exibição dos resultados em um DataFrame do Pandas.


## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/andrade787/Analisador.git
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    ```
    
    2.1
      Ative o ambiente virtual:
        ```bash
        venv\Scripts\activate
        ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Inicialização do Projeto

    python manage.py runserver


## API

### Exemplo de Solicitação (POST)

**Endpoint:** `http://localhost:8000/api/v1/calcular-dados/`

**Método:** `POST`

**Corpo da Solicitação (Body):**

```json
{
  "tickers_info": [
    "KNCR11.SA;FII",
    "GARE11.SA;FII",
    "BBDC4.SA;AÇÃO"
  ],
  "taxa_retorno": [50.08, 0.10],
  "taxa_crescimento": 0.005,
  "anos_solicitados": 5
}

