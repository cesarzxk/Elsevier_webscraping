## CEDERJ 2019 - MIQUÉIAS DERNIER E VINICIUS ZANOVELLI (ORIENTADOR ALTOBELLI DE BRITO)

COLETA DIRECIONADA DE DADOS DA _INTERNET_ ATRAVÉS DE MECANISMOS 
DE AUTOMAÇÃO (_WEB SCRAPING_) COM FOCO EM ASPECTOS DA COMPOSIÇÃO 
E DA FORMULAÇÃO DE MEDICAMENTOS

Este repositório contém uma implementação de _software_ para coleta 
direcionada e automatizada de dados da _internet_ e uma aplicação
desta implementação voltada para a pesquisa de aspectos específicos
da composição e da formulação de medicamentos.

<br />

## Como instalar (console)

Instale o pacote Python (e todas as dependências):

```console
pip install .\farmacia
```

<br />

## Como executar a aplicação (console)

Digte no console

```console
python farmacia {drugbank,merck,scopus} configfile [-h] [--tipo {csv,json}] [--saida SAIDA]
```

argumentos posicionais (obrigatórios):<br/>
  * **{drugbank,merck,scopus}**
  * **configfile**:         Arquivo de configuração formato json com as configurações específicas para cada site

argumentos opcionais:<br/>
  * **-h, --help**:         show this help message and exit
  * **--tipo {csv,json}**:  Tipo de saída *multiplo {csv, json}. Default = csv
  * **--saida SAIDA**:      Nome do arquivo que será gerado com os resultados. Default = $(nome do site).csv

Exemplos de uso:
```console
python farmacia drugbank entradas\drugbank.json
python farmacia drugbank entradas\drugbank.json --tipo=json
python farmacia drugbank entradas\drugbank.json --tipo=json --tipo=csv
python farmacia drugbank entradas\drugbank.json --saida=resultado-drugbank --tipo=json
```

<br />

