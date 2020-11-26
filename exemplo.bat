pip install .\farmacia
cls
echo Este teste retornará os artigos correspondentes as configuração padrão do arquivo JSON
python farmacia scopus entradas\scopus.json --saida="arquivo-de-saida" --tipo=csv
