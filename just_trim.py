import uavsim #Import the main library
import numpy as np #Import the numpy library
from uavsim.utility.trim import compute_trim #Import the trim function
import matplotlib.pyplot as plt # Import the graph library 
from mpl_toolkits.mplot3d import Axes3D

sim_timestep = 0.01 #Time delta (in seconds) of the simulation

uav_params = uavsim.UAVParams('params.yaml') #Get the UAV parameters (class defined in "...\uavsim\parameters\uav_parameters.py")
sensor_params = uavsim.SensorParams('sensor_params.yaml') #Get the sensors parameters (not used in this code)

uav_dynamics = uavsim.UAVDynamics(uav_params, sensor_params, sim_timestep) #Get the UAV parameters (class defined in "...\uavsim\uav_dynamics.py")

uav_velocity_ref = 25 # Total velocity reference
gamma_ref = 0 # Flight path angle reference

# Trimming the UAV and showing the results
trim_state, trim_delta = compute_trim(uav_dynamics, uav_velocity_ref, gamma_ref)
print(trim_state)
print(trim_delta)

# Initial states and surface control commands
uav_dynamics.state = trim_state
delta = trim_delta

sim_time = 0.0 #Simulation initial time
sim_total_time = 600 #Simulation total time (in seconds)
n_steps = int(sim_total_time / sim_timestep) #Number of steps in the simulation

# Creating the vectors to store the velocities values
u = np.zeros(n_steps+1)
v = np.zeros(n_steps+1)
w = np.zeros(n_steps+1)

# Creating the vectors to store the position values
px = np.zeros(n_steps+1)
py = np.zeros(n_steps+1)
pz = np.zeros(n_steps+1)

# Creating the vectors to store the time values
time = np.zeros(n_steps+1)

print('Starting Simulation...')

n = 0
while n < (n_steps + 1):

   wind = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T #Wind linear and angular velocities equals to zero (just for a basic test) 
   uav_dynamics.update(delta, wind) #Update the UAV states

   # Store the velocities, positions and time values
   u[n] = uav_dynamics.state[3]
   v[n] = uav_dynamics.state[4]
   w[n] = uav_dynamics.state[5]
   px[n] = uav_dynamics.state[0]
   py[n] = uav_dynamics.state[1]
   pz[n] = uav_dynamics.state[2]
   time[n] = sim_time

   # Increment the time and step of the simulation  
   sim_time += sim_timestep
   n += 1

print('Simulation Done...')

#Plot the velocities in the body axis
fig, axs = plt.subplots(3)
fig.suptitle('Body axis velocities')
axs[0].plot(time,u)
axs[1].plot(time,v)
axs[2].plot(time,w)

#Plot the UAV trajectory
fig = plt.figure(2)
ax = fig.gca(projection='3d')
ax.plot(px,py,-pz)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()