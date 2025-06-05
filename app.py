from flask import Flask, render_template, json, request, Response, jsonify , make_response 
import config
import requests
from datetime import datetime, timedelta
import banco

# Endpoint que possibilita os verbos
app = Flask(__name__)

# Caminho para a home page
@app.get('/')
def index():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', mes_passado=mes_passado, hoje=hoje)

# Caminho para a página sobre nós
@app.get('/sobre-nos')
def sobre():
    return render_template('index/sobre-nos.html', titulo='Sobre Nós')

# Caminho para a página que tem o dashboard
@app.get('/dash')
def dash():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/dashboard.html', titulo='Dashboard', mes_passado=mes_passado, hoje=hoje)

# Caminho para a página do digital twin
@app.get('/digital-twin')
def digitalTwin():
    return render_template('index/digital-twin.html', titulo='Digital Twin')

@app.get('/relatorio')
def exportar():
    return render_template('index/relatorio.html', titulo='Relatório')

# Atualiza o banco de dados
@app.get('/atualizarBanco')
def atualizarBanco():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo('Id_RegF', 'SensorPassagem')

    resultado = requests.get(f'{config.url_api}?sensor=passage&id_inferior={maior_id}&id_sensor=2')
    passagem = resultado.json()

	# Inserir os dados `passagem` novos no banco
    if passagem and len(passagem) > 0:
        banco.inserirPassagem(passagem)
    
    maior_id = banco.obterIdMaximo('Id_RegC', 'SensorContato')

    resultado = requests.get(f'{config.url_api}?sensor=magnetic&id_inferior={maior_id}')
    contato = resultado.json() 

    # Inserir os dados `contato` novos no banco
    if contato and len(contato) > 0:
        banco.inserirContato(contato)
        
    maior_id = banco.obterIdMaximo('Id_RegP', 'SensorPresenca')

    resultado = requests.get(f'{config.url_api}?sensor=presence&id_inferior={maior_id}')
    presenca = resultado.json() 

    # Inserir os dados `presença` novos no banco
    if presenca and len(presenca) > 0:
        banco.inserirPresenca(presenca)
    
	# Trazer os dados do banco
    dados = [
        { 'dia': '10/09', 'valor': 80 },
        { 'dia': '11/09', 'valor': 92 },
        { 'dia': '12/09', 'valor': 90 },
        { 'dia': '13/09', 'valor': 101 },
        { 'dia': '14/09', 'valor': 105 },
        { 'dia': '15/09', 'valor': 100 },
        { 'dia': '16/09', 'valor': 64 },
        { 'dia': '17/09', 'valor': 78 },
        { 'dia': '18/09', 'valor': 93 },
        { 'dia': '19/09', 'valor': 110 }
    ]
    return json.jsonify(dados) 


# Função responsável por popular o heatmap
@app.get('/obterDadosHeatmap')
def obterDadosHeatmap():

    dataInicial = request.args["data_inicial"]
    dataFinal = request.args["data_final"]
    dados = banco.listarPassagemMensal(dataInicial, dataFinal)

    resposta = make_response(jsonify(dados))
    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

# Função para popular o gráfico de linha
@app.get('/obterFluxoHora')
def obterFluxoHora():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        dados = banco.obterFluxoPorHora(data_inicial, data_final)
    else:
        dados = banco.obterFluxoPorHora()

    resposta = make_response(dados)
    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

# Função para obter o tempo médio de decisão de compra
@app.get('/obterMediaDecisao')
def obterMedia():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        dados = banco.obterMediaDecisao(data_inicial,data_final)
    else:
        dados = banco.obterMediaDecisao()
        print(dados[0][0])

    resposta = make_response(jsonify(dados))
    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

# Função para popular o gráfico de barras
@app.get('/obterTaxaAtratividade')
def obterTaxaAtratividade():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        dados = banco.obterTaxaAtratividade(data_inicial, data_final)
    else:
        dados = banco.obterTaxaAtratividade()
    
    resposta = make_response(jsonify(dados))
    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

# Função para popular o KPI de clientes presentes na loja 
@app.get('/obterFluxoAtual')
def obterFluxo():
    dados = banco.obterFluxoAtual()

    resposta = make_response(jsonify(dados[0][0]))
    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta



# Função para verificar a existencia de cliente na frente da geladeira e se esta está aberta ou fechada
@app.get('/atualizaPinguin')
def atualizaPinguin():
    pinguin = banco.atualizarPinguins()

    resposta = make_response(jsonify(pinguin))
    if type(pinguin) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

@app.get('/teste')
def teste():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        taxaAtratividade = banco.obterTaxaAtratividade(data_inicial, data_final)
        mediaDecisao = banco.obterMediaDecisao(data_inicial,data_final)
        fluxoPorHora = banco.obterFluxoPorHora(data_inicial, data_final)
    else:
        taxaAtratividade = banco.obterTaxaAtratividade()
        mediaDecisao = banco.obterMediaDecisao(data_inicial,data_final)
        fluxoPorHora = banco.obterFluxoPorHora()

    resposta = make_response((jsonify(taxaAtratividade, mediaDecisao, fluxoPorHora)))
    if type((taxaAtratividade)) == str or type((mediaDecisao)) == str or type((fluxoPorHora)) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200    
    
    return resposta


if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
