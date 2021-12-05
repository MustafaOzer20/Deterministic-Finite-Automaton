class State:
    def __init__(self, name, state="normal", **kwargs):
        if len(kwargs) == 0:
            raise Exception("State must have length greater than zero.")
        self.name = name
        self.state = state # start, final, normal, final-start, trap)
        self.transections = kwargs
        if self.state != "trap":
            for i in self.get_keys():
                self.transections[i] = None
        else:
            for i in self.get_keys():
                self.transections[i] = self

    def get_keys(self):
        return self.transections.keys()


    def __str__(self) -> str:
        return f'{self.name}, {self.state}'



class DynamicDFA:

    def __init__(self, example_state):
        # Example state's type must be State
        self.L = None
        self.sigma = None
        self.begin = None
        self.states = dict()
        self.sigma = list(example_state.get_keys())

    def addState(self, state):
        if self.sigma != list(state.get_keys()):
            raise Exception(f"Transitions to be added must match the alphabet of this dfa: {self.sigma}")
        self.states.update({state.name: state})

    def run(self, array):
        current = self.begin
        for letter in array:
            if letter in self.sigma:
                print(f"{current} -> {letter}")
                if current != None:
                    current = current.transections[letter]
                else:
                    raise Exception("Please make sure you have configured all states. 'self.configState'")
            else:
                return f"invalid input: {letter}"
        print(current)
        if 'final' in current.state:
            return True
        else:
            return False

    def configState(self, name, **kwargs):
        if list(kwargs.keys()) != self.sigma:
            raise KeyError("Your dictionary contains Invalid keys.")
        if None in kwargs.values():
            raise ValueError("DFA not contains 'None' value.")
        state = self.states[name]
        for i in kwargs.keys():
            temp = kwargs[i]
            kwargs[i] = self.states[temp]

        state.transections = kwargs

        if state.state == "start":
            self.begin = state

        return f"{state}"

    def configDFA(self, language):
        self.L = language

    
    def __str__(self) -> str:
        return str(self.L)


q0 = State("q0", "start", a=None, b=None)   
dfa = DynamicDFA(q0)

q1 = State("q1", "final", a=None, b=None) 
q2 = State("q2", a=None, b=None) 
q_t = State("q_t", "trap", a=None, b=None) 

dfa.addState(q0)
dfa.addState(q1)
dfa.addState(q2)
dfa.addState(q_t)

dfa.configState("q0", a="q_t", b="q1")
dfa.configState("q1", a="q2", b="q1")
dfa.configState("q2", a="q1", b="q2")

dfa.configDFA("starts with b and contains an even number of a")


print(dfa.run("babab"))
