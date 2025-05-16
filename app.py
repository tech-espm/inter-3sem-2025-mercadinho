from flask import Flask, render_template, json, request, Response
import config
import requests
from datetime import datetime, timedelta
# nessa linha de baixo
import banco

app = Flask(__name__)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/heatmap')
def heatmap():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/heatmap.html', hoje=hoje)

@app.get('/heatmap2')
def heatmap2():
    semana_passada = (datetime.today() + timedelta(days=-6)).strftime('%Y-%m-%d')
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/heatmap2.html', semana_passada=semana_passada, hoje=hoje)


@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/getPassagem')
def getPassagem():

    dataInicial = request.args["dataInicial"]
    dataFinal = request.args["dataFinal"]
    dados = banco.listarDados(dataInicial, dataFinal)

    return json.jsonify(dados)

@app.get('/obterDados')
def obterDados():
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

@app.get('/obterDadosPassagem')
def obterDadosPassagem():
    # Obter o maior id do banco
    """
	maior_id = banco.obterIdMaximo("Id_RegF", "SensorPassagem")

    resultado = requests.get(f'{config.url_api}?sensor=passage&id_inferior={maior_id}')
    dados_novos = resultado.json()

	# Inserir os dados novos no banco
    if dados_novos and len(dados_novos) > 0:
        banco.inserirPassagem(dados_novos)

    dataInicial = request.args["dataInicial"]
    dataFinal = request.args["dataFinal"]
    dados = banco.listarPassagemMensal(dataInicial, dataFinal)"""
    dados = [{
        "dia": "14/05/2025",
        "total_entrada": 10,
	},{
        "dia": "15/05/2025",
        "total_entrada": 20,
	},{
        "dia": "16/05/2025",
        "total_entrada": 30,
	}]
    return json.jsonify(dados)

@app.post('/criar')
def criar():
    dados = request.json
    print(dados['id'])
    print(dados['nome'])
    return Response(status=204)

@app.get('/digitalTwin')
def digitalTwin():
    return render_template('index/digitalTwin.html', titulo='digitalTwin')

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
