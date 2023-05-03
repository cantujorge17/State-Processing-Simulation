# State-Processing-Simulation
A PyGame program that simulates an OS state machine

### Steps to run application:

1. Clone the repository
2. Open the repository in a terminal
3. Install pygame using the command `pip3 install pygame`
4. Use the command `python3 main.py` to run the application

### How to use application:
When you launch the application, you will start in the process menu screen.
In the top left corner of the application, there are buttons to add and
remove processes from the simulation. Underneath each of the processes
contains four variables:

- Arrival Time: The time the process will arrive to the simulation
- CPU Time: The time needed to run the process to completion
- I/O Time: The time where an I/O request is made (-1 means there is no I/O 
request)
- I/O Duration: The time needed to complete I/O request (Does not appear if
I/O Time is -1)

These variables can be modified by clicking on any of the processes in the 
menu screen, which opens the settings menu. When modifying the values, the 
CPU Time can not be lower than the I/O Time, and vise versa. In order to
exit the settings menu, click on the save button to save the new values,
or click on cancel to discard the changes made to the variables.

The simulation can be run by clicking on the "Run Simulation" button.
When the simulation is running, the state of the processes will be shown,
as well as the current time unit. The time can be incremented by clicking
anywhere on the screen. The arrow in the simulation represents the CPU
performing an action on the specified process. In order to exit the
simulation, simply click the "Go Back" button to return the the process
menu screen.