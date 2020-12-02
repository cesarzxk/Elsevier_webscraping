# CEDERJ 2020.2 - CÉSAR VARGAS DOS SANTOS E DANIEL VARGAS DOS SANTOS

Aplicação voltada a coleta de dados da _Internet_
através de mecanismo de automação (_Web Scraping_)
com foco em aspectos da composição e da formulação
de medicamentos.


## :rocket: Tecnologias

Este projeto foi desenvolvido com as seguintes tecnologias:

- Python
- Scrapy
- REST
- [VS Code]()

## :information_source: Como Instalar
Para clonar essa aplicação você precisará do [Git](https://git-scm.com) instalado em seu computador.

```bash
# Instalar as dependências
$ pip install requests

# Clonar o repositório
$ git clone https://github.com/altobellibm/CEDERJ_2020_DANIEL_VARGAS_CEZAR_SANTOS

# Instalar a aplicação
$ pip install ./farmacia

# Rodar a aplicação
$ python farmacia scopus configfile [-h] [--tipo csv] [--saida SAIDA]

# Exemplo
$ python farmacia scopus entradas\scopus.json --saida=resultado-scopus --tipo=csv

```
Argumentos opcionais:

* **[-h]** Mostra uma mensagem de ajuda e sai.
* **[--saida SAIDA]** --saida NOME_DO_ARQUIVO_DE_SAIDA  - Default $(nome do site).csv

Caso haja algum erro, será gerado automáticamente um arquivo 'erros.json' contendo os dados coletados.

## :memo: Licença
This project is under the MIT license. See the [LICENSE](https://github.com/lukemorales/react-native-design-code/blob/master/LICENSE) for more information.
