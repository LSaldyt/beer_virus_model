from scipy.integrate import odeint
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np


from parameters import estimate_parameters_by_region
from read import read

class SIRD_Model:

    def __init__(self, population, init_infected, init_recovered, init_dead):
        self.population     = population
        self.init_infected  = init_infected
        self.init_recovered = init_recovered
        self.init_dead      = init_dead

        self.init_susceptible = self.population - self.init_infected - self.init_recovered

    # See reference.py
    def deriv(self, y, t, N, beta, gamma, yeet):
        S, I, R, D = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        dDdt = yeet * I
        return dSdt, dIdt, dRdt, dDdt

    def plot(self, ax, beta, gamma, yeet, duration=1000, alpha=0.3, lw=0.8):
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        # A grid of time points (in days)
        t = np.linspace(0, duration, duration)

        # The SIR model differential equations.

        # Initial conditions vector
        y0 = self.init_susceptible, self.init_infected, self.init_recovered, self.init_dead
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(self.deriv, y0, t, args=(self.population, beta, gamma, yeet))
        S, I, R, D = ret.T

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        ax.plot(t, S/self.population, 'b', alpha=alpha, lw=lw) # , label='Susceptible')
        ax.plot(t, I/self.population, 'r', alpha=alpha, lw=lw) # , label='Infected')
        ax.plot(t, R/self.population, 'g', alpha=alpha, lw=lw) # , label='Recovered with immunity')
        ax.plot(t, D/self.population, 'k', alpha=alpha, lw=lw) # , label='Dead')

def main():
    regions = read()
    params  = estimate_parameters_by_region(regions, ('Hubei', 'China'))

    pprint(params) 

    print('Beginning model..', flush=True)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)
    model = SIRD_Model(1200000, 13, 0, 0)
    # model = SIRD_Model(58000000, 444, 28, 17)
    for i in range(49, 150):
        model.plot(ax, params['infection_rate'] * ((i+1)/100), params['recovery_rate'], params['death_rate'])
    model.plot(ax, params['infection_rate'], params['recovery_rate'], params['death_rate'], alpha=1.0, lw=3)
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Population')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()
    # model.plot(params['infection_rate'], params['naive_recovery_rate'], params['naive_death_rate'])


if __name__ == '__main__':
    main()
