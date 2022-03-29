# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:56:51 2021

@author: grego
"""

import random
import math
from math import pi
import xlrd
import time


#temperature=xlrd.open_workbook('temperature_sample_calibrate2.xls')
temperature=xlrd.open_workbook('temperature_sample.xls')
file=temperature.sheets()
Pop=[]
Fitness =[]
Taille = 200

class individu:
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c        
    def Affichage(self):
        print("le meilleur triplet est (",self.a,",",self.b,",",self.c,")") 
def t(i,individu): #fonction de Weierstrass
    ti=0
    a=individu.a
    b=individu.b
    c=individu.c
    for n in range (0,c+1):
        ti+=(a**n)*math.cos((b**n)*pi*i) 
    return ti
def populationInitial():
    for i in range(Taille):
        a = round(random.uniform(0,0.999),2)
        b = random.randint(1,20)
        c = random.randint(1,20)
        triplet=individu(a,b,c)
        Pop.append(triplet)        
def croisement():
    for i in range(Taille):
        i1 = random.randint(0,Taille-1)
        i2 = random.randint(0,Taille-1)
        while i1==i2: 
            i1 = random.randint(0,Taille-1)    #cette partie sert juste à être sûr de ne pas croiser le même individu      
            i2 = random.randint(0,Taille-1)
        fils1=individu(Pop[i1].a,Pop[i2].b,Pop[i1].c)
        fils2=individu(Pop[i1].a,Pop[i1].b,Pop[i2].c)
        fils3=individu(Pop[i1].a,Pop[i2].b,Pop[i2].c)
        fils4=individu(Pop[i2].a,Pop[i1].b,Pop[i1].c)
        fils5=individu(Pop[i2].a,Pop[i1].b,Pop[i2].c)
        fils6=individu(Pop[i2].a,Pop[i2].b,Pop[i1].c)
        Pop.append(fils1)
        Pop.append(fils2)
        Pop.append(fils3)
        Pop.append(fils4)
        Pop.append(fils5)
        Pop.append(fils6)        
def mutation():
    for i in range(Taille):
        i1 = random.randint(0,len(Pop)-1)
        i2 = random.randint(0,2)        #sert à choisir quel paramètre on va substituer
        if i2==0:
            new_individu=individu(random.uniform(0,0.99),Pop[i2].b,Pop[i1].c)
        elif i2==1:
            new_individu=individu(Pop[i1].a,random.randint(1,20),Pop[i1].c)
        else:
            new_individu=individu(Pop[i1].a,Pop[i1].b,random.randint(1,20))
    Pop.append(new_individu)                 
def evaluer():
    Fitness.clear() #je nettoie toute ma liste de Fitness pour pouvoir la mettre à jour plus facilement
    for i in range(len(Pop)):
        cout=0
        for j in range(1,len(file[0].col(0))):
            cout += abs(t(float(file[0].col(0)[j].value),individu(Pop[i].a,Pop[i].b,Pop[i].c))-float(file[0].col(1)[j].value))   
        Fitness.append(cout)        
def selection():    #méthode de trie vu en module de langage python
    n=len(Fitness)
    for i in range(n):
        for j in range(0,n-i-1):
            if Fitness[j]>Fitness[j+1]:
                Pop[j],Pop[j+1]=Pop[j+1],Pop[j]                
                Fitness[j],Fitness[j+1]=Fitness[j+1],Fitness[j]                  
def AlgoG(nb): #nb=nombre de génération
    populationInitial()
    start_time = time.time()
    Time=[]         #permet d'enregistrer les temps de chaque génération pour trouver le meilleur individu
    estimation=[]   #va servir pour compter le nombre de génération nécessaire pour trouver une solution stable
    for i in range(nb):
        croisement()
        mutation()
        evaluer()
        selection()
        while len(Pop)>Taille:
            del Pop[-1]
            del Fitness[-1]
        print(min(Fitness))
        Pop[Fitness.index(min(Fitness))].Affichage()
        estimation.append(Pop[Fitness.index(min(Fitness))])
        Time.append(time.time()-start_time)
    compteur=0    
    for j in range(len(estimation)):
        if estimation[j]==Pop[Fitness.index(min(Fitness))]:
            compteur+=1
    generations=nb-compteur+1
    interval=Time[generations]
    interval_total = time.time() - start_time
    print("l'algorithme a convergé vers le triplet suivant :")
    Pop[Fitness.index(min(Fitness))].Affichage()
    print("en : ", generations,"générations et : ",interval," secondes")
    print("temps d'exécution totale",interval_total,"secondes")
        
       
if __name__=="__main__":
    
    AlgoG(15)