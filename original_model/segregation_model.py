#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:27:30 2024

@author: odeviron
"""
from numpy import *
from numpy.random import *
from matplotlib.pyplot import *
from matplotlib.colors import ListedColormap
N=30
K=3
p=0.15
colors = cm.tab20(np.linspace(0, 1, K - 1))  # K-1 couleurs distinctes
colors = vstack([[1, 1, 1, 1], colors])       # Ajouter blanc comme première couleur (RGBA)

# Créer une colormap discrète
cmap = ListedColormap(colors, name="custom_colormap")
pp=0.25
X=choice(arange(K),(N,N),p=[pp]+list(ones(K-1)/(K-1)*(1-pp)))
print(count_nonzero(X==1),count_nonzero(X==2))  
Xh=zeros((N+2,N+2))
Xh[1:N+1,1:N+1]=X
I=[-1,0,1,-1,1,-1,0,1]
J=[-1,-1,-1,0,0,1,1,1]
jjj=0
Np=zeros(10)
zz=0
n=1
while(len(Np)>0)&(jjj<100):
    print(n,zz)
    if n==zz:
        jjj+=100
    else:
        zz=n
    Xv=zeros((N,N,8))
    k=0
    for i,j in zip(I,J):
            Xv[:,:,k]=Xh[1+i:N+1+i,1+j:N+1+j]
            k+=1
    N1 = count_nonzero((Xv != X[..., None])&(Xv !=0) , axis=2)
    N2=array(nonzero(X==0)).T
    Nb=nonzero((N1>p*8))
    Nb=[[Nb[0][i],Nb[1][i]] for i in range(len(Nb[0]))]
    shuffle(Nb)
    for i,j in Nb:
        nf=True
        c=X[i,j]
        ii=N2.shape[0]
        ik=0
        N2l=[N2[k,:] for k in range(N2.shape[0])]
        shuffle(N2l)
        ik=0
        while nf:
            k,l=N2l[ik]
            n=count_nonzero((Xv[k,l,:]!=0)&(Xv[k,l,:]!=c))
            if n<=p*8:
                tempo=X[k,l]
                X[k,l]=X[i,j]
                X[i,j]=tempo
                nf=False
            ik+=1
            if ik==len(N2l):
                ik=randint(len(N2l))
                k,l=N2l[ik]
                tempo=X[k,l]
                X[k,l]=X[i,j]
                X[i,j]=tempo
                nf=False
    Xh[1:N+1,1:N+1]=X     
    n=len(Nb)         
    pcolor(X,cmap=cmap)
    pause(0.1)
    jjj+=1