import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
dt = 1.0  # Time step
num_steps = 50  # Number of time steps
true_velocity = 1.0  # Constant velocity

# Generate true positions
x_true = np.arange(0, num_steps * dt, dt) * true_velocity

# Generate noisy measurements
measurement_noise_std = 2.0
z_measurements = x_true + np.random.normal(0, measurement_noise_std, size=num_steps)

# Kalman filter initialization
x_est = np.zeros(num_steps)  # Estimated position
P = np.zeros(num_steps)      # Estimate uncertainty
x_est[0] = 2.0               # Initial position estimate
P[0] = 10.0                   # Initial estimate uncertainty

# Define noise covariances
Q = 0.1  # Process noise covariance
R = measurement_noise_std ** 2  # Measurement noise covariance

#blue algo

for k in range(1,num_steps):
    x_pred = x_est[k-1] + true_velocity*dt
    P_pred = P[k-1] + Q
    K_k = P_pred/(P_pred+R)
    x_est[k] = x_pred + K_k*(z_measurements[k]-x_pred)
    P[k] = (1-K_k)*P_pred

plt.figure()
plt.plot(x_true,color="red",label = "x_true")
plt.scatter(range(num_steps),z_measurements , label = "obs")
plt.plot(x_est,"g--",label = "x_est",)
plt.legend()
plt.show() 

#2D 
x_true = np.zeros((4,num_steps))
x_true[:,0] = [0,1,0,1]

# State Matrix

F = np.array([
    [1,dt,0,0], # x(k+1) = x(k)+vx(k)+dt
    [0,1,0,0],
    [0,0,1,dt],
    [0,0,0,1]
])
#X(k+1) = F*X(k))

#Observation matrix
H = np.array([
    [1,0,0,0],
    [0,0,1,0]
])

#Process and mesurements noise covariances
Q = np.eye(4) * 0.0001
R = np.eye(2)*2.0

#Generate true positions and measurments
z_measurements = np.zeros((2,num_steps))
for k in range(1,num_steps):
    x_true[:,k] = F @ x_true[:,k-1] + np.random.multivariate_normal(np.zeros(4),Q)
    
    z_measurements[:,k] = H @ x_true[:,k] + np.random.multivariate_normal(np.zeros(2),R)

x_est = np.zeros((4,num_steps))
P = np.zeros((4,4,num_steps))
x_est[:,0] = [0,0.5,0,0.5]
P[:,:,0] = np.eye(4)

for k in range(1,num_steps):
    x_pred = F @ x_est[:,k-1]
    P_pred = F @ P[:,:,k-1] @ F.T + Q 

    y = z_measurements[:,k] - H @ x_pred
    S = H @ P_pred@H.T +R
    K = P_pred @ H.T @ np.linalg.inv(S)
    x_est [:,k] = x_pred + K @ y
    P[:,:,k] = (np.eye(4) - K @H ) @ P_pred


# Plot 
    
plt.figure(figsize=(12, 6))
plt.plot(x_true[0, :], x_true[2, :], label='True Position', color='green')
plt.scatter(z_measurements[0, :], z_measurements[1, :], color='red', label='Measurements', alpha=0.5)
plt.plot(x_est[0, :], x_est[2, :], label='Kalman Filter Estimate', linestyle='--', color='blue')
plt.xlabel('Position X')
plt.ylabel('Position Y')
plt.title('Two-Dimensional Position and Velocity Estimation using Kalman Filter')
plt.legend()
plt.show()