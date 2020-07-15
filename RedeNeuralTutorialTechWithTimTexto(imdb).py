# -*- coding: utf-8 -*-
"""RedeNeuralTutorialTechWithTimTexto(imdb).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18-FINQrzR1eeEsD5lCn82Sod8SHRvIq5
"""

"""
as execuçoes desse arquivo fiz pelo google colab
devido ao baixo poder computacioinal

"""
import tensorflow as tf
from tensorflow import keras
import numpy as np

dataset = keras.datasets.imdb

index_das_palavras = dataset.get_word_index() #carrega os indices e itens do modelo

index_das_palavras = {k:(v+4) for k,v in index_das_palavras.items()} #Cria um dicionario com as palvras e seus indices chaves começando do indice 4

index_das_palavras["<PAD>"] = 0 #Usado para padronizar
index_das_palavras["<START>"] = 1 #
index_das_palavras["<UNK>"] = 2  # unknown
index_das_palavras["<UNUSED>"] = 3 #

palavras_dos_indexs = dict([(palavra,chave) for (chave,palavra) in index_das_palavras.items()]) #criando um dicionario  que usa como chave as palavras e os indices como valores
"""
index_das_palavras = utilizando como chave a palavra acessa o codigo correspondente
palavras_dos_index = utilizando como chave o codigo correspondente para acessar a palavra
"""

tamanho_padrao_de_entrada = 250 #tamanho para padronizar o que sera (tamanho do input) inserido na rede
(dados_para_treino, respostas_do_treino), (dados_para_teste, respostas_dos_testes) = dataset.load_data(num_words=10000)

dados_para_treino = keras.preprocessing.sequence.pad_sequences(dados_para_treino,value=index_das_palavras["<PAD>"],padding="post",maxlen=tamanho_padrao_de_entrada) #Padronizando tamanho dos dados
dados_para_teste = keras.preprocessing.sequence.pad_sequences(dados_para_teste,value=index_das_palavras["<PAD>"],padding="post",maxlen=tamanho_padrao_de_entrada) #Padronizando tamanho dos dados

def decode_review(text):
  """
      pega um texto codificado, e retorna uma string com as palavras correspondentes a cada codigo
  """
  return "".join([palavras_dos_indexs.get(i,"?")+" " for i in text])

def review_encode(linhas):
  """
  @param linhas: reccebe uma lista de strings
  @return: retorna uma lista de inteiros(codigos) tratados para passar para o modelo
  """
  texto = []
  for linha in linhas:
    texto.extend(linha.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"","").strip().split(" "))
  codificando = [1] #Indicie equivalente ao simbolo <start>
  for palavra in texto:
    if (palavra.lower() in index_das_palavras):
      codificando.append(index_das_palavras[palavra.lower()])
    else:
      codificando.append(2) #Desconhecido
  codificando = keras.preprocessing.sequence.pad_sequences([codificando], value=index_das_palavras["<PAD>"], padding="post", maxlen=250) # Padroniza o tamanho, se for grande corta e se for pequeno adiciona o numero de <pads> necessario
  return codificando

rede = keras.Sequential()

rede.add(keras.layers.Embedding(100000,16)) #Primeira camada ajuda a achar semelhanças entre palavras(ou frases?)/(pelo o que eu entendi)
rede.add(keras.layers.GlobalAveragePooling1D()) #Segunda camada reduz o numero de dimenções para facilitar o processo
rede.add(keras.layers.Dense(16,activation="relu")) #camada cheia(full conected)
rede.add(keras.layers.Dense(1,activation="sigmoid")) #Camada de saida

rede.summary()
rede.compile(optimizer="adam",loss="binary_crossentropy",metrics=["accuracy"])

x_validacao = dados_para_treino[:10000]
x_treino = dados_para_treino[10000:]

y_validacao = respostas_do_treino[:10000]
y_treino = respostas_do_treino[10000:]

treino_do_modelo = rede.fit(x_treino,y_treino,epochs=40,batch_size=512,validation_data=(x_validacao,y_validacao),verbose = 1)
resultados = rede.evaluate(dados_para_teste,respostas_dos_testes)
print(resultados)

rede.save("/content/drive/My Drive/Colab Notebooks/rede_imdb_classificacao.h5")

"""Proximas execuções podem ser feitas a partir desta celula."""

redeNeural = keras.models.load_model("/content/drive/My Drive/Colab Notebooks/rede_imdb_classificacao.h5")

with open("/content/drive/My Drive/Colab Notebooks/avaliacao_idbm_rei_leao.txt", encoding="utf-8") as f:
  avaliacao_codificada = review_encode(f.readlines())

predicao = redeNeural.predict(avaliacao_codificada)

print(predicao)
print(avaliacao_codificada)
print(decode_review(avaliacao_codificada[0]))