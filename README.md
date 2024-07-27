# Aanalisador

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

