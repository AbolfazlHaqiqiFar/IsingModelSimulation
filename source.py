# We define the main function in which the code is executed


from medium import Medium

def main():
    out = open("data.ising", "w")

    dt = 0.010
    for t in range(0,40):
        print("temp: {:6.4f}".format(t*dt))
        medium = Medium(num = 128,
				dim = 1,
				initial_config = "inputfile",
				inputFilename="lattice.data",
				outputfilename="trajectory.xyz",
				dump_step=0,
				initial_direction = 1,
				steps = 250000,
				temp = t*dt,
				display=False )

        aveE, varE, aveP, varP = medium.Evolution(display=False)
        print("%-5.3f\t%-5.3f\t%-5.3f\t%-5.3f\t%-5.3f" %(t*dt,aveE,varE,aveP,varP), file=out)
        medium.WriteTheLattice()
        print("#", "-"*70)
    
if "__main__"==__name__:
        main()  