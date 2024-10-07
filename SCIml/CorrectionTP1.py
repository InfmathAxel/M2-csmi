import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
from sklearn.gaussian_process import GaussianProcessRegressor

############### class MLP ####################

class mlp(nn.Module):
    def __init__(self, layer_sizes=list):
        super().__init__()

        self.layer_sizes = layer_sizes ### tableau contenu la taille de chaque couche.
        self.hidden_layers = [] ### liste des couches 

        for i in range(0,len(layer_sizes)-1):
            self.hidden_layers.append(nn.Linear(self.layer_sizes[i], self.layer_sizes[i+1])) ### on construit la liste des couches linéaires 

        self.hidden_layers = nn.ModuleList(self.hidden_layers) 
        ### on transforme ca en liste de module ou les méthodes de module pourront être appliquées. Notamment utiles pour récuperer l'ensemble des paramètres entrainables
        self.activation=nn.Tanh() ## crée une couche d'activation Tanh

    def forward(self, inputs):
        ## le forward applique le réseau aux données. Ici on boucle sur les couhes linéaires et on applique à chaque fois couche linéaire puis activation
        for i in range(0,len(self.layer_sizes)-1):
            inputs = self.activation(self.hidden_layers[i].forward(inputs))
        return inputs

########## Résolution du problème elliptique ###########

def solve(N,Mh,vector_f=torch.ones(100)):
    dx= 1./N ## calcul dx
    A= (2.0/dx**2.0)*torch.diag(torch.ones(N+1),diagonal=0)-(1.0/dx**2.0)*torch.diag(torch.ones(N),diagonal=-1)-(1.0/dx**2.0)*torch.diag(torch.ones(N),diagonal=1)
    ### on crée la matrice. torch.diag crée une matrice diagonale de numéro de diagonal "diagonal" avec une tensor comme diagonale
    A[0,:]=0.0; A[0,0]=1.0
    A[-1,:]=0.0; A[-1,-1]=1.0
    vector_f[0]=0.0; vector_f[-1]=0.0
    ### on applique les conditions limites de Dirichlet Homogène
    x= torch.linalg.solve(A,vector_f)
    return x

N=20
## Nb maille
Mh = torch.linspace(0,1,N+1)
## maillage 
f=4.0*torch.pi**2.0*torch.sin(2.0*torch.pi*Mh)
### source associé à la solution sin(2\pi x)
sol_lap=solve(N,Mh,vector_f=f)
### on résout

### on affiche le résultat
plt.plot(Mh.detach().numpy(),sol_lap.detach().numpy())
plt.scatter(Mh.detach().numpy(),sol_lap.detach().numpy())
plt.show()


############ NN part #################

train_set = TensorDataset(Mh[:,None], sol_lap[:,None])
train_loader = DataLoader(train_set, batch_size=N+1, shuffle=True)
### crée un data set ou a chaque itération on renvoit N+1 data en mélangeant aléatoirement les données. Si batch_size < N+1 il y aura plusieurs iteration jusqu'a 
### ce que l'ensemble des données soit parcouru

model= mlp([1,20,40,20,1])
### on crée le modèle
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(),lr=0.05)
##@ création de la fonction de cout et de l'optimiseur
epochs=200
for epoch in range(epochs):
    total_loss = 0
    num = 0
    for x, y in train_loader:
        optimizer.zero_grad()
        ### on met le gradient a zéro
        y_pred = model(x)
        ### on applique le modèle au données.
        loss = criterion(y_pred, y)
        ### on applique la loss
        ### le gradient est mis a zéro car a chque fonction traversée on ajoute les contributions de gradients
        loss.backward()
        ## calcul du gradient final
        optimizer.step()
        ## etape d'optimisation
        total_loss += loss.item()
    print(epoch, total_loss )


Mh_test = torch.linspace(0.0,1.0,85)
sol_ref=torch.sin(2.0*torch.pi*Mh_test)
sol_nn = model.forward(Mh_test[:,None])
### on génére un maillage de test à 85 point, la solution de référence et la solution issue du réseau 


plt.plot(Mh_test.detach().numpy(),sol_ref.detach().numpy())
plt.scatter(Mh_test.detach().numpy(),sol_nn.detach().numpy())
plt.show()
### on affiche les résultats

############### Regression part ###############
from sklearn.kernel_ridge import KernelRidge
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic

kernel_ridge1 = KernelRidge(kernel= RBF(length_scale=0.05),alpha=0.001)
kernel_ridge1.fit(Mh[:,None].detach().numpy(), sol_lap.detach().numpy())
### on crée un régresseur et on fit les données

kernel_ridge2 = KernelRidge(kernel= RationalQuadratic(length_scale=0.05),alpha=0.001)
kernel_ridge2.fit(Mh[:,None].detach().numpy(), sol_lap.detach().numpy())
### on crée un régresseur et on fit les données

sol_kr1 = kernel_ridge1.predict(Mh_test[:,None])
sol_kr2 = kernel_ridge2.predict(Mh_test[:,None])
### on prédit les solutions des régressions

plt.plot(Mh_test.detach().numpy(),sol_ref.detach().numpy())
plt.scatter(Mh_test.detach().numpy(),sol_kr1)
plt.scatter(Mh_test.detach().numpy(),sol_kr2)
plt.show()

####### uncertain quatification part #######
Nmesure=5
x_mesure =torch.rand(size=(Nmesure,1))
f_mesure=4.0*torch.pi**2.0*torch.sin(2.0*torch.pi*x_mesure)
### on suppose qu'on connait la source en 5 points aléatoire

kernel = 1 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2))
gaussian_process = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
gaussian_process.fit(x_mesure.detach().numpy(),f_mesure.detach().numpy())
### on fit un GP sur ces 5 points donc on va pouvoir échantilloner aléatoire des fonctions
### conditionnellement au fait qu'elle passe par ses 5 points.

mean_prediction, std_prediction = gaussian_process.predict(Mh[:,None].detach().numpy(), return_std=True)
### on récupére un f moyen et l'écart type de f.

plt.scatter(x_mesure.detach().numpy(), f_mesure.detach().numpy())
plt.plot(Mh.detach().numpy(), mean_prediction, label="Mean prediction")
plt.fill_between(
    Mh.detach().numpy().ravel(),
    mean_prediction - 1.96 * std_prediction,
    mean_prediction + 1.96 * std_prediction,
    alpha=0.5,
    label=r"95% confidence interval",
)
plt.show()
### on plot la moyenne et l'écart type des f

nb_simu=100
u_sim=torch.zeros((nb_simu,N+1))
f=gaussian_process.sample_y(Mh[:,None].detach().numpy(),nb_simu)
### on échantillonne nb_simu fonctions f
for i in range(0,nb_simu):
    floc=torch.from_numpy(f[:,i]).to(torch.float32)
    sol_lap=solve(N,Mh,vector_f=floc)
    u_sim[i,:]=sol_lap

### on calcul les "nb_simu" solutions 

u_mean= torch.sum(u_sim,dim=0)/nb_simu
### on calcul la solution moyenne
u_mean=u_mean[None,:]
### on passe d'un tensor N à [1,N] pour pouvoir soustraire des tenseurs

u_sim= u_sim-u_mean
### on caucl pour chaque simu l'écart entre la simu et la simu moyenne
u_sigma2=torch.sum(u_sim**2.0,dim=0)/nb_simu
u_std=torch.sqrt(u_sigma2)
### calcul de la variance et de l'ecart type

plt.plot(Mh.detach().numpy(), u_mean[0,:], label="Mean prediction")
plt.fill_between(
    Mh.detach().numpy().ravel(),
    u_mean[0,:] - 1.96 * u_std,
    u_mean[0,:] + 1.96 * u_std,
    alpha=0.5,
    label=r"95% confidence interval",
)
plt.show()
### on plot