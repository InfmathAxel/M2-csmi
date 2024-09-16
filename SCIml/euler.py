import numpy as np
import matplotlib.pyplot as plt
import torch 


class systeme:
    def __init__(self,n=1,H = None,dH_dp = None,dH_dq= None):
        self.n = n
        self.H = H
        self.dH_dp = dH_dp
        self.dH_dq = dH_dq


class EulerExplicit:
    def __init__(self,sys=None):
        self.p = []
        self.q = []
        self.H = []
        self.sys = sys

    def initial_condition(self,po,q0):
        self.p.append(po)
        self.q0.append(q0)