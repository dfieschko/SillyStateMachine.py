from time import sleep
from SillyStateMachine import SillyStateMachine

def check_list(correct_list, actual_list):
    for x in range(0, len(correct_list) - 1):
        assert correct_list[x] == actual_list[x]

class BasicStateMachine(SillyStateMachine):
    """Test child"""
    def init_setup(self):
        self.status = "I haven't started yet!"
        self.States = {
            "Start" : self._start_state,
            "State 1" : self._state_1,
            "State 2" : self._state_2,
            "State 3" : self._state_3,
            "Idle" : self._idle
        }

        self.interrupted = False
        self.state_list = []
        self.ret_list = []

    def interrupt(self):
        self.interrupted = True
        self.state_list.append(self.next_state)
        if self.prev_ret != None:
            self.ret_list.append(self.prev_ret)

    def stop_actions(self):
        self.status = "Stopped!"

    def reset_actions(self):
        self.status = "Reset!"

    def _start_state(self):
        self.status = "I started!"
        self.period = 0.002
        self.next_state = "Start"

    def _state_1(self, next = 2):
        self.period = 0
        if next == 2:
            self.next_state = "State 2"
        else:
            self.next_state = "State 3"
    
    def _state_2(self):
        self.kwargs = {"next": 3}
        self.next_state = "State 1"
        return 2

    def _state_3(self):
        self.kwargs = {"next": 2}
        self.next_state = "State 1"
        return 3


def test_basic_init():
    machine = BasicStateMachine()
    assert machine.status == "I haven't started yet!"
    assert machine.next_state == "Start"
    assert machine.period == 0
    assert machine.run_flag == False
    assert machine.isRunning() == False

def test_basic_start_stop():
    machine = BasicStateMachine()
    machine.start()
    assert machine.isRunning() == True
    assert machine.getState() == "Start"
    assert machine.next_state == "Start"
    assert machine.status == "I started!"
    assert machine.period == 0.002
    assert machine.getPeriod() == 0.002
    machine.stop()
    assert machine.isRunning() == False
    assert machine.status == "Stopped!"

def test_basic_reset():
    machine = BasicStateMachine()
    machine.setState("State 1")
    machine.start()
    machine.reset()
    sleep(0.01)
    assert machine.isRunning() == False
    assert machine.getState() == "Start"
    assert machine.status == "Reset!"

def test_basic_interrupt():
    machine = BasicStateMachine()
    machine.start()
    sleep(machine.getPeriod())
    assert machine.interrupted == True
    machine.stop()
    assert machine.isRunning() == False

def test_basic_kwargs_ret():
    machine = BasicStateMachine()
    machine.setState("State 1")
    machine.start()
    sleep(0.05)
    machine.stop()
    correct_call_list = [
        "State 1",
        "State 2",
        "State 1",
        "State 3",
        "State 1",
        "State 2",
        "State 1",
        "State 3",
        "State 1",
        "State 2",
        "State 1",
        "State 3",
        "State 1",
        "State 2",
        "State 1",
        "State 3",
    ]
    actual_call_list = machine.state_list
    check_list(correct_call_list, actual_call_list)
    correct_ret_list = [
        2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3,
    ]
    actual_ret_list = machine.ret_list
    check_list(correct_ret_list, actual_ret_list)

def test_fail():
    assert False
