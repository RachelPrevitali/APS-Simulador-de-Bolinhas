'''---Feito por Rachel Paulino Previtali---'''

import pygame
import math
from random import randint

with open("input.txt", "r") as f:
    TAM_X = int(f.readline().strip())
    TAM_Y = int(f.readline().strip())
    n_bolas = int(f.readline().strip())


cor_do_fundo = (6, 21, 46) 
tela = pygame.display.set_mode((TAM_X, TAM_Y))
clock = pygame.time.Clock()
run = True

class Bola:
    def __init__(self,raio,cor,posicao,veloc,massa):    #definindo as bolinhas
        self.raio = raio
        self.cor = cor
        self.posicao = posicao
        self.veloc = veloc
        self.massa = massa
    def atualizaPos(self):
        self.posicao[0] += self.veloc[0] 
        self.posicao[1] += self.veloc[1] 
    def colideParede(self):
        if self.posicao[0]+self.raio >= TAM_X or self.posicao[0]-self.raio <= 0:
            self.veloc[0] *= -1
        if self.posicao[1]+self.raio >= TAM_Y or self.posicao[1]-self.raio <= 0:
            self.veloc[1] *= -1
    def colideBolas(self,other): #tratando as colisões como unidimensionais

        dist = math.sqrt((self.posicao[0]-other.posicao[0])**2 + (self.posicao[1]-other.posicao[1])**2)
        if dist <= (self.raio+other.raio):
            self.cor = (154, 186, 245)
            other.cor = (154, 186, 245)

            veloc_aux1 = self.veloc[0] #guarda a velocidade inicial de uma das bolinhas, antes de mudar
            veloc_aux2 = self.veloc[1]

            self.veloc[0]=((self.massa-other.massa)/(self.massa+other.massa))*self.veloc[0] + ((2*other.massa)/(self.massa+other.massa))*other.veloc[0]
            self.veloc[1]=((self.massa-other.massa)/(self.massa+other.massa))*self.veloc[1] + ((2*other.massa)/(self.massa+other.massa))*other.veloc[1]

            other.veloc[0]=((2*self.massa)/(self.massa+other.massa))*veloc_aux1 + ((other.massa-self.massa)/(self.massa+other.massa))*other.veloc[0]
            other.veloc[1]=((2*self.massa)/(self.massa+other.massa))*veloc_aux2 + ((other.massa-self.massa)/(self.massa+other.massa))*other.veloc[1]
            
    def descolaBolas (self,other):

        dist_centros = math.sqrt((self.posicao[0]-other.posicao[0])**2 + (self.posicao[1]-other.posicao[1])**2)

        if dist_centros <= (self.raio+other.raio):
        
            dx = self.posicao[0]-other.posicao[0]
            dy = self.posicao[1]-other.posicao[1]

            erro = (self.raio+other.raio) - dist_centros

            erro_x = (dx*erro)/dist_centros
            erro_y = (dy*erro)/dist_centros

            self.posicao[0]+=(erro_x)/2
            self.posicao[1]+=(erro_y)/2

            other.posicao[0]-=(erro_x)/2
            other.posicao[1]-=(erro_y)/2
    
    def descolaParede(self):
        if self.posicao[0]-self.raio < 0:

            dist = self.raio-self.posicao[0]
            self.posicao[0] += dist

        elif self.posicao[0]+self.raio > TAM_X:

            dist = self.raio-(TAM_X-self.posicao[0])
            self.posicao[0] -= dist



        if self.posicao[1]-self.raio < 0:

            dist = self.raio-self.posicao[1]
            self.posicao[1] += dist
            

        elif self.posicao[1]+self.raio > TAM_Y:

            dist = self.raio-(TAM_Y-self.posicao[1])
            self.posicao[1] -= dist



bolas = []

for i in range (n_bolas): #loop para criar as bolinhas
    bola = Bola(randint(20,40), (0,0,0), [randint(0,TAM_X), randint (0,TAM_Y)], [randint(-10,10),randint(-10,10)], randint(10,50)) 
    bolas.append(bola) #põe a bolinha criada em uma posição do vetor

while run:
    clock.tick(25)

    for event in pygame.event.get(): #vê se fechou a janela
        if event.type == pygame.QUIT:
            run = False
    
    tela.fill(cor_do_fundo)

    for b in bolas: #a cada iteração do loop eh feito tudo para uma bolinha, e vai fazendo para todas as outras da lista
        b.atualizaPos()
        b.colideParede()
        b.descolaParede()

        for o in list(bolas[0 : bolas.index(b)]): 
            b.colideBolas(o)                        #compara a bolinha que estamos analisando (no loop externo) com todas as outras!
            b.descolaBolas(o)


        pygame.draw.circle(tela, b.cor, (b.posicao[0], b.posicao[1]), b.raio)

        b.cor = (62, 127, 247)

    pygame.display.update()

pygame.quit()
