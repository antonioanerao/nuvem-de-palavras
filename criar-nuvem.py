from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

arquivo_nuvem = input('Nome do arquivo para gerar a nuvem de palavras: ')

nuvem = pd.read_csv(arquivo_nuvem, encoding = 'utf-8')

# vamos trocar os espaços dos nomes dos imunizantes
# por um underline, para as palavras aparecerem juntas
# essa parte não é obrigatória

# cria um dicionário com os dados, necessário para a word cloud
d = {}
for palavra, total in nuvem.values:
    d[palavra] = total

# inicializa uma word cloud
wordcloud = WordCloud()

# gera uma wordcloud através do dicionário de frequências
wordcloud.generate_from_frequencies(frequencies = d)

plt.figure(figsize = (15, 10)) # tamanho do gráfico
plt.imshow(wordcloud, interpolation = 'bilinear') # plotagem da nuvem de palavras
plt.axis('off') # remove as bordas
plt.show() # mostra a word cloud
