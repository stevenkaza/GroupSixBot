To use: copy the files AI.py, Com.py and Move.py to a computer (these files are for the 'pi')
Copy the files UI.py and GUI.py to a difference computer (the laptop)
In AI.py in the init function call Com() with a free port number and the host with whatever the IP address of your OTHER computer is(the laptop).
ie: self.com = Com(8080,"192.168.0.105")
in GUI, in the init function near the bottom call self.u = UI() with whatever port number is being used in Com. the default is 13000.

On your laptop computer type 'python GUI.py'
On your 'pi' computer type 'python AI.py'

hopefully it all works!
------------
Move class

To use the move class,
1) first import Move (look up python importing modules if you need to)
2)Then create a new instance of the Move() type ie bot = Move()
 a) then we can do something like bot.move(5) for it to go forward 5 cm
3) Methods and Functions:

*****************
move(float distance)

Enter a positive integer for distance for the robot to travel
currently we have an offset so that the robot spins back to its starting direction /angle but
it depends on the surface of the robot

Enter a negative amount for the robot to move backwards.

*************
turn (float angle)

Enter a positive amount for the robot's desired angle, it will turn right
Enter a negative amount for the robot to turn left
Again this might have to change depending on the surface of the robot 
