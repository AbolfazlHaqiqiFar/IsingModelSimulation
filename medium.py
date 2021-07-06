
from lattice import Lattice
import matplotlib.pyplot as plt

class Medium:

###########################################################################################

    def __init__(self, num= 64, dim=1, initial_config= 'stochastic', \
        initial_direction= 1, J=1, steps= 100, temp= 0):

        """
        Medium class input include : 
            Number of system particles ---> 'num'
            System dimension ---> 'dim'
            Number of steps performed ---> 'steps'
            System temperature ---> 'temp'
            Initial direction means ' consider all spins up or down
            """

        self.Steps = steps
        self.Temp = temp
        self.latticeSize = num
        self.lattice = Lattice(n = num, d = dim, mode= initial_config, dirr= initial_direction, J = J)
        #print("ener: ", Lattice.energy())
        #print("polar: ", Lattice.polarization())
        #print(steps, temp)
###########################################################################################

    def SingleMonteCarlosteps(self):
        
        """
        In the Monte Carlo step, we first select a spin 
            and calculate its energy,Then change its direction 
            and calculate its energy again,after then calculate 
            the difference between two energies(deltaE)
            """
        spin = self.lattice.chooseSpin()
        energy_before_flip = self.lattice.energyOf(spin)
        self.lattice.flipSpin(spin)
        energy_after_flip  = self.lattice.energyOf(spin)
        deltaE = energy_after_flip - energy_before_flip
        """
        If deltaE > 0 --> rejected in Monte Carlo 
            """
        if deltaE > 0:
            #Take a Metropolice Step
            ans = self.lattice.MetropoliceStep(self.Temp, deltaE) #True or False
            if ans == False:
                self.lattice.flipSpin(spin)
###########################################################################################

    def MonteCarloSteps(self):
            for l in range(self.latticeSize):
                    self.SingleMonteCarlosteps()
            return self.lattice.energy(), self.lattice.polarization()
###########################################################################################

    def Evolution(self):
		    ave_totalE = 0
		    ave_orderP = 0
		    for s in range(self.Steps):
			    totalE, orderP = self.MonteCarloSteps()
			    ave_totalE += totalE
			    ave_orderP += orderP
			    #print("%-4.d %-5.3f %-5.3f"%(s, totalE, orderP))
                

		    return (ave_totalE / self.Steps) ,(ave_orderP / self.Steps) 