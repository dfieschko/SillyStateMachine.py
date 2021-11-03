# SillyStateMachine.py
A simple state machine running on its own thread that chooses states from a dict of state names and function pointers.

The main purpose of this project was to familiarize myself with automated unit tests with Github Actions and pytest.

```
pip install SillyStateMachine
```

## Creating a state machine with SillyStateMachine
```python
from SillyStateMachine import SillyStateMachine

# make a child of SillyStateMachine and define its states
class MyMachine(SillyStateMachine):
    def init_setup(self): # overload init_setup to set up the class
        # required - set States dictionary
        self.States = { # State dict - mnemonic string : function pointer
            "Start" : self._start_state,
            "State 1" : self._state_1,
            "State 2" : self._state_2,
            "State 3" : self._state_3
        } # Initial state is automatically set to first state in dict.
        
        # not required - set initial sleep period
        self.period = 0.001 # time.sleep(period) is called once per loop
                            # default period is 0

        # initialize your own class variables
        self.var1 = 0
        self.var2 = "beep"

    # overload functions

    def interrupt(self): # not required
        # interrupt() is called once per loop.
        # overload it to perform checks/actions
        if external_trigger():
            do_stuff()

    def stop_actions(self): # not required
        ...
    
    def reset_actions(self): # not required
        ...

    # define the behavior of each state

    def _start_state(self):
        
        ... # do whatever you want the state to do
        self.period = 0.05 # you can set the sleep period in each state
        if condition: # set the next state
            self.next_state = "State 1"
        else:
            self.next_state = "State 2"
    
    def _state_1(self):
        ...

    def _state_2(self):
        ...

    def _state_3(self):
        ...

    # define your own functions for interacting with the machine
    def func1(self):
        ...
    def func2(self):
        ...
```
## Running the state machine
```python
# continued from example above

# initialize the machine
machine = MyMachine()

# start the state machine
machine.start()

# access member objects & variables
print(machine.getState())   # e.g.  >>> "State 3"
print(machine.isRunning())  # e.g.  >>> True
print(machine.getPeriod())  # e.g.  >>> 0.05
machine.setState("State 1") # manually set the next state

# stop or reset the state machine
machine.stop()  # will stop running but not reset state
                # stop() will call stop_actions() - overload this!

machine.reset() # will stop running AND reset state
                # reset() will call reset_actions() - overload this!
```
