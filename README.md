## CEDERJ 2020.2 - CÉSAR VARGAS DOS SANTOS E DANIEL VARGAS DOS SANTOS

COLETA DIRECIONADA DE DADOS DA _INTERNET_ ATRAVÉS DE MECANISMOS 
DE AUTOMAÇÃO (_WEB SCRAPING_) COM FOCO EM ASPECTOS DA COMPOSIÇÃO 
E DA FORMULAÇÃO DE MEDICAMENTOS

Este repositório contém uma implementação de _software_ para coleta 
direcionada e automatizada de dados da _internet_ e uma aplicação
desta implementação voltada para a pesquisa de aspectos específicos
da composição e da formulação de medicamentos.

<br />
## Será gerado automáticamente um arquivo 'erros.json' contendo os dados coletados caso ocorra alguma excessão.

<br/>
## Como instalar (console)

Instale o pacote Python (e todas as dependências):

```console
pip install .\farmacia
```

<br />

## Como executar a aplicação (console)

Digte no console

```console
python farmacia scopus configfile [-h] [--tipo csv] [--saida SAIDA]
```
argumentos opcionais:<br/>
  * **-h, --help**:         show this help message and exit
  * **--saida SAIDA**:      Nome do arquivo que será gerado com os resultados. Default = $(nome do site).csv

Exemplos de uso:
```console
python farmacia scopus entradas\scopus.json --saida=resultado-scopus --tipo=csv
```
<br />

