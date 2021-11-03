from threading import Thread, Lock
from time import sleep

class SillyStateMachine:
    """
    A finite state machine that uses a dict to tie strings to functions.

    The state machine will start on the first state in the dict.

    The whole thing runs on its own thread, so it's non-blocking and asynchronous. Users will
    benefit from knowledge of inter-thread communication methods.

    In each loop, it will:
    - Call interrupt() - overload this function!
    - Call the function pointed to by self.next_state
    - Sleep for a period defined by self.period

    Var kwargs can act as the arguments for the next function called as a state, in case you
    don't want to add class variables to handle that.
    """

    def __init__(self) -> None:
        super().__init__()
        self.States = {"Idle" : self._idle} # dict of state_mnemomic : state_function_pointer
        self.kwargs = {}      # keyword arguments for next function
        self.run_flag = False # setting to False will stop thread
        self.period = 0.0     # wait this amount of time between states
        self.prev_ret = None  # return value of previous function
        self.init_setup()   # overload to provide initial actions
        self.next_state = next(iter(self.States)) # set next state to first state in dict
        self.current_state = self.next_state

        # locks:
        self._state_manipulation_lock = Lock() # collision avoidance for setState()

    def init_setup(self):
        """
        This function is called at the end of __init__ for the parent class SillyStateMachine.
        
        Overload this function to provide initial actions like setting up self.States, events, and
        conditions.
        """
        pass

    def stop_actions(self):
        """
        Called when stop() is called. Overload this function to provide actions to take as
        the state machine shuts down.
        """
        pass

    def reset_actions(self):
        """
        Called when reset() is called. Overload this function to provide actions to take as
        the state machine is reset.
        """
        pass

    def start(self):
        """
        Start the state machine loop in a new thread.

        Will not start a new thread if one is already running.
        """
        if not self.run_flag:
            self.run_flag = True # enable thread loop
            loop = Thread(target = self.loop) # initialize thread
            loop.start() # start thread

    def stop(self):
        """Stop the thread. Does not reset the state machine!"""
        self.run_flag = False   # stops thread
        self.current_state = self.next_state # update current_state
        self.stop_actions()     # calls stop_actions - overload in child

    def loop(self):
        """Runs the state machine."""
        while self.run_flag:
            self._state_manipulation_lock.acquire() # avoid collision w/ setState()
            self.interrupt()            # interrupt() can be overloaded in child
            self.__next(**self.kwargs)    # call next state with keyword arguments
            self._state_manipulation_lock.release() # avoid collision w/ setState()
            sleep(self.period)  # wait period

    def interrupt(self):
        """
        Overload this - it'll run before the next state every loop.

        This is useful for checking conditions and events, or for running checks in general.
        """
        pass
    
    def __next(self, **kwargs):
        """Calls the function pointed to by next_state, with args = self.kwargs"""
        self.current_state = self.next_state   
        self.kwargs = {}    # clear self.kwargs so functions w/ no arguments don't have to
        self.prev_ret = self.States[self.current_state](**kwargs) # call next state function

    def reset(self):
        """
        Jumps to first state in self.States and stops the current thread.
        
        Triggers reset_actions() - overload reset_actions() in child class to provide actions.
        """
        self.next_state = next(iter(self.States)) # set state to first state in dict
        self.current_state = self.next_state      # update current_state
        self.run_flag = False   # stop thread
        self.reset_actions()    # reset_actions can be overloaded in child

    def _idle(self):
        """Do nothing."""
        pass

    def isRunning(self) -> bool:
        """Returns True if the state machine is active, False if it is not."""
        return self.run_flag

    def getState(self) -> str:
        """
        Returns mnemonic for current state.

        current_state is set in thread loop, so setState() won't be reflected in getState()
        immediately.
        """
        return self.current_state

    def setState(self, state_mnemonic : str):
        """
        Manually set the next state.
        
        This state will be set as soon as the current state is finished executing (but before sleep
        period), so it will take non-zero time to update.
        """
        if not state_mnemonic in self.States.keys():    # make sure state exists
            raise ValueError(state_mnemonic + " does not exist in State dictionary!")
        self._state_manipulation_lock.acquire() # avoid collisions
        self.next_state = state_mnemonic # set next state
        self._state_manipulation_lock.release() # avoid collisions

    def getPeriod(self) -> float:
        """Returns the current period to sleep between states."""
        return self.period


