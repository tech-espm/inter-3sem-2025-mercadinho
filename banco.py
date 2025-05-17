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

def listarPessoas():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, nome, email) in pessoas:
			print(f'\nid: {id} / nome: {nome} / email: {email}')

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def obterPessoa(id):
	with Session(engine) as sessao:
		parametros = {
			'id': id
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

		if pessoa == None:
			print('Pessoa não encontrada!')
		else:
			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def criarPessoa(nome, email):
	# É importante utilizar o método begin() para que a sessão seja comitada
	# automaticamente ao final, caso não ocorra uma exceção!
	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
	# e nenhuma alteração será persistida. Para mais informações de como explicitar
	# esse processo de commit() e rollback():
	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
	with Session(engine) as sessao, sessao.begin():
		pessoa = {
			'nome': nome,
			'email': email
		}

		sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), pessoa)

		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
		# é passar uma lista como segundo parâmetro:
		# lista = [ ... ]
		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html

def getPassagem(data):
	with Session(engine) as sessao, sessao.begin(): #"2025-02%" = formato da data pra mes
		sessao.execute(text("Select day(Dt_Senf) ,sum(En_SenF) From SensorPassagem where Dt_SenF like data group by day(Dt_SenF)"), data)

def obterIdMaximo(id, tabela):
	with Session(engine) as sessao:
		registro = sessao.execute(text(f"SELECT MAX({id}) FROM {tabela}")).first()

		if registro == None or registro[0] == None:
			return 0
		else:
			return registro[0]

def inserirPassagem(registros):
	with Session(engine) as sessao, sessao.begin():
		for registro in registros:
			sessao.execute(text("INSERT INTO SensorPassagem (Id_RegF, Dt_SenF, Id_SenF, En_SenF, Sd_SenF, Id_Loja) VALUES (:id, :data, :id_sensor, :entrada, :saida, 1)"), registro)

def inserirContato(registros):
	with Session(engine) as sessao, sessao.begin():
		for registro in registros:
			sessao.execute(text(f"INSERT INTO SensorContato (Id_RegC, Dt_SenC, Id_SenC, Tm_SenC, Ab_SenC, Id_Gelad) VALUES (:id, :data, :id_sensor, :delta, :fechado, 3)"), registro)

def inserirPresenca(registros):
	with Session(engine) as sessao, sessao.begin():
		for registro in registros:
			if registro["id_sensor"] < 4:
				sessao.execute(text("INSERT INTO SensorPresenca (Id_RegP, Dt_SenP, Tm_SenP, Oc_Sens, Id_SenP, Id_Gelad) VALUES (:id, :data, :delta, :ocupado, :id_sensor, :id_sensor)"), registro)

def listarPassagemMensal(data_inicial, data_final):
	with Session(engine) as sessao:
		parametros = {
			'data_inicial': data_inicial + ' 00:00:00',
			'data_final': data_final + ' 23:59:59'
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		registros = sessao.execute(text("""
		Select date_format(dia, '%d/%m/%Y') as dia, visitantes as total_entrada, weekday(dia) as diaSmn
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
