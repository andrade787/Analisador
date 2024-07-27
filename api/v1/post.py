import yfinance as yf
import pandas as pd
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def calcular_dados(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            tickers_info = body.get(
                "tickers_info", []
            )  # RECEBER OS ATIVOS QUE O USUARIO QUER VERFICIAR
            taxa_retorno = body.get("taxa_retorno", (0.08, 0.10))
            taxa_crescimento = body.get("taxa_crescimento", 0.005)
            anos_solicitados = body.get("anos_solicitados", 5)

            dados_ativos = []

            def coleta_dividendos(ticker):
                """
                Coleta o histórico de dividendos de um ativo e calcula o total de dividendos por ano.

                Parâmetros:
                ticker (str): O símbolo do ativo.

                Retorna:
                Series ou None: Uma série com o total de dividendos por ano. Retorna None se não houver dados de dividendos.
                """
                ativo = yf.Ticker(ticker)
                historico_dividendos = ativo.dividends.reset_index()

                if historico_dividendos.empty:
                    return None

                historico_dividendos["year"] = historico_dividendos["Date"].dt.year
                dividendos_por_ano = historico_dividendos.groupby("year")[
                    "Dividends"
                ].sum()

                return dividendos_por_ano

            def calcula_dividendos(dividendos_ano, anos=5):
                """
                Calcula o total e a média dos dividendos para um número específico de anos.

                Parâmetros:
                dividendos_ano (Series): Série com dividendos anuais, com o ano como índice.
                anos (int): Número de anos a serem considerados no cálculo. Padrão é 5 anos.

                Retorna:
                tuple: Um tuplo contendo:
                    - Total de dividendos acumulados nos anos considerados.
                    - Média anual de dividendos.
                    - Número de anos com dados disponíveis.
                """
                ano_atual = datetime.datetime.now().year
                ano_inicio = ano_atual - anos

                dividendos_filtrados = dividendos_ano[
                    (dividendos_ano.index >= ano_inicio)
                    & (dividendos_ano.index < ano_atual)
                ]
                anos_disponiveis = len(dividendos_filtrados)
                if anos_disponiveis == 0:
                    return 0, 0, 0
                total_dividendos = dividendos_filtrados.sum()
                media_dividendos = total_dividendos / anos_disponiveis
                return total_dividendos, media_dividendos, anos_disponiveis

            def modelo_gordon(dividendo, taxa_retorno=0.06, taxa_crescimento=0.005):
                """
                Calcula o preço justo de uma ação ou FII usando o modelo de Gordon.

                Parâmetros:
                dividendo (float): O valor do dividendo anual do ativo.
                taxa_retorno (float): A taxa de retorno esperada. Padrão é 0.06 (6%).
                taxa_crescimento (float): A taxa de crescimento dos dividendos esperada. Padrão é 0.005 (0.5%).

                Retorna:
                float: O preço justo do ativo com base no modelo de Gordon.
                """
                return dividendo / (taxa_retorno - taxa_crescimento)

            def modelo_bazin(dividendo, taxa_retorno=0.06):
                """
                Calcula o preço justo de uma ação ou FII usando o modelo de Bazin.

                Parâmetros:
                dividendo (float): O valor do dividendo anual do ativo.
                taxa_retorno (float): A taxa de retorno esperada. Padrão é 0.06 (6%).

                Retorna:
                float: O preço justo do ativo com base no modelo de Bazin.
                """
                return dividendo / taxa_retorno

            for ticker_info in tickers_info:
                ticker, tipo_ativo = ticker_info.split(";")
                dividendos = coleta_dividendos(ticker)
                if dividendos is not None:
                    total_dividendos, media_dividendos, anos_disponiveis = (
                        calcula_dividendos(dividendos, anos_solicitados)
                    )
                    ativo = yf.Ticker(ticker)
                    cotacao_atual = ativo.info.get("currentPrice", 0)
                    dy_div = ativo.info.get("dividendYield", 0) * cotacao_atual

                    gordon = modelo_gordon(
                        media_dividendos, taxa_retorno[0], taxa_crescimento
                    )
                    bazin = modelo_bazin(media_dividendos, taxa_retorno[1])

                    recomendacao_gordon = "🟢" if cotacao_atual < gordon else "🔴"
                    recomendacao_bazin = "🟢" if cotacao_atual < bazin else "🔴"
                    retorno = (
                        taxa_retorno[0] if tipo_ativo == "AÇÃO" else taxa_retorno[1]
                    )

                    dados_ativos.append(
                        {
                            "Data": f"{datetime.datetime.now()}",
                            "Ticker": ticker,
                            "Tipo": tipo_ativo,
                            "Preço Atual": f"R${cotacao_atual:.2f}",
                            "Preço Teto (Bazin)": f"R$ {bazin:.2f}{recomendacao_bazin}",
                            "Preço Teto (Gordon)": f"R$ {gordon:.2f}{recomendacao_gordon}",
                            "Margem Bazin": f"R${bazin - cotacao_atual:.2f}",
                            "Margem Gordon": f"R${gordon - cotacao_atual:.2f}",
                            "Taxa de Retorno": f"{retorno*100:.2f}%",
                            "Taxa de Crescimento": f"{taxa_crescimento * 100:.2f}%",
                            "Período Solicitado": anos_solicitados,
                            "Período Disponível": anos_disponiveis,
                            "Total Dividendos": f"R$ {total_dividendos:.2f}",
                            "Média Dividendos": f"R$ {media_dividendos:.2f}",
                            "Dividend Yield": f"R$ {dy_div:.2f}",
                        }
                    )

            return JsonResponse({"dados_ativos": dados_ativos}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método não permitido"}, status=405)
