# Vamos utilizar o pacote SQLAlchemy para acesso a banco de dados:
# https://docs.sqlalchemy.org
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install SQLAlchemy
#
# Além disso, o SQLAlchemy precisa de um driver do conexão ao banco. Isso depende do servidor
# (MySQL, Postgres, SQL Server, Oracle...) e do driver real. Vamos utilizar o driver MySQL-Connector,
# que também precisa ser instalado (de preferência com o VS Code fechado):
# python -m pip install mysql-connector-python
# tava dando erro aqui gente porque o python 13. não tem suporte oficial ainda para
# SQLAlchemy então tem q dar update nele 
# pip install --upgrade sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco


# Como criar uma comunicação com o banco de dados:
# https://docs.sqlalchemy.org/en/14/core/engines.html
#
# Detalhes específicos ao MySQL
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
#
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine(conexao_banco)

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

# def listarPessoas():
# 	# O with do Python é similar ao using do C#, ou o try with resources do Java.
# 	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
# 	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
# 	with Session(engine) as sessao:
# 		pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

# 		# Como cada registro retornado é uma tupla ordenada, é possível
# 		# utilizar a forma de enumeração de tuplas:
# 		for (id, nome, email) in pessoas:
# 			print(f'\nid: {id} / nome: {nome} / email: {email}')

# 		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
# 		# com outras linguagens de programação:
# 		#for pessoa in pessoas:
# 		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

# def obterPessoa(id):
# 	with Session(engine) as sessao:
# 		parametros = {
# 			'id': id
# 		}

# 		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
# 		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
# 		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
# 		pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

# 		if pessoa == None:
# 			print('Pessoa não encontrada!')
# 		else:
# 			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

# def criarPessoa(nome, email):
# 	# É importante utilizar o método begin() para que a sessão seja comitada
# 	# automaticamente ao final, caso não ocorra uma exceção!
# 	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
# 	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
# 	# e nenhuma alteração será persistida. Para mais informações de como explicitar
# 	# esse processo de commit() e rollback():
# 	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
# 	with Session(engine) as sessao, sessao.begin():
# 		pessoa = {
# 			'nome': nome,
# 			'email': email
# 		}

# 		sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), pessoa)

# 		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
# 		# é passar uma lista como segundo parâmetro:
# 		# lista = [ ... ]
# 		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html

# def getPassagem(data):
# 	with Session(engine) as sessao, sessao.begin(): #"2025-02%" = formato da data pra mes
# 		sessao.execute(text("Select day(Dt_Senf) ,sum(En_SenF) From SensorPassagem where Dt_SenF like data group by day(Dt_SenF)"), data)

# Função que atualiza o banco de dados com base no último dado inserido
def obterIdMaximo(id, tabela):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT MAX({id}) FROM {tabela}")).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

# Insere uma tabela de dados de passagem de clientes
def inserirPassagem(registros):
	try:
		with Session(engine) as sessao, sessao.begin():
			for registro in registros:
				sessao.execute(text("INSERT INTO SensorPassagem (Id_RegF, Dt_SenF, Id_SenF, En_SenF, Sd_SenF, Id_Loja) VALUES (:id, :data, :id_sensor, :entrada, :saida, 1)"), registro)
	except Exception as e:
		return str(e)
# Insere uma tabela de dados de contato da porta
def inserirContato(registros):
	try:
		with Session(engine) as sessao, sessao.begin():
			for registro in registros:
				sessao.execute(text(f"INSERT INTO SensorContato (Id_RegC, Dt_SenC, Id_SenC, Tm_SenC, Ab_SenC, Id_Gelad) VALUES (:id, :data, :id_sensor, :delta, :fechado, 3)"), registro)
	except Exception as e:
		return str(e)
# Insere uma tabela de dados de presença de clientes 
def inserirPresenca(registros):
	try:
		with Session(engine) as sessao, sessao.begin():
			for registro in registros:
				if registro["id_sensor"] < 4:
					sessao.execute(text("INSERT INTO SensorPresenca (Id_RegP, Dt_SenP, Tm_SenP, Oc_Sens, Id_SenP, Id_Gelad) VALUES (:id, :data, :delta, :ocupado, :id_sensor, :id_sensor)"), registro)
	except Exception as e:
		return str(e)
	
# Função que extrai os dados do banco para gerar o heatmap
def listarPassagemMensal(data_inicial, data_final):
	try:
		with Session(engine) as sessao:
			parametros = {
				'data_inicial': data_inicial + ' 00:00:00',
				'data_final': data_final + ' 23:59:59'
			}

			# Mais informações sobre o método execute e sobre o resultado que ele retorna:
			# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
			# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
			registros = sessao.execute(text("""
			Select date_format(dia, '%d/%m') as dia, visitantes as total_entrada, weekday(dia) as diaSmn
			from (Select concat(date_format(Dt_SenF, '%Y/%m/%d'), " 00:00:00") as dia ,sum(En_SenF) as visitantes
				from SensorPassagem 
				where Dt_SenF 
				between :data_inicial and :data_final 
				group by dia) as meioTermoPassagem
			"""), parametros)

			lista = []

			for (dia, total_entrada, diaSmn) in registros:
				lista.append({
					"dia": dia,
					"total_entrada": total_entrada,
					"diaSmn": diaSmn
				})

			return lista
	except Exception as e:
		return str(e)
	
# Função que extrai os dados do banco para gerar o gráfico de linhas
def obterFluxoPorHora(data_inicial=None, data_final=None):
		try:
			with Session(engine) as sessao:
				parametros = {}
				sql = "select date_format(Dt_SenF, '%H:00') as hora, sum(En_SenF) as total_entradas, sum(Sd_SenF) as total_saidas from SensorPassagem"

				if data_inicial and data_final:
					sql += " where Dt_SenF between :data_inicial and :data_final"
					parametros["data_inicial"] = data_inicial + " 00:00:00"
					parametros["data_final"] = data_final + " 23:59:59"

				sql += " group by hora order by hora"

				registros = sessao.execute(text(sql), parametros)
				resultado = []

				for hora, entradas, saidas in registros:
					resultado.append({
						"hora": hora,
						"entradas": entradas,
						"saidas": saidas
					})

				return resultado
		except Exception as e:
			return str(e)

# Função que extrai os dados do banco para obter o tempo médio de decisão de compra
def obterMediaDecisao(data_inicial=None, data_final=None):
	try:
		with Session(engine) as sessao:
			parametros = {}
			sql = "select avg(delta) from (select avg(Tm_SenP) as delta,  date_format(Dt_SenP, '%Y/%m/%d %H:%i') as Dia from sensorpresenca where date_format(Dt_SenP, '%Y/%m/%d %H:%i') in (select date_format(Dt_SenC, '%Y/%m/%d %H:%i') from sensorcontato "
			if data_inicial and data_final:
				sql += """where Ab_SenC = 1 and Dt_SenC between :data_inicial and :data_final )	group by date_format(Dt_SenP, '%Y/%m/%d %H:%i')) as n;"""
				parametros["data_inicial"] = data_inicial + " 00:00:00"
				parametros["data_final"] = data_final + " 23:59:59"
				print(parametros)
			
			else:
				sql += """where Ab_SenC = 1) group by date_format(Dt_SenP, '%Y/%m/%d %H:%i')) as n;"""
			
			registro = sessao.execute(text(sql), parametros)
			resultado = []

			for i in registro:
				resultado.append(i)

			return resultado[0][0] // 60
	except Exception as e:
		return str(e)
# Função que extrai os dados do banco para obter a taxa de atratividade 
def obterTaxaAtratividade(data_inicial=None, data_final=None):
	try:
		with Session(engine) as sessao:
			parametros = {}
			sql = "select Id_Gelad, count(*) as total_visitas from sensorpresenca where Oc_Sens = 1"
			if data_inicial and data_final:
				sql += " and Dt_SenP between :data_inicial and :data_final"
				parametros["data_inicial"] = data_inicial + " 00:00:00"
				parametros["data_final"] = data_final + " 23:59:59"
			
			sql += " group by Id_Gelad order by total_visitas desc"
			
			registro = sessao.execute(text(sql), parametros)

			
			resultado = []
			for Id_Gelad, total_visitas in registro:
				resultado.append({
					"Id_Gelad": Id_Gelad,
					"total_visitas": total_visitas
				})
				
			return resultado
			
	except Exception as e:
		return str(e)


# Função para devolver a quantidade de clientes na loja no momento
def obterFluxoAtual():
	try:
		with Session(engine) as sessao:
			fluxo_atual = sessao.execute(text("""
			SELECT SUM(En_SenF) - SUM(Sd_SenF) AS clientes
				FROM SensorPassagem
				WHERE date_format(Dt_SenF, '%Y/%d/%d') = date_format(current_date(), '%Y/%d/%d');
			"""))
		resultado=[]
		for i in fluxo_atual:
			resultado.append(i)
		return resultado
	except Exception as e:
		return str(e)

# Função para verificar a existencia de cliente na frente da geladeira e se esta está aberta ou fechada
def atualizarPinguins():
	try:
		with Session(engine) as sessao:
			p = sessao.execute(text("""select 
				(select c.Ab_SenC from sensorcontato c where c.Id_SenC = 3 order by c.Id_RegC desc limit 1) aberto,
				(select p.Oc_Sens from sensorpresenca p where p.Id_SenP = 3 order by p.Id_RegP desc limit 1) presente"""))

			pinguin = []

			for i in p:
				pinguin.append({
					"Aberto":i[0],
					"Presente": i[1]
						})
			
			return pinguin
	except Exception as e:
		return str(e)