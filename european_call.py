#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 14:46:38 2020

@author: Selo
"""
from math import log, sqrt, exp 
from scipy import stats
import numpy as np

class EuropeanCall:
    def __init__(self, S, K, vola, days_to_expiration, div_yield=None):
        self.S = S
        self.K = K
        self.vola = vola
        self.days_to_expiration = days_to_expiration
        if div_yield == None:
            self.div_yield = 0
        else:
            self.div_yield = div_yield
        
    def internal_value(self):
        int_val = max(0,(self.S-self.K))
        return(int_val)
    
    def black_scholes_value(self, risk_free_rate):
        S0 = float(self.S)
        k = float(self.K)
        r = float(risk_free_rate)
        T = float(self.days_to_expiration / 365)
        q = float(self.div_yield)
        sigma = float(self.vola)
        d1 = (log(S0/k)+(r + 0.5 * sigma**2)*T)/(sigma * sqrt(T))
        d2 = (log(S0/k)+(r - 0.5 * sigma**2)*T)/(sigma * sqrt(T))
        bs_value = (S0 * stats.norm.cdf(d1, 0.0, 1.0)* exp(-q * T) \
                    - k * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
        return(bs_value)
    
    def monte_carlo_value(self, risk_free_rate, num_paths=100000):
        if num_paths== None:
            num_paths=1000
        else:
            num_paths=num_paths
        S0 = float(self.S)
        k = float(self.K)
        r = float(risk_free_rate)
        sigma = float(self.vola)
        T = self.days_to_expiration
        dt= 1/365 # length of a time interval ie day
        q = float(self.div_yield)
        results=[]
        for n in range(num_paths):
            path=[]
            for t in range(T+1):
                if t == 0: 
                    path.append(S0)
                else:
                    z = np.random.normal(loc=0, scale=1)
                    St = path[t - 1] * exp((r - q - 0.5 * sigma ** 2) * dt \
                                           + sigma * sqrt(dt) * z)
                    path.append(St)
           # print(path[-1])
            results.append(path)
        
        # MC estimator:
        #for i in results:
        #    print(max(i[-1] - k,0)) 
        C0 = exp(-r * (T * dt)) * sum([max(path[-1] - k, 0) for path in results])/num_paths 
        return(C0)
    
    def delta(self, risk_free_rate):
        S0 = float(self.S)
        k = float(self.K)
        r = float(risk_free_rate)
        T = float(self.days_to_expiration / 365)
        q = float(self.div_yield)
        sigma = float(self.vola)
        d1 = (log(S0/k)+(r + 0.5 * sigma**2)*T)/(sigma * sqrt(T))
        bs_delta = exp(-q * T)*stats.norm.cdf(d1, 0, 1)
        return(bs_delta)
    
    def mc_delta(self, risk_free_rate):
        S0 = float(self.S)
        r = float(risk_free_rate)
        k = float(self.K)
        T = float(self.days_to_expiration / 365)
        q = float(self.div_yield)
        sigma = float(self.vola)
        S_up = S0 *1.001
        S_down = S0 *0.999
        Up = EuropeanCall(S_up,k,sigma,int(365*T),q)
        Down = EuropeanCall(S_down,k,sigma,int(365*T),q)
        x= Up.monte_carlo_value(r)
        y= Down.monte_carlo_value(r)
        mc_delta=(x-y)/(S_up-S_down)
        return(mc_delta)
        
        
        
    
A = EuropeanCall(100,90,0.2,60,0.02)
x = A.internal_value()
print(x)
v = A.black_scholes_value(0.02)
print(v)
c=A.monte_carlo_value(0.02)
print(c)
d=A.delta(0.02)
print(d)
e=A.mc_delta(0.02)
print(e)