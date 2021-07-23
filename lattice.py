
# Russell Kajouri & Abolfazl Haqiqifar
#Imail : afzhqq@gmail.com


from spin import Spin
import numpy as np
import time



class Lattice():
    '''
    Lattice is a number of Spins together.
        '''
    ###########################################################################################

    def __init__(self, n, d , mode, inputfile, dirr, J, h, latticeDisplay)-> None:

        """
        n is Number of spins 
        d is Number of dimension
        J is called the exchange energy The size of J tells you how strongly neighboring spins are
             coupled to each other – how much they want to (anti-)align
             The sign of J tells you whether neighbors prefer to align or to anti-align.
              """
        np.random.seed(int(time.time()))
        self.Jfactor = J
        self.magfactor = h
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
    def stochastic_localization1D(self):
        '''
        Radomly and in a random direction(stochastic) --> Paramagnetism

        for 1 dimiension
        '''
        for l in range(self.number):
            self.L.append(Spin(np.random.randint(0,2)*2-1))   
                # Here we need discrete random addiction (0 or 1)   
        pass
    ############################################################################################

    def stochastic_localization2D(self):# 
        '''
        Radomly and in a random direction(stochastic) --> Paramagnetism 

        for 2 dimiension
        '''
        for l in range(self.number):
            dummy = []
            for k in range(self.number):
                dummy.append(Spin(np.random.randint(0,2)*2-1))
                pass
            #end of the second loop
            self.L.append(dummy)

    #2##########################################################################################

    def ordered_localization1D(self, dirr):
        '''
        Regularly and in a specific direction(ordered) --> Ferromagnetism

        for 1 dimiension
        '''
        for l in range(self.number):
            self.L.append(Spin(dirr))
    ###########################################################################################

    def ordered_localization2D(self, dirr):
        '''
        Regularly and in a specific direction(ordered) --> Ferromagnetism

        for 2 dimiension
        '''
        for l in range(self.number):
            dummy = []
            for k in range(self.number):
                dummy.append(Spin(dirr))
            self.L.append(dummy)    
            pass
        pass   
    ###########################################################################################

    def display(self):

        '''Depending on the dimension the system show different behaviors'''
        if self.dim == 1:
            for l in range(self.number):
                    print(self.L[l].direction, end= "")
        print()
        
        if self.dim == 2:
            for l in range(self.number):
                for k in range(self.number):
                    print('%-1d'%self.L[l][k].direction, end= "")
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
                ene += -self.L[l].direction * self.energy1D_Of(l)
                #instead of the abov calculations, use the energyof function
            return (ene * 0.5) / self.number 
                #0.5 Because each spin has two neighbors
        elif self.dim==2:
            for l in range(self.number):
                for k in range(self.number):
                    ene += -self.L[l][k].direction*self.energy2D_Of(l,k)
            return (ene * 0.25) / (self.number * self.number)
                #0.25 Because each spin has four neighbors 


         
    
    ###########################################################################################

    def period(self, n):

        """
        If the number it receives is out of range ,
          it returns it to the first ---> If the particles are N ==> L_N = L_0 
            """

        return n % self.number
    ###########################################################################################

    def polarization(self):

        """
         This function finds the regularity of lattice 
        The initial value of the function is zero 
        Polarization should be close to zero
            """
        polariz = 0.0
        if self.dim == 1:
            for l in range(self.number):
                polariz += self.L[l].direction
            return float(polariz / self.number)
        if self.dim == 2:
            for l in range(self.number):
                for k in range(self.number):
                    polariz += self.L[l][k].direction
            return float(polariz / (self.number * self.number))
    ###########################################################################################

    def energy_flipSpin_1D(self, l):
        return 2 * self.L[l].direction * self.energy1D_Of(l)
	

    def energy_flipSpin_2D(self, l , k):
        return 2 * self.L[l][k].direction * self.energy2D_Of(l,k)
    ###########################################################################################

    def energy1D_Of(self, l):
        '''Calculation of single Spin energy'''
        summ =	self.L[self.period(l-1)].direction +\
				        self.L[self.period(l+1)].direction
        return self.Jfactor * summ + self.magfactor
    


    def energy2D_Of(self, l, k):
            ''' Calculation of single Spin energy'''
            summ =	self.L[self.period(l-1)][k].direction +\
				            self.L[self.period(l+1)][k].direction +\
				            self.L[l][self.period(k-1)].direction +\
				            self.L[l][self.period(k+1)].direction

            return self.Jfactor * summ + self.magfactor
    ###########################################################################################

    def flipSpin_1D(self, l):
        '''Changes the direction of the spin in one dimiension'''
        self.L[l].direction *= -1
    ###########################################################################################

    def flipSpin_2D(self, l, k):
        '''Changes the direction of the spin in 2 dimiension'''
        self.L[l][k].direction *= -1
    ###########################################################################################

    def chooseSpin(self):
         '''Selects a spin at random'''
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
    
    def GetsBackSpin_1D(self, l):
        """Return the spin to its orginal state for one dimiension"""
        return self.L[l].direction
    
    def GetsBackSpin_2D(self, l, k):
        """Return the spin to its orginal state for 2 dimiension"""
        return self.L[l][k].direction
    ###########################################################################################
    def readInputFile(self, filename):
        read = open(filename, 'r')
        while True:
            str_L = read.readline().strip().split(',')
            print(str_L)
            if len(str_L)==2 and int(str_L[1])==self.dim:
                print("The inputfile has been detected!")
                break
            elif len(str_L)>2 or len(str_L)<2:
                print("something is wrong in your inputfile")
                exit()

        if self.dim==1:
            temp=[int(x) for x in str_L]
            if temp[0]==self.number:
                while True:
                    lattice = read.readline().strip().split(',')
                    if len(lattice) == self.number:
                        break
                    else:
                        print("Number of spins are not equal with the reported value in source code")
                        exit()
                lattice = [int(x) for x in lattice]
                for i in range(self.number):
                    self.L.append(Spin(lattice[i]))
            else:
                print("Number of spin is not compatible with the source code")
                exit()

        elif self.dim==2:
            temp=[int(x) for x in str_L]
            if temp[0]==self.number:
                for l in range(self.number):
                    while True:
                        lattice = read.readline().strip().split(',')
                        if len(lattice) == self.number:
                            break
                        else:
                            print("Number of spins are not equal with the reported value in source code")
                            exit()
                    lattice = [int(x) for x in lattice]
                    dummy=[]
                    for i in range(self.number):
                        dummy.append(Spin(lattice[i]))
                    self.L.append(dummy)
            else:
                print("Number of spin is not compatible with the source code")
                exit()
	###########################################################################################
    def GetVariance(self, Xbar, X): 
        '''Takes Variance from input values
                input values include the average and individual data
        '''
        XVar = 0
        for i in range(len(X)):
            XVar += (X[i] - Xbar) * (X[i] - Xbar)
        return XVar / self.number
	###########################################################################################
    def dumpXYZ(self, output, dump_s, total_s, iterator):
         dump = open(output, "a+")
         if iterator % dump_s == 0 or iterator == total_s - 1:
            if self.dim == 1:
                dump.write("{}\n".format(self.number))
                dump.write("spin_dir xloc yloc zloc\n")
                for i in range(self.number):
                    dump.write("%d %d %d %d\n" %(self.L[i].direction, i, 0, 0))

            if self.dim == 2:
                dump.write("{}\n".format(self.number * self.number))
                dump.write("spin_dir xloc yloc zloc\n")
                for i in range(self.number):
                    for j in range(self.number):
                        dump.write("%d %d %d %d\n" %(self.L[i][j].direction, j, -i, 0))

         dump.close()
    ###########################################################################################