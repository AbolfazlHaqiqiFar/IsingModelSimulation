#  Abolfazl Haqiqifar
#Imail : afzhqq@gmail.com

from lattice import Lattice
import matplotlib.pyplot as plt

class Medium:

###########################################################################################

    def __init__(self, num= 64, dim=1, initial_config= 'stochastic', inputFilename="lattice.data",\
                        initial_direction = 1, J=1, h = 0, steps= 100, temp = 0,  display = False,\
                        outputfilename="trajectory.xyz", dump_evolution = 100, dump_relaxation = 0):

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
        if dim == 1:
            self.latticeSize = num
        elif dim == 2:
            self.latticeSize = num*num
        self.output = outputfilename
        self.dump_s = dump_evolution
        self.dump_r = dump_relaxation
        self.dim = dim
        self.num = num
        self.lattice = Lattice(n = num, d = dim, mode = initial_config,\
            inputfile = inputFilename, dirr = initial_direction, J = J, h= h, latticeDisplay = display)
        #print("ener: ", Lattice.energy())
        #print("polar: ", Lattice.polarization())
        #print(steps, temp)
###########################################################################################
        

    def SingleMonteCarloStep(self):
            '''
                    In the Monte Carlo step, we first select a spin 
            and calculate its energy,Then change its direction 
            and calculate its energy again,after then calculate 
            the difference between two energies(deltaE)

            If deltaE > 0 --> rejected in Monte Carlo

        '''
            if self.dim == 1:
                spin = self.lattice.chooseSpin()
                deltaE = self.lattice.energy_flipSpin_1D(spin)
            elif self.dim == 2:
                row  = self.lattice.chooseSpin()
                clmn = self.lattice.chooseSpin()
                deltaE = self.lattice.energy_flipSpin_2D(row, clmn)

                
            if deltaE <= 0 or self.lattice.MetropoliceStep(self.Temp, deltaE):
                if self.dim==1: self.lattice.flipSpin_1D(spin)
                elif self.dim==2: self.lattice.flipSpin_2D(row, clmn)
###########################################################################################

    def MonteCarloSteps(self):
            for l in range(self.latticeSize):
                    self.SingleMonteCarloStep()
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
            self.loading(rs, relaxation_steps)
            if self.dump_r != 0:
                self.lattice.dumpXYZ(self.output, self.dump_r, relaxation_steps, rs)
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
            self.loading(s, self.Steps)
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
            out.write("{},{}".format(self.num, self.dim))
            for i in range(self.num):
                if i < self.num-1:
                    out.write("{},".format(self.lattice.GetsBackSpin_1D(i)))
                else:
                    out.write("{}".format(self.lattice.GetsBackSpin_1D(i)))
            out.close()
            print("### The lattice has been dumped by name: ", name)
        elif self.dim==2:
            out = open(name, 'w')
            out.write("{},{}\n".format(self.num,self.dim))
            for i in range(self.num):
                for l in range(self.num):
                    if l<self.num-1:
                        out.write("{},".format(self.lattice.GetsBackSpin_2D(i,l)))
                    else:
                        out.write("{}\n".format(self.lattice.GetsBackSpin_2D(i,l)))
            out.close()
            print("### The lattice has been dumped by name: ", name)
        pass
    ###########################################################################################

    def loading(self, m, M):
        M2 = M / 100.0
        if m==0:
            print("%-3d%% passed.          "%(0),end="\r")
        elif m % M2 == 0:
            print("%-3d%% passed,          "%int(m/M2),end="\r")

