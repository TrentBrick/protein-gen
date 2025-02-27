import numpy as np
import torch

class DoubleWell(object):

    params_default = {'a4' : 1.0,
                      'a2' : 6.0,
                      'a1' : 1.0,
                      'k' : 1.0,
                      'dim' : 1}

    def __init__(self, params=None):
        # set parameters
        if params is None:
            params = self.__class__.params_default
        self.params = params

        # useful variables
        self.dim = self.params['dim']
        self.AA_num = self.dim
        self.is_discrete = False

    def energy(self, x, argmax=False):
        dimer_energy =self.params['a4'] * x[:, 0] ** 4 - self.params['a2'] * x[:, 0] ** 2 + self.params['a1'] * x[:, 0]
        oscillator_energy = 0.0
        if self.dim == 2:
            oscillator_energy = (self.params['k'] / 2.0) * x[:, 1] ** 2
        if self.dim > 2:
            oscillator_energy = np.sum((self.params['k'] / 2.0) * x[:, 1:] ** 2, axis=1)
        return  -(dimer_energy + oscillator_energy)

    def energy_torch(self, x):
        dimer_energy =self.params['a4'] * x[:, 0] ** 4 - self.params['a2'] * x[:, 0] ** 2 + self.params['a1'] * x[:, 0]
        oscillator_energy = 0.0
        if self.dim == 2:
            oscillator_energy = (self.params['k'] / 2.0) * x[:, 1] ** 2
        if self.dim > 2:
            oscillator_energy = torch.sum((self.params['k'] / 2.0) * x[:, 1:] ** 2, dim=1)
        return  -(dimer_energy + oscillator_energy).unsqueeze(1)

    def plot_dimer_energy(self, axis=None, temperature=1.0):
        """ Plots the dimer energy to the standard figure """
        x_grid = np.linspace(-3, 3, num=200)
        if self.dim == 1:
            X = x_grid[:, None]
        else:
            X = np.hstack([x_grid[:, None], np.zeros((x_grid.size, self.dim - 1))])
        # flipping the energy again so that it plots the desirable direction
        energies = - (self.energy(X) / temperature)

        import matplotlib.pyplot as plt
        if axis is None:
            axis = plt.gca()
        #plt.figure(figsize=(5, 4))
        axis.plot(x_grid, energies, linewidth=3, color='black')
        axis.set_xlabel('x / a.u.')
        axis.set_ylabel('Energy / kT')
        axis.set_ylim(energies.min() - 2.0, energies[int(energies.size / 2)] + 2.0)

        return x_grid, energies