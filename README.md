# IsingModelSimulation

This is the code of the Ising model in Physics science

The code has been prepared for 1D, 2D configuration and you can choose the
initial configuration of the system into three modes, the first is at the

 ordered configuration which means all of spins are in the same direction
wether are up or down
The second option has been provided by inputfilename command which enables
us to set an arbitrary configuration for our system.
And the third option is stochastic mode which mean the spins' direction are
random.

The above are the available command in the code

 num(int) -> the number of spin in a row, this number must choose at the base of digit 2
dim(int) -> 1 or 2 which are representing of 1D or 2D respectively

 initial_config(str) -> "ordered", "stochastic", "inputfile" The unavailable command
will have considered as a stochastic initial configuration.

inputfilename(str) -> This command is used when the initial configuration is on inputfilename mode
outputfilename(str) -> it is used to determine the name of the output file
dump_evolution(int) -> zero means no report and positive number means we have a snapshot every "dump_evolution" step
dump_relaxtation(int) ->
initial_direction
J :: the strength of the external magnetic field
