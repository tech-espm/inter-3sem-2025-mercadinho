from flask import Flask, render_template, json, request, Response, jsonify
import config
import requests
from datetime import datetime, timedelta
import banco

# Endpoint que possibilita os verbos
app = Flask(__name__)

# Caminho para a home page
@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

# Caminho para a página contendo o heatmap
@app.get('/heatmap')
def heatmap():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/heatmap.html', mes_passado=mes_passado, hoje=hoje)

# Caminho para a página sobre nós
@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

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
    ];
    return json.jsonify(dados)

# Caminho para a página do digital twin
@app.get('/digitalTwin')
def digitalTwin():
    return render_template('index/digitalTwin.html', titulo='digitalTwin')

# Caminho para o gráfico de linha (Fluxo de passagem x Hora)
@app.get('/linha')
def linha():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/linha.html', titulo='Gráfico de Linha', mes_passado=mes_passado, hoje=hoje)

# Função responsável por popular o heatmap
@app.get('/obterDadosHeatmap')
def obterDadosHeatmap():
    # Obter o maior id do banco
    maior_id = banco.obterIdMaximo("Id_RegF", "SensorPassagem")
    
    resultado = requests.get(f'{config.url_api}?sensor=passage&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirPassagem(dados_novos)

    dataInicial = request.args["data_inicial"]
    dataFinal = request.args["data_final"]
    dados = banco.listarPassagemMensal(dataInicial, dataFinal)
    return json.jsonify(dados)

# Função para popular o gráfico de linha
@app.get('/obterFluxoHora')
def obterFluxoHora():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        dados = banco.obterFluxoPorHora(data_inicial, data_final)
    else:
        dados = banco.obterFluxoPorHora()

    return json.jsonify(dados)

# Caminho para a página que tem o tempo médio de decisão de compra
@app.get('/decisao')
def decisao():
    data_inicial = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    data_final = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/decisao.html', titulo='Grandes Numeros', data_inicial=data_inicial, data_final=data_final)

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

    return jsonify(dados[0][0] // 60)


# Caminho para o gráfico de barras
@app.get('/barras')
def barras():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/barras.html', titulo='Gráfico de Barras', mes_passado=mes_passado, hoje=hoje)

# Função para popular o gráfico de barras
@app.get('/obterTaxaAtratividade')
def obterTaxaAtratividade():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')

    if data_inicial and data_final:
        dados = banco.obterTaxaAtratividade(data_inicial, data_final)
    else:
        dados = banco.obterTaxaAtratividade()

    return json.jsonify(dados)

# Função para popular o KPI de clientes presentes na loja 
@app.get('/obterFluxoAtual')
def obterFluxo():
    clientestuais = banco.obterFluxoAtual()
    return json.jsonify(clientestuais[0][0])

# Caminho para a página que tem os clientes atuais na loja
@app.get('/atualClientes')
def atualClientes():
    return render_template('index/clientesAtuais.html', titulo='clientesAtuais')

# Caminho para a página que tem o dashboard
@app.get('/dash')
def dash():
    mes_passado = (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/dashboard.html', titulo='Dashboard', mes_passado=mes_passado, hoje=hoje)

# Função para verificar a existencia de cliente na frente da geladeira e se esta está aberta ou fechada
@app.get('/atualizaPinguin')
def atualizaPinguin():
    pinguin = banco.atualizalarPinguins()

    return json.jsonify(pinguin)


if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
