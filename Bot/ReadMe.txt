To use: copy the files AI.py, Com.py and Move.py to a computer (these files are for the 'pi')
Copy the files UI.py and GUI.py to a difference computer (the laptop)
In AI.py in the init function call Com() with a free port number and the host with whatever the IP address of your OTHER computer is(the laptop).
ie: self.com = Com(8080,"192.168.0.105")
in GUI, in the init function near the bottom call self.u = UI() with whatever port number is being used in Com. the default is 13000.

On your laptop computer type 'python GUI.py'
On your 'pi' computer type 'python AI.py'

hopefully it all works!