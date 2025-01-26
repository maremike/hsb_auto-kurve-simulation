Following program is a simulation of a car driving through an inclined turn. It makes use of numerical optimization.


Software information: <br/>
The program uses Python only (tested with version 3.13.1). <br/>
It has been tested on Windows 11 (24H2) and GNU-Linux Fedora (v41). <br/>


Program dependencies: <br/>
To install dependencies (in project folder): pip install -r requirements.txt <br/>
numpy (2.2.2), matplotlib (3.10.0), scipy (1.15.1), pyyaml (6.0.2) <br/>


Running the program: <br/>
Locate the file main.py (in src/control/) and run it using an IDE (tested with IntelliJ IDea 2024.3.1.1). <br/>
A different approach would be to download the release file and run that. <br/>
What each color of vector is for can be seen in the code under the package view. Or in the pdf assigned to the task. <br/>
All input and output parameters as well as the states of the program can be read from the console. <br/>


Changing the configuration: <br/>
The file config.yaml is responsible for initializing the variables and constraints. <br/>
Locate the file and adjust the constraints and variables. <br/>


Infos about the configuration: <br/>
If you want to increase the amount of simulation steps, adjust simulationIterations. <br/>
To change the input variables: <br/>
you can only adjust the following variables within the specified constraint (if unchanged): turnAngle, velocity, wheelDistance, temperature, roadWidth <br/>
you might adjust: gravity acceleration and gas content, but you have to adjust the constraints as well. If you want to focus the optimization on different aspects, the weighting can be adjusted as well (higher number = aim for lower value). <br/>
The simulation might struggle to find a suiting starting value. You might have been unlucky and the program chose bad starting values for the optimization. So you might have to run the program twice to finish the optimization. <br/>
But if it is still not working, the variable inaccuracyTolerance can be increased to allow more inaccurate values for faster optimization. <br/>
