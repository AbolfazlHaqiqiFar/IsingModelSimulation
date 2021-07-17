
# Russell Kajouri & Abolfazl Haqiqifar
#Imail : afzhqq@gmail.com


from spin import Spin
import numpy as np
import time



class Lattice():
#Lattice is a number of Spins together.
    ###########################################################################################

    def __init__(self, n, d , mode, inputfile, dirr, J, latticeDisplay)-> None:

        """
        n is Number of spins 
        d is Number of dimension
        J is called the exchange energy The size of J tells you how strongly neighboring spins are
             coupled to each other – how much they want to (anti-)align
             The sign of J tells you whether neighbors prefer to align or to anti-align.
              """
        np.random.seed(int(time.time()))
        self.Jfactor = J
        self.number = n
        self.dim = d # System dimiension
        self.L = []

        # Different modes of the system in terms of order and dimension
        if mode == "ordered":
            if self.dim == 1:
                self.ordered_localization1D(dirr)
            if self.dim == 2:
                self.ordered_localization2D(dirr)
        elif mode == "inputfile":
	        self.readInputFile(inputfile) 
        else:
            if self.dim == 1:
                self.stochastic_localization1D()
            elif self.dim == 2:
                self.stochastic_localization2D()
        if latticeDisplay :
            self.display()
        pass
    #1##########################################################################################
    """
    Spins can have one of the following initial conditions:
        1- Radomly and in a random direction(stochastic) --> Paramagnetism
        2- Regularly and in a specific direction(ordered) --> Ferromagnetism
    The end result has nothing to do whit the initial condition
    """
    def stochastic_localization1D(self):# for 1 dimiension
        for l in range(self.number):
            self.L.append(Spin(np.random.randint(0,2)*2-1))   
                # Here we need discrete random addiction (0 or 1)  
            pass
        pass
    ############################################################################################

    def stochastic_localization1D(self):# for 2 dimiension
        for l in range(self.number):
            dummy = []
            for k in range(self.number):
                dummy.append(Spin(np.random.randint(0,2)*2-1))
                pass
            #end of the second loop
            self.L.append(dummy)

    #2##########################################################################################

    def ordered_localization1D(self, dirr):# for 1 dimiension
        for l in range(self.number):
            self.L.append(Spin(dirr))
            pass
        pass
    ###########################################################################################

    def ordered_localization2D(self, dirr):# for 2 dimiension
        for l in range(self.number):
            dummy = []
            for k in range(self.number):
                dummy.append(Spin(dirr))
            self.L.append(dummy)    
            pass
        pass   
    ###########################################################################################

    def display(self):

        # Depending on the dimension the system show different behaviors
        if self.dim == 1:
            for l in range(self.number):
                    print(self.L[l].direction, end= "")
        print()
        
        if self.dim == 2:
            for l in range(self.number):
                for k in range(self.number):
                    print(self.L[l][k].direction, end= "")
                print(end = "\n")
    ###########################################################################################

    def energy(self):

        """
        Suppose the system is periodic & ferromagnetism ->  'J = 1 '
         Consider the system from base 2^n 
              so that we can easily get mood from it
              H = -J sum_i=0^N-1 (L_i)*(L_i+1)
              """
        ene = 0
        if self.dim == 1:
            for l in range(self.number):
                # ene += self.L[l].direction * self.L[self.period(l+1)].direction
                # ene += self.L[l].direction * self.L[self.period(l-1)].direction
                #or
                ene += self.energyOf_1D(l)#instead of the abov calculations, use the energyof function
            return (ene * 0.5) / self.number 
                #0.5 Because each spin has two neighbors
        elif self.dim == 2:
            for l in range(self.number):
                for k in range(self.number):
                    ene += self.energyOf_2D(l,k)
            return (ene * 0.25) / self.number * self.number
                #0.25 Because each spin has four neighbors 


         
    
    ###########################################################################################

    def period(self, n):

        """
        If the number it receives is out of range ,
          it returns it to the first ---> If the particles are N ==> L_N = L_0 
            """

        if n == self.number:
            return n % self.number
        elif n == -1:
            return self.number - 1
        else:
            return n
    ###########################################################################################

    def polarization(self):

        """
         This function finds the regularity of lattice 
        The initial value of the function is zero 
        Polarization should be close to zero
            """

        polariz = 0.0
        for l in range(self.number):
            polariz += self.L[l].direction
            pass
        return float(polariz / self.number)
    ###########################################################################################

    def energyOf(self, l):

        # Calculation of single Spin energy

        return -1 * self.Jfactor * self.L[l].direction *\
				(self.L[self.period(l-1)].direction + self.L[self.period(l+1)].direction)
    ###########################################################################################

    def flipSpin(self, l):
        # Changes the direction of the spin
        self.L[l].direction *= -1
    ###########################################################################################

    def chooseSpin(self):
         # Selects a spin at random
            return np.random.randint(0, self.number)
    ###########################################################################################
    
    def MetropoliceStep(self, temp, deltaE):
        """
         if temp = 0 --> false 
         if the temperature is bigger than zero , we get a random number between zero and one
               if bigger than exp(-deltaE/ temp) return True else return false
               """

        if temp == 0:
            return False
        else :
            return True if np.random.random() < np.exp(-deltaE / temp) else False
    ###########################################################################################

    def GetsBackSpin(self, i):
        return self.L[i].direction
    ###########################################################################################

    def readInputFile(self, filename):
        read = open(filename, 'r')
        str_L = read.readline().split(',')
        temp_lattice=[int(x) for x in str_L]
        if len(temp_lattice) - 1 == temp_lattice[0]:
            for i in range(self.number):
                self.L.append(Spin(temp_lattice[i + 1]))
        else:
            exit()
	###########################################################################################
    def GetVariance(self, Xbar, X):
         XVar = 0
         for i in range(len(X)):
            XVar += (X[i] - Xbar) * (X[i] - Xbar)
         return XVar / self.number
	###########################################################################################
    def dumpXYZ(self, output, dump_s, total_s, iterator):
         dump = open(output, "a+")
         if iterator % dump_s == 0 or iterator == total_s - 1:
            dump.write("{}\n".format(self.number))
            dump.write("spin_dir xloc yloc zloc\n")
            for i in range(self.number):
                dump.write("%d %d %d %d\n" %(self.L[i].direction, i, 0, 0))

         dump.close()
    ###########################################################################################