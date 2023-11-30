import os
import re
import unicodedata
from collections import Counter
import csv

arquivos_sujos = 'arquivos_sujos'
arquivos_limpos = 'arquivos_limpos'
formato_arquivo_saida = '.csv'

def remover_acentos_e_caracteres_especiais(texto):
    # Normaliza a string para a forma NFD (Normalization Form Decomposition)
    texto = unicodedata.normalize('NFD', texto)
    # Remove caracteres diacríticos (marcas de acentuação)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    # Remove caracteres especiais, mantendo apenas letras e espaços
    texto = re.sub(r'[^\w\s]', '', texto)
    # Remove todos os números
    texto = re.sub(r'\d+', '', texto)
    # Converte a string para minúsculas
    texto = texto.lower()
    return texto

if not os.path.exists(arquivos_limpos):
    os.makedirs(arquivos_limpos)

arquivos = [arq for arq in os.listdir(arquivos_sujos)]

for indice, arquivo in enumerate(arquivos, start=1):
    nome_arquivo, extensao_arquivo = os.path.splitext(arquivo)
    arquivo_docx = nome_arquivo+formato_arquivo_saida

    caminho_completo_docx = os.path.join(arquivos_limpos, arquivo_docx)

    if os.path.isfile(caminho_completo_docx):
        print('O arquivo de numero '+str(indice)+' '+nome_arquivo+formato_arquivo_saida+' já foi limpo\n')
    else:
        if nome_arquivo != '.gitignore':
            print('Limpando arquivo '+nome_arquivo+extensao_arquivo + '\n')

            conteudo_arquivo = open(os.path.join(arquivos_sujos, arquivo), 'r', encoding='utf-8').read()

            output = remover_acentos_e_caracteres_especiais(conteudo_arquivo)

            file = open(arquivos_limpos+'/'+nome_arquivo+formato_arquivo_saida, "w")
            file.write(output)
             
            file.close()

            # Contador para as palavras
            contador_palavras = Counter()

            # Abre o arquivo CSV
            with open(caminho_completo_docx, 'r', encoding='utf-8') as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv)
                
                for linha in leitor_csv:
                    # Verifica se a linha tem o número esperado de colunas
                    if len(linha) > 0:
                        frase = remover_acentos_e_caracteres_especiais(linha[0])
                        palavras = re.findall(r'\b\w+\b', frase)
                        contador_palavras.update(palavras)

            # Salvar os resultados em um arquivo CSV
            with open(arquivos_limpos+'/'+nome_arquivo+'-nuvem'+formato_arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv)
                # Escreve o cabeçalho
                escritor_csv.writerow(['palavra', 'total'])

                # Escreve as palavras e suas contagens
                for palavra, contagem in contador_palavras.items():
                    escritor_csv.writerow([palavra, contagem])
