import torch
from typing import Callable

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import copy as cp
from torch import nn
from torch.autograd import grad

class SystemH: #### une classe qui va gérer le système physique
    def __init__(self,n:int=1,H:Callable=None):
        self.n=n ### nombre de particules
        self.H = H ## fonction Hamiltonien

    def generator_init(self,m_q:float,m_p:float,sigma_q:float,sigma_p:float,nb_simu:int):
        #### on se donne une moyenne et variance pour les variables p,q
        #### on génère aléatoire "nb_simu" conditions initiales
        tens=torch.ones((nb_simu,self.n))
        q0=torch.normal(m_q*tens,sigma_q*tens)
        p0=torch.normal(m_p*tens,sigma_p*tens)
        return q0,p0

    def gradH(self,q:torch.Tensor,p:torch.Tensor):
        #### on calcul le gradient de H par rapport à q,p avec pytorch
        q= torch.tensor(q,requires_grad=True) ### on transforme q en tensor dont on veut stocker le gradient
        p= torch.tensor(p,requires_grad=True) ### on transforme p en tensor dont on veut stocker le gradient
        He=self.H(q,p) ### on évalue H
        
        dH_dq= grad(He, q, torch.ones_like(q), create_graph=True)[0] ### on calcul le grad / q
        dH_dp= grad(He, p, torch.ones_like(p), create_graph=True)[0] ### on calcul le grad / p
        return dH_dq,dH_dp
        

class TimeScheme:
    #### une classe général pour les schémas en temps
    def __init__(self,sys:SystemH=None):
        self.sys=sys ### on lui donne un système
        self.p= [] ### liste des p(t)
        self.q =[] ### liste des q(t)
        self.H = [] ### liste des H(t)
        self.time=[] ### liste des t

    def initial_condition(self,q0:torch.Tensor,p0:torch.Tensor):
        ### on stocke les conditions initiales
        self.p.append(p0)
        self.q.append(q0)
        self.H.append(self.sys.H(q0,p0))
        self.time.append(0.0)

    def OnetimeStep(self,dt):
        ### fonction qui calculera une étape en temps
        pass

    def LoopInTime(self,T:int=10,dt:int=0.1):
        ### boucle en temps
        while self.time[-1] < T:
            qs,ps=self.OnetimeStep(dt) ### on applique les schémas puis on stocke les quantités
            self.p.append(ps)
            self.q.append(qs)
            self.H.append(self.sys.H(qs,ps))
            self.time.append(self.time[-1]+dt)


class EulerExplicit(TimeScheme):
    ### classe qui hérite de TimeScheme 
    def OnetimeStep(self,dt):
        ### on calcul le gradient de H et on applique le schéma
        dH_dq_n, dH_dp_n = self.sys.gradH(self.q[-1],self.p[-1])

        qnp= self.q[-1]+dt*dH_dp_n
        pnp= self.p[-1]-dt*dH_dq_n
        return qnp,pnp

class EulerSymplectic(TimeScheme):
    ### classe qui hérite de TimeScheme 

    def fixepoint(self,f,q0):
        ### fonction qui calcul un point fixe de $x=f(x)$
        for i in range(0,50):
            q=f(q0)
            q0=cp.copy(q)
        return q

    def OnetimeStep(self,dt):
        ## une étape en temps de Euler symplectique
        f = lambda q: self.q[-1]+self.sys.gradH(q,self.p[-1])[1]
        qnp= self.fixepoint(f,self.q[-1])
        ### on calcul q n+1 en implicite
        dH_dq_n = self.sys.gradH(qnp,self.p[-1])[0] 
        pnp= self.p[-1]-dt*dH_dq_n
        ### puis p n+1 explicite
        return qnp,pnp


def plot(scheme,list_simu,i_var:int=0):
    ### fonction pour faire les plots
    fig, ax = plt.subplots(2, 2, figsize=(12, 6))
    scheme.q= torch.stack(scheme.q,dim=0).detach().numpy() ### on transforme une liste de tenseurs en tenseurs (pratique pour les plots)
    ### on transforme le tenseur en tableau numpy
    scheme.p= torch.stack(scheme.p,dim=0).detach().numpy()
    scheme.H= torch.stack(scheme.H,dim=0).detach().numpy()

    for i_simu in list_simu:
        ax[0,0].plot(scheme.time,scheme.q[:,i_simu,i_var])
        ax[0,0].set_title("q(t)")

        ax[0,1].plot(scheme.time,scheme.p[:,i_simu,i_var])
        ax[0,1].set_title("p(t)")

        ax[1,0].plot(scheme.q[:,i_simu,i_var],scheme.p[:,i_simu,i_var])
        ax[1,0].set_title("portrait de phase")

        ax[1,1].plot(scheme.time,scheme.H[:,i_simu,i_var])
        ax[1,1].set_title("H")
    plt.show()
    
#### exemple ######   
def H_oscillator(q,p):
    omega =2.0
    return 0.5*p*p +0.5*(omega**2)*q*q

def H_oscillator_nl(q,p):
    omega =2.0
    return 0.5*p*p +0.5*(omega**2)*q*q + 0.333*q*q*q

    

Oscillator = SystemH(1,H_oscillator_nl)
q0,p0=Oscillator.generator_init(1.0,0.1,0.1,0.4,5)

Schema1=EulerExplicit(Oscillator)
Schema1.initial_condition(q0,p0)
Schema1.LoopInTime(30,0.02)
plot(Schema1,list_simu=[0,1,3],i_var=0)

Schema2=EulerSymplectic(Oscillator)
Schema2.initial_condition(q0,p0)
Schema2.LoopInTime(30,0.02)
plot(Schema2,list_simu=[0,1,3],i_var=0)
