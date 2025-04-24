#  Tramway Queue Modeling

A Python simulation for modeling and analyzing tramway systems using queuing theory.

---

##  Overview

This project implements a mathematical model to simulate and analyze the behavior of a tramway transit system. It uses queuing theory (specifically the **M/M/c** model) to calculate key performance metrics like wait times, queue lengths, and system stability under different operational conditions.

---

##  Features

- **Advanced Queue Theory Modeling**: Implementation of the M/M/c queuing model optimized for transit systems  
- **Interactive Visualizations**: 2D and 3D plots to visualize relationships between different parameters  
- **System Stability Analysis**: Tools to determine if a given configuration can handle passenger demand  
- **Parameter Optimization**: Find optimal values for vehicle count and capacity  

---

##  Project Structure

- `tramwayV2.py` : Core implementation of the tramway queuing model class  
- `projet.ipynb` : Jupyter notebook with examples, simulations, and visualizations  

---

##  Getting Started

###  Prerequisites

matplotlib
numpy
plotly
ipython

###  Running Simulations

1. **Import the tramway class**
`from tramwayV2 import *`
3. **Create a tramway object**
`tw = tramway()`
5. **Configure system parameters**
   # Parameters:
    1. Capacity of each tramway (number of seats)
    2. Complete trip time (minutes)
    3. Average time between clients (minutes)
    4. Number of stations
    5. Number of vehicles
    6. Percentage of trip spent serving clients
  `tw.setAllParams(90, 70, 0.2, 20, 24, 40)`
7. **Get and analyze results**
`tw.printResults()`
##  Key Parameters

| Parameter                    | Description                                     |
|------------------------------|-------------------------------------------------|
| `nbrDePlacesDansUnTramway`   | Number of seats in each tramway                 |
| `tempsVoyageComplet`         | Complete trip time (in minutes)                 |
| `tempsMoyenEntreDeuxClients` | Average time between two client arrivals (min)  |
| `nbrStations`                | Number of stations in the system                |
| `nbrVehicules`               | Number of vehicles operating                    |
| `alpha`                      | % of trip time spent serving clients            |

---

##  Output Metrics

- `mu` : Service rate  
- `lambda` : Arrival rate  
- `rho` : Utilization factor  
- `P0` : Probability the system is empty  
- `L` : Avg. number of clients in the system  
- `Lq` : Avg. number in the queue  
- `W` : Avg. time in the system  
- `Wq` : Avg. waiting time in queue  

---

##  Visualization Examples

The notebook includes visualizations showing:

- How wait times vary with vehicle count for different arrival rates  
- How tramway capacity affects system stability and wait times  
- Optimal configurations for different demand scenarios  

---

##  License

This project is available for academic and research purposes.

---

##  Contributors

Developed by Mustapha for public transportation queue modeling and optimization.
