'''
Rotina para estratégia de busca de geolocalização do sensor SEARCH1
Programa de Autoria de Henrique Guimarães Coutinho. Domínio público.
Última atualização: 09/09/2021.
Como citar: endereço github.

'''

import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import math as m
import tqdm as tq


#--criar as entradas específicas--#
#variáveis
temp = 31.592 #(ºC)
vel_som = 331 * m.sqrt(1+(temp/273)) #(m/s)

#diferenças de tempo de chegada captadas (TDoA)
t12 = 11 #(ms)
t13 = -1 #(ms)
t14 = 3 #(ms)
t23 = -12 #(ms)
t24 = -8 #(ms)
t34 = -4 #(ms)


#coordenadas dos sensores envolvidos#
beacon_x1 = 0.20
beacon_y1 = 0.55

beacon_x2 = 2.75
beacon_y2 = 3.00

beacon_x3 = 2.40
beacon_y3 = 9.00

beacon_x4 = 0.10
beacon_y4 = 9.75

#iniciando coordenadas do emissor de som reais
target_x_real = 1.45
target_y_real = 5.45

#iniciando coordenadas do emissor de som pro search
target_x = 0.00
target_y = 0.00

#criar geometria - tamanho dos eixos (metros)
axis_1 = [0, 2.9, 0 , 10.93]

#declarando a variável do erro array
ERarr = []


#--mexendo com as distâncias, onde a mágica ocorre--#

#equação TDOA ===> c * Δt1,2 = Δd1,2 = √((target_x - beacon_x2)^2 + (target_y - beacon_y2)^2) - √((target_x - beacon_x1)^2 + (target_y - beacon_y1)^2)

x_temp = 0 #declarando as variáveis temporárias 
y_temp = 0
x_disc = 0.01 #declarando o valor da discretização de pontos 
y_disc = 0.01
x_lim = axis_1[1] #limite dos valores (definidos pelo tamanho do axis)
y_lim = axis_1[3]

#declarando x e y arr
xarr = []
yarr = []

#declarando tabs array
tabs = []

while(x_temp <= x_lim and y_temp <= y_lim):
    target_x = x_temp
    target_y = y_temp
    d12 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) 
    d13 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) 
    d14 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
    d23 = m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) - m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) 
    d24 = m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
    d34 = m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
    t12temp = (d12/vel_som)*1000 #(ms)
    t13temp = (d13/vel_som)*1000 #(ms)
    t14temp = (d14/vel_som)*1000 #(ms)
    t23temp = (d23/vel_som)*1000 #(ms)
    t24temp = (d24/vel_som)*1000 #(ms)
    t34temp = (d34/vel_som)*1000 #(ms)

    xarr.append(x_temp)
    yarr.append(y_temp)
    #print(x_temp, y_temp)

    x_temp = x_temp + x_disc
    if (x_temp>x_lim):
        x_temp = 0
        y_temp = y_temp + y_disc
  
    
    #descobrir como salvar os erros dos tempos associados com as posições para posterior plot     

    tabs.append(abs(t12temp - t12))
    tabs.append(abs(t13temp - t13))
    tabs.append(abs(t14temp - t14))
    tabs.append(abs(t23temp - t23))
    tabs.append(abs(t24temp - t24))
    tabs.append(abs(t34temp - t34))
    ERarr.append(np.sum(tabs))
    #print(len(tabs))
    tabs.clear()
        
#procurando a posição do menor valor
minimum = min(ERarr)
posmenor = ERarr.index(minimum)

#print(xarr)
#print(yarr)
#print(ERarr)
#print(minimum)
#print(posmenor)
target_x = xarr[posmenor]
target_y = yarr[posmenor]
print('O emissor está em:', sep = ' ')
print(target_x, target_y)

#criando o gráfico - grid e títulos
plt.grid()
plt.xlabel('Superfície x (metros)')
plt.ylabel('Superfície y (metros)')
plt.title('Mapeamento da Superfície de Teste - Resultado 2')

#plotando os pontos que representam os sensores - vermelho
plt.plot(beacon_x1,beacon_y1, 'ro')
plt.plot(beacon_x2, beacon_y2, 'ro')
plt.plot(beacon_x3,beacon_y3, 'ro')
plt.plot(beacon_x4, beacon_y4, 'ro')


#plotando o ponto do target com menor erro - azul
plt.plot(target_x, target_y, 'go')

#plotando o ponto do target real - azul
plt.plot(target_x_real, target_y_real, 'bo')

#escrevendo as legendas nos pontos 
names = ['1', '2', '3', '4', 'Emissor (Encontrado)', 'Emissor (Real)']
plt.text(beacon_x1 + 0.1, beacon_y1 + 0.10, names[0], fontsize = 8)
plt.text(beacon_x2 + 0.1, beacon_y2 + 0.10, names[1], fontsize = 8)
plt.text(beacon_x3 - 0.1, beacon_y3 + 0.20, names[2], fontsize = 8)
plt.text(beacon_x4 + 0.1, beacon_y4 + 0.10, names[3], fontsize = 8)
plt.text(target_x + 0.2, target_y + 0.0, names[4], fontsize = 8)
plt.text(target_x_real + 0.2, target_y_real - 0.20, names[5], fontsize = 8)

#definindo os eixos e mostrando o gráfico
plt.axis(axis_1)
plt.gca().set_aspect(1)
plt.show()