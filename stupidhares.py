#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 23:08:44 2019

@author: Matheritmo
"""
import PokerInit as pk
from collections import namedtuple
import numpy as np
import random
import time
import keras
from keras.models import load_model
from keras import Sequential
from keras.layers import Dense, Activation
import numpy as np
import tensorflow
import sys

dizval={2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J', 12:'Q' ,13:'K', 14:'A'}
dizsem = {1:'spades',2:'flower',3:'diamonds',4:'heart'}
action= namedtuple('act','move amount')


class game():
        
    def __init__(self,n):
        self.n=n
        self.events = ['preflop']
        self.table= pk.table(2)
    
    def initgame(self):
                
        for k in range(self.n):
            self.table.reset()
               
                                                          
            for event in self.events:
                if k==0:
                    print('\n ######\n first event \n #########')
                if k !=0:
                    
                    print('\n ##############\n other event \n ####################\n')
                #time.sleep(3)             
                playerhistory=[]
                for i in range(len(self.table.nplayer)):
                    if self.table.nplayer[i].position==0:                
                        playerhistory.append(i)                
                #print(event)
                movehistory=[]
                b=action(0,0)
                movehistory.append(b)
                movehistory.append(b)
                movehistory.append(b)
                        

                                           
    
                if event == 'preflop':
                    #print(event)
                    self.table.nplayer[playerhistory[0]].stack -= self.table.bigb
                    self.table.nplayer[int(not(playerhistory[0]))].stack -= self.table.smallb
                    self.table.pot = self.table.smallb + self.table.bigb
                    print('bigblind',self.table.bigb,' ')
                    print('smallblind',self.table.smallb)
                    i==True
                    while i==True:
                        #print(event)
                        print('pot ',self.table.pot)
                        print('is the turn of ',int(not(playerhistory[-1])))
                        print('movehistory',movehistory[-1])
                        g = pk.getactionpos(movehistory[-1].move,'preflop')
                        print(g,'is your possible move \n')
                        if int(not(playerhistory[-1]))==0: 
                            print(self.table.nplayer[int(not(playerhistory[-1]))].card1,self.table.nplayer[int(not(playerhistory[-1]))].card2)
                            while True:
                                d=input('your choice is ')
                                if int(d) in g:
                                    break
                                else:
                                    print('do the possible choice or program don`t run')
                                    print(int(not(playerhistory[-1])))
                                    
                                        

                            # 1 check , 2 call, 3 raise, 4 fold
    
                            if int(d) == 3:
                                #print(d)
                                
                                if movehistory[-1].move==0:
                                    if len(movehistory)==3:
                                        self.table.nplayer[int(not(playerhistory[-1]))].stack -= self.table.smallb
                                        self.table.pot += self.table.smallb
                                    while True:                                          
                                        x=input('amount ')
                                        if float(x) < 2*self.table.bigb:
                                            print('bet error raise minimium 2bigblind')
                                        if float(x) >= self.table.nplayer[int(not(playerhistory[-1]))].stack:
                                            if float(x) >= self.table.nplayer[int(playerhistory[-1])].stack:
                                                print('raise your all in')
                                                b= action(3,self.table.nplayer[int(playerhistory[-1])].stack)
                                                break
                                            else:
                                                print('raise all in')
                                                b= action(3,int(self.table.nplayer[int(not(playerhistory[-1]))].stack))                                
                                        else:
                                            b=action(3,int(x))
                                            break
                                            
                                else:
                                    while True:
                                        #print('here')
                                        x=input('amount ')
                                        if int(x)< 2*movehistory[-1].amount:
                                            print('bet error raise minimium 2*raise')
                                        else:   
                                            b=action(3,int(x))
                                            break
                            
                            
                            if int(d) !=3:                                                        
                                b=action(int(d),0)
                        
                        #agent init here
                        
                        if int(not(playerhistory[-1]))==1: #cousin of DeepTurtle --> stupidhares
                            # arbitrary test for now , later i adjust this
                            test=np.array([self.table.nplayer[1].position,self.table.nplayer[1].stack,self.table.nplayer[1].stack/self.table.bigb,8,0.05])
                            test=test.reshape((1,5))
                            model = load_model('stupid_model.h5') #load the model 
                            score = model.predict(test)
                            if len(g)==2:                                
                                if np.argmax(score)==0:
                                    mf=g[np.argmax(score)]
                                if np.argmax(score)==2:
                                    mf=g[np.argmax(score)-1]
                                if np.argmax(score)==1:
                                    mf=g[np.argmax(score)-1]
                                if np.argmax(score)==3:    
                                    mf=g[0]
                            if len(g)==3:
                                if np.argmax(score)==0 or np.argmax(score)==1:                                    
                                    mf=g[0]
                                if np.argmax(score)==3:
                                    mf=g[-1]
                                else:
                                    mf=g[1]
                        #agent finish here
                        #the amount of raise for now is choice randomly whit a gamma distribution(2-mean)
                            mos=mf
                            print(mos)
                            if mos == 3:
                                if movehistory[-1].move !=3:
                                    nc=np.random.gamma(2,2)
                                    nc +=2
                                    finraise=int(nc*self.table.bigb)
                                    if finraise >= self.table.nplayer[int(not(playerhistory[-1]))].stack:
                                        if finraise >= self.table.nplayer[int(playerhistory[-1])].stack:
                                            print('raise your all in')
                                            b= action(3,self.table.nplayer[int(playerhistory[-1])].stack)
                                            break
                                        else:
                                            print('raise all in')
                                            b= action(3,int(self.table.nplayer[int(not(playerhistory[-1]))].stack))
                                            break
                                    
                                    b=action(3,finraise)
                                    
                                if movehistory[-1].move ==3:
                                    
                                    #reraise
                                    nc=np.random.gamma(2,2)
                                    nc +=2                                    
                                    res=movehistory[-1].amount
                                    reisfin=int(nc * res)
                                    if reisfin >= (self.table.nplayer[1].stack):
                                        print('all in')
                                        b= action(3,self.table.nplayer[1].stack)                                        
                                    elif reisfin >= res + self.table.nplayer[0].stack:
                                        print('raise your all in')
                                        b= action(3,int(self.table.nplayer[0].stack + res))
                                        
                                    else:
                                        b=action(3,int(reisfin))
                                    
                                   
                            if mos !=3:
                                b=action(int(mos),0)
                                                        
                           
                            
                        #call
                        if b.move==2:
                            if movehistory[-1].move==0:                                                             

                                if len(movehistory)==4:
                                    
                                    
                                    playerhistory.append(int(not(playerhistory[-1]))) 
                                    
                                    diff=(movehistory[-1].amount-self.table.smallb)
                                    self.table.nplayer[int(not(playerhistory[-1]))].stack -= diff
                                    self.table.pot += diff
                                    movehistory.append(b)
                                    
                                else:                                    
                                    playerhistory.append(int(not(playerhistory[-1])))
                                    
                                    
                                    self.table.nplayer[int(not(playerhistory[-1]))].stack -= self.table.smallb
                                    self.table.pot += self.table.smallb
                                    movehistory.append(b)


                            else:
                                         
                                
                                diff=(movehistory[-1].amount)
                                
                                if diff >= self.table.nplayer[int(not(playerhistory[-1]))].stack:
                                    self.table.pot += self.table.nplayer[int(not(playerhistory[-1]))].stack
                                    self.table.nplayer[int(not(playerhistory[-1]))].stack = 0
                                    movehistory.append(b)
                                    playerhistory.append(int(not(playerhistory[-1])))

                                else:                                                                         
                                    self.table.nplayer[int(playerhistory[-1])].stack -= diff
                                    self.table.pot += diff
                                    playerhistory.append(int(not(playerhistory[-1])))
                                    movehistory.append(b)
                                    #print('HERE')
                        #check        
                        if b.move==1:
                            movehistory.append(b)
                            playerhistory.append(int(not(playerhistory[-1])))
                        
                        #raise
                        if b.move==3:
                            movehistory.append(b)
                            playerhistory.append(int(not(playerhistory[-1])))
                            self.table.pot += b.amount
                            self.table.nplayer[int(playerhistory[-1])].stack -=int(b.amount)
                        
                        #fold
                        if b.move==4:                            
                            self.table.nplayer[int(playerhistory[-1])].stack += self.table.pot
                            self.table.reset()
                            print(self.table.nplayer[0].card,'\n',self.table.nplayer[0].stack,'\n')
                            print(self.table.nplayer[1].card,'\n',self.table.nplayer[1].stack,'\n')                  
                            
                            break
                        if movehistory[-2].move==2 and movehistory[-1].move==1:
                            i=False
                            
                        if movehistory[-2].move==3 and movehistory[-1].move==2:
                            
                            i=False
                            
                #showdown  
                if i==False:
                    self.table.flop()
                    print('pot is ',self.table.pot)
                    win=self.table.winner()
                    print(self.table.tablecard,'\n')
                    if win[1]==11:
                        print('split')
                        t= self.table.pot/2
                        self.table.nplayer[0].stack += t
                        self.table.nplayer[1].stack += t   
                    else:                                                
                        h = win[1]
                        self.table.nplayer[int(h)].stack +=self.table.pot
                    for i in range(len(self.table.nplayer)):
                        if self.table.nplayer[i].stack<=0:
                            print(self.table.nplayer[0].card,'\n',self.table.nplayer[0].stack,'\n')
                            print(self.table.nplayer[1].card,'\n',self.table.nplayer[1].stack,'\n')
                            print('game finish')
                            time.sleep(3)
                            exit
                    
                       
                    print(self.table.nplayer[0].card,'\n',self.table.nplayer[0].stack,'\n')
                    print(self.table.nplayer[1].card,'\n',self.table.nplayer[1].stack,'\n')                  

                    
                    break
                    

    
    
    
    

