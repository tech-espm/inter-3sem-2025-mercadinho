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

## Motivação do Projeto

A tomada de decisão baseada em dados transforma negócios e torna as estratégias mais assertivas. Em um mercado altamente competitivo, onde há um grande volume de dados, é essencial extrair o máximo de valor dessas informações para identificar tendências e obter vantagem competitiva. Um exemplo claro desse cenário é o varejo de bens de consumo, como apontam Arbache et al. (2011), este mercado vem enfrentando diversos desafios, pois o consumidor está cada vez mais difícil de ser conquistado e as empresas precisam lutar, dia a dia, pela sua participação no mercado.

Na era digital, o e-commerce disponibiliza uma grande abundância de dados que facilitam a tomada de decisões estratégicas. No entanto, isso não significa que dados do varejo físico possam ser ignorados. Afinal, em termos de movimentação e impacto das vendas da economia, o varejo restrito movimentou R$ 1,99 trilhão em 2021, o que equivale a 22,9% do PIB brasileiro (SBVC, 2022).

No contexto de mercados que ainda dependem de lojas físicas, existem informações e insights que não podem ser coletados e obtidos apenas em um ambiente digital, como o comportamento do consumidor em pontos de venda, as suas respectivas interações com o produto à mostra e outros fatores que podem influenciar no processo de compra. Enquanto as ações de marketing podem ser medidas pelo valor de mercado da marca, pelo número de canais de distribuição e pela quantidade de consumidores do produto; e, as ações de vendas podem ser mensuradas pela quantidade efetiva de produtos comercializados e pela fatia do mercado que a marca detém; as ações do trade marketing não possuem métricas tão claras, pois se baseiam em atividades de relacionamento com distribuidores, pontos de venda e clientes (LONGARAY et al., 2016).

Sendo assim, este projeto visa suprir a falta de visibilidade analítica e quantitativa do comportamento do consumidor no mercado de varejo. Será feita uma análise comportamental do consumidor com a finalidade de otimizar o uso e disposição dos pontos de venda e auxiliar na tomada de decisão estratégica de trade marketing.

### Referências Bibliográficas

LONGARAY, A. A.; ENSSLIN, L.; ENSSLIN, S.; DUTRA, A.; MUNHOZ, P. R. da S.  
**Modelo multicritério de apoio à decisão construtivista para avaliação de desempenho do trade marketing**: um caso ilustrado no setor farmacêutico. *Revista Produção Online*, [S. l.], v. 16, n. 1, p. 49–76, 2016.  
DOI: [10.14488/1676-1901.v16i1.1885](https://doi.org/10.14488/1676-1901.v16i1.1885).  
Disponível em: <https://www.producaoonline.org.br/rpo/article/view/1885>. Acesso em: 7 mar. 2025.

SOCIEDADE BRASILEIRA DE VAREJO E CONSUMO (SBVC).  
**O papel do varejo na economia brasileira**. Edição 2022. [S. l.]: SBVC, 2022.  
Disponível em: <https://sbvc.com.br/o-papel-do-varejo-na-economia-brasileira-atualizacao-2022-sbvc/>. Acesso em: 7 mar. 2025.

ARBACHE, F. S.; SANTOS, A. G.; MONTENEGRO, C.; SALLES, W. F.  
**Gestão de logística, distribuição e trade marketing**. São Paulo: FGV, 2011.

## Objetivo do Projeto

O Mercadinho busca proporcionar uma ferramenta de análise do comportamento do consumidor em pontos de venda que possuam freezers e geladeiras, através da coleta de dados de presença, contagem de pessoas, e abertura e fechamento de portas por sensores da Absolut Technologies e posterior exibição, por meio de visualização em dashboard e modelagem 3D do espaço.

## Funcionalidades

- Digital twin do estabelecimento;
- Geração e exportação de relatórios em formato xlsx e csv;
- Dashboard contendo: 
    - KPIs de tempo médio de avaliação de alternativas na decisão de compra e total de visitantes no estabelecimento por janela de tempo selecionada;
    - Heatmap comunicando o total de visitantes por dia;
    - Gráfico de linhas exibindo a entrada e a saída dos clientes por hora;
    - Gráfico de barras contendo o número de visitas aos freezers das marcas.

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
