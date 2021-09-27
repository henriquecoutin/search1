'''
Rotina para gabarito da estratégia de busca de geolocalização do sensor SEARCH1
Programa de Autoria de Henrique Guimarães Coutinho. Domínio público.
Última atualização: 09/09/2021.
Como citar: endereço github.

'''

import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import math as m


#--criar as entradas específicas--#
#variáveis
temp = 31.592 #(ºC)
vel_som = 331 * m.sqrt(1+(temp/273)) #(m/s)

#diferenças de tempo de chegada captadas (TDoA)
t12 = 1 #(ms)
t13 = 2 #(ms)
t14 = 3 #(ms)
t23 = 5 #(ms)
t24 = 3 #(ms)
t34 = 2 #(ms)


#coordenadas dos sensores envolvidos#
beacon_x1 = 0.20
beacon_y1 = 0.55

beacon_x2 = 2.75
beacon_y2 = 3.00

beacon_x3 = 2.40
beacon_y3 = 9.00

beacon_x4 = 0.1
beacon_y4 = 9.75

#coordenadas do emissor de som
target_x = 1.45
target_y = 5.45


#criar geometria - tamanho dos eixos (metros)
axis_1 = [0, 2.9, 0 , 10.93]

#--mexendo com as distâncias, onde a mágica ocorre--#

#equação TDOA ===> c * Δt1,2 = Δd1,2 = √((target_x - beacon_x2)^2 + (target_y - beacon_y2)^2) - √((target_x - beacon_x1)^2 + (target_y - beacon_y1)^2)

'''obs: O'KEEFE estava errado! use a equação de LI, X., DENG., Z. (TOA e TDOA_2) '''
d12 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) 
d13 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) 
d14 = m.sqrt(m.pow(target_x - beacon_x1,2) + m.pow(target_y - beacon_y1,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
d23 = m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) - m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) 
d24 = m.sqrt(m.pow(target_x - beacon_x2,2) + m.pow(target_y - beacon_y2,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
d34 = m.sqrt(m.pow(target_x - beacon_x3,2) + m.pow(target_y - beacon_y3,2)) - m.sqrt(m.pow(target_x - beacon_x4,2) + m.pow(target_y - beacon_y4,2)) 
t12esp = (d12/vel_som)*1000 #(ms)
t13esp = (d13/vel_som)*1000 #(ms)
t14esp = (d14/vel_som)*1000 #(ms)
t23esp = (d23/vel_som)*1000 #(ms)
t24esp = (d24/vel_som)*1000 #(ms)
t34esp = (d34/vel_som)*1000 #(ms)

print("Tempo 1 -> 2 esperado:",t12esp)
print("Tempo 1 -> 3 esperado:",t13esp)
print("Tempo 1 -> 4 esperado:",t14esp)
print("Tempo 2 -> 3 esperado:",t23esp)
print("Tempo 2 -> 4 esperado:",t24esp)
print("Tempo 3 -> 4 esperado:",t34esp)


#criando o gráfico - grid e títulos
plt.grid()
plt.xlabel('Superfície x (metros)')
plt.ylabel('Superfície y (metros)')
plt.title('Mapeamento da Superfície de Teste')

#plotando os pontos que representam os sensores - vermelho
plt.plot(beacon_x1,beacon_y1, 'ro')
plt.plot(beacon_x2, beacon_y2, 'ro')
plt.plot(beacon_x3,beacon_y3, 'ro')
plt.plot(beacon_x4, beacon_y4, 'ro')


#plotando o ponto do target - azul
plt.plot(target_x, target_y, 'bo')

#escrevendo as legendas nos pontos 
names = ['1', '2', '3', '4', 'Emissor']
plt.text(beacon_x1 + 0.1, beacon_y1 + 0.1, names[0], fontsize = 8)
plt.text(beacon_x2 + 0.1, beacon_y2 + 0.1, names[1], fontsize = 8)
plt.text(beacon_x3 - 0.1, beacon_y3 + 0.2, names[2], fontsize = 8)
plt.text(beacon_x4 + 0.1, beacon_y4 + 0.1, names[3], fontsize = 8)
plt.text(target_x + 0.1, target_y + 0.1, names[4], fontsize = 10)

#definindo os eixos e mostrando o gráfico
plt.axis(axis_1)
plt.gca().set_aspect(1)
plt.show()
