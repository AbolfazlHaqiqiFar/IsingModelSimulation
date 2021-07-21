# Russell Kajouri & Abolfazl Haqiqifar
#Imail : afzhqq@gmail.com

from lattice import Lattice
import matplotlib.pyplot as plt

class Medium:

###########################################################################################

    def __init__(self, num= 64, dim=1, initial_config= 'stochastic', inputFilename="lattice.data",\
                        initial_direction = 1, J=1, h = 0, steps= 100, temp = 0,  display = False,\
                                outputfilename="trajectory.xyz", dump_step = 100):

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
        self.output = outputfilename
        self.dump_s = dump_step
        self.dim = dim
        self.lattice = Lattice(n = num, d = dim, mode = initial_config,\
            inputfile = inputFilename, dirr = initial_direction, J = J, h= h, latticeDisplay = display)
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
        spin, row, clmn = 0, 0, 0
        if self.dim == 1:
            spin = self.lattice.chooseSpin()
            energy_before_flip = self.lattice.energyOf_1D(spin)
            self.lattice.flipSpin_1D(spin)
            energy_after_flip  = self.lattice.energyOf_1D(spin)

        elif self.dim == 2:
            row = self.lattice.chooseSpin()
            clmn = self.lattice.chooseSpin()
            energy_before_flip = self.lattice.energyOf_2D(row, clmn)
            self.lattice.flipSpin_2D(row, clmn)
            energy_after_flip  = self.lattice.energyOf_2D(row,clmn)

        deltaE = energy_after_flip - energy_before_flip
        """
        If deltaE > 0 --> rejected in Monte Carlo 
            """
        if deltaE > 0 and not self.lattice.MetropoliceStep(self.Temp, deltaE):
            if self.dim == 1:
                self.lattice.flipSpin_1D(spin)
            elif self.dim == 2:
                self.lattice.flipSpin_2D(row,clmn)
###########################################################################################

    def MonteCarloSteps(self):
            for l in range(self.latticeSize):
                    self.SingleMonteCarlosteps()
            return self.lattice.energy(), self.lattice.polarization()
###########################################################################################

    def Evolution(self, display=False):
        """
		 we run the system for 20% of the monte carlo steps as the relaxation time
		 and won't insert it in our calculation
        """
        print("# The relaxation time has been started.")
        relaxation_steps = int(self.Steps / 5)
        for rs in range(relaxation_steps):
            self.MonteCarloSteps()
		
		# Now we start to calculate the energy and the magnerization of the system
		# for the given Monte Carlos steps

        print("# The relaxation time has been finished successfully.")
        print("# The Evolution time has been started.")

        polar_arr = []
        energ_arr = []

        ave_totalE = 0
        ave_orderP = 0
        for s in range(self.Steps):
            totalE, orderP = self.MonteCarloSteps()
            ave_totalE += totalE; ave_orderP += orderP

            polar_arr.append(orderP)
            energ_arr.append(totalE)

            polar_var = self.lattice.GetVariance(ave_orderP/self.Steps, polar_arr)
            energ_var = self.lattice.GetVariance(ave_totalE/self.Steps, energ_arr)

            if display:
                print("%-4.d %-5.3f %-5.3f"%(s, totalE, orderP))

            if self.dump_s != 0:
                self.lattice.dumpXYZ(self.output, self.dump_s, self.Steps, s)

        return (ave_totalE / self.Steps) , energ_var, (ave_orderP / self.Steps), polar_var


###########################################################################################

    def WriteTheLattice(self, name="lattice.data", wformat="txt"):
        if self.dim == 1:
            out = open(name, 'w')
            out.write("{}".format(self.latticeSize))
            for i in range(self.latticeSize):
                out.write(",{}".format(self.lattice.GetsBackSpin_1D(i)))
                pass
            out.close()
            print("### The lattice has been dumped by name: ", name)
        pass

