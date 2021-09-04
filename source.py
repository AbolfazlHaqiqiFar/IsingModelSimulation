# We define the main function in which the code is executed


from numpy import fabs
from medium import Medium

def main():
    out = open("data.ising", "w")

    dt = 0.10
    for t in range(-30,30):
        print("temp: {:6.4f}".format(t*dt))
        medium = Medium(num = 64,
				dim = 2,
				initial_config = "ordered",
				inputFilename="lattice.data",
				outputfilename='trajectory.xyz',
				dump_evolution=1500,
				dump_relaxation=0,
				initial_direction = 1,
        J= 1,
        h = t*dt,
				steps = 15000,
				temp = 0.5,
				display=True )

        aveE, varE, aveP, varP = medium.Evolution(display=False)
        print("%-5.3f\t%-5.3f\t%-5.3f\t%-5.3f\t%-5.3f" %(t*dt,aveE,varE,aveP,varP), file=out, flush=True)

        medium.WriteTheLattice()
        print("#", "-"*70)
        pass
    
if "__main__"==__name__:
        main()  
