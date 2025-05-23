# Projeto Interdisciplinar III - Sistemas de Informação ESPM

<p align="center">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

# Mercadinho - Sistema de Monitoramento do Comportamento do Consumidor

### 2025-01

## Integrantes
- [Alexandre Martinelli](https://github.com/alexandremartinelli11/)
- [Gabriel Cardoso Campos Rodrigues](https://github.com/gabrielccr-555)
- [Hugo Coscelli Ferraz](https://github.com/z-hugo-ferraz/)
- [Julia Akemi Mullis](https://github.com/akemi-m/)
- [Theo Camuri Gaspar](https://github.com/tigasparzin/)

## Descrição do Projeto

O Mercadinho busca proporcionar uma ferramenta de análise do comportamento do consumidor em pontos de venda que possuam freezers e geladeiras, através da coleta de dados de presença, contagem de pessoas, e abertura e fechamento de portas por sensores da Absolut Technologies e posterior exibição, por meio de visualizações em dashboards e modelagem 3D. 

## Funcionalidades

- Mapeamento 3D, com digital twin atualizado em tempo real;
- Geração e exportação de relatórios para Microsoft Excel;
- Exibição de dashboards com KPIs de tempo médio de avaliação de alternativas na decisão de compra, horários de maior fluxo de clientes, freezers mais visitados e cálculo do número médio de clientes na loja por período.

## Configuração do Projeto

Para executar, deve criar o arquivo `config.py` da seguinte forma:

```python
host = '0.0.0.0'
port = 3000
conexao_banco = 'mysql+mysqlconnector://usuario:senha@host/mercadinho'
url_api = 'https://iagen.espm.br/sensores/dados'
```

Todos os comandos abaixo assumem que o terminal esteja com o diretório atual na raiz do projeto.

## Criação e Ativação do venv

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```
.venv\Scripts\activate
python app.py
```

## Mais Informações

https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/

# Licença

Este projeto é licenciado sob a [MIT License](https://github.com/tech-espm/inter-3sem-2025-mercadinho/blob/main/LICENSE).

<p align="right">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo-si-512.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>
