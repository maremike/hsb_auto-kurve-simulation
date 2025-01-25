Following program is a simulation of a car driving through an inclined turn. It makes use of numerical optimization.


Software information:
The program uses Python only (tested with version 3.13.1).
It has been tested on Windows 11 (24H2) and GNU-Linux (Fedora & Debian).


Program dependencies: 
numpy, matplotlib, scipy, yaml


To run the program: 
Locate the file main.py (in src/control/) and run it.
A different approach would be to download the release file and run that. 


Changing the configuration: 
The file config.yaml is responsible for initializing the variables and constraints.
Locate the file and adjust the constraints and variables.


Infos about the configuration:
If you want to increase the amount of simulation steps, adjust simulationIterations.
To change the input variables:
you can only adjust the following variables within the specified constraint (if unchanged): turnAngle, velocity, wheelDistance, temperature, roadWidth
you might adjust: gravity acceleration and gas content, but you have to adjust the constraints as well. If you want to focus the optimization on different aspects, the weighting can be adjusted as well (higher number = aim for lower value).
The simulation might struggle to find a suiting starting value. You might have been unlucky and the program chose bad starting values for the optimization. So you might have to run the program twice to finish the optimization.
But if it is still not working, the variable inaccuracyTolerance can be increased to allow more inaccurate values for faster optimization.