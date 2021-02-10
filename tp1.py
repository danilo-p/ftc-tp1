import sys

DELIMITER = ','
LINE_BREAK = '\n'
INITIAL_STATE = "__INITIAL__"
FINAL_STATE = "__FINAL__"
LAMBDA_TRANSITION = ''

class State:
  def __init__(self, name, initial = False, final = False):
    self.name = name
    self.initial = initial
    self.final = final

  def set_final(self, final):
    self.final = final

  def set_initial(self, initial):
    self.initial = initial

  def human_readable(self):
    flags = ""

    if self.final:
      flags += "F"

    if self.initial:
      flags += "I"

    if len(flags) == 0:
      flags += "-"

    return f'State({self.name}, {flags})'

  def __eq__(self, obj):
    return self.name == obj.name

  def __str__(self):
    return self.human_readable()

  def __repr__(self):
    return self.human_readable()

class Transition:
  def __init__(self, src, symb, dest):
    self.src = src
    self.symb = symb
    self.dest = dest

  def human_readable(self):
    return f'Transition({self.src}, {self.symb}, {self.dest})'

  def __str__(self):
    return self.human_readable()

  def __repr__(self):
    return self.human_readable()

class AfnLambda:
  def __init__(self, states, transitions):
    self.states = states
    self.transitions = []

  def add_state(self, s):
    self.states.append(s)

  def get_initial_states(self):
    return [s for s in self.states if s.initial]

  def get_final_states(self):
    return [s for s in self.states if s.final]

  def add_transition(self, t):
    self.transitions.append(t)

class Der:
  def __init__(self, afn_lambda):
    self.states = afn_lambda.states.copy()
    self.transitions = []
    self.transform_afn_lambda_transitions(afn_lambda.transitions)

  def transform_afn_lambda_transitions(self, afn_lambda_transitions):
    for src in self.states:
      state_transitions = [t for t in afn_lambda_transitions if t.src == src]
      for dest in self.states:
        dest_transitions_symb = [t.symb for t in state_transitions if t.dest == dest]
        if len(dest_transitions_symb):
          r = " + ".join([symb for symb in dest_transitions_symb if symb])
          if len(dest_transitions_symb) > 1:
            r = f'({r})'
          self.transitions.append(Transition(src, r, dest))

class RegExp:
  def __init__(self, der):
    self.states = der.states.copy()
    self.transitions = der.transitions.copy()
  
  def remove_transition_if_exists(self, t):
    if t in self.transitions:
      self.transitions.remove(t)

  def remaining_transitions(self):
    return [t for t in self.transitions if not (t.src == State(INITIAL_STATE) and t.dest == State(FINAL_STATE))]

  def first_removable_transitions(self):
    remaining = self.remaining_transitions()
    if len(remaining) == 0:
      return []

    t1s = [] # e1 - e
    for t in remaining:
      if t.src != t.dest:
        t1s.append(t)

    if len(t1s) == 0:
      return []

    for t1 in t1s:
      e1 = t1.src
      e = t1.dest

      t2 = None # e - e
      for t in remaining:
        if t.src == e and t.dest == e:
          t2 = t
          break

      t3s = [] # e - e2
      for t in remaining:
        if t != t1 and t != t2 and t.src == e:
          t3s.append(t)

      if len(t3s) == 0:
        continue

      result = []
      for t3 in t3s:
        t0 = None # e1 - e2
        e2 = t3.dest

        for t in remaining:
          if t.src == e1 and t.dest == e2:
            t0 = t
            break

        result.append((t0, t1, t2, t3))

      return result

    return []

  def build(self):
    while True:
      removable_transitions = self.first_removable_transitions()
      if len(removable_transitions) == 0:
        return

      for t0, t1, t2, t3 in removable_transitions:
        r1 = t1.symb
        r3 = t3.symb

        r0 = None
        if t0:
          r0 = t0.symb

        r2 = None
        if t2:
          r2 = t2.symb

        r = ""
        if r2:
          r = f'{r1}{r2}*{r3}'
        else:
          r = f'{r1}{r3}'

        if r0:
          r = f'({r0} + {r})'

        self.transitions.append(Transition(t1.src, r, t3.dest))
        self.remove_transition_if_exists(t0)
        self.remove_transition_if_exists(t1)
        self.remove_transition_if_exists(t2)
        self.remove_transition_if_exists(t3)

  def __str__(self):
    return self.transitions[0].symb

if len(sys.argv) != 2:
  print("Usage: ./tp1 <input file>")
  sys.exit()

input_file = sys.argv[1]

input_data = open(input_file).read()
input_data = input_data.split(LINE_BREAK)
input_data = [i.split(DELIMITER) for i in input_data]

states = [State(s) for s in input_data[0].copy()]

for initial_state_name in input_data[2].copy():
  for s in states:
    if s == State(initial_state_name):
      s.set_initial(True)

for final_state_name in input_data[3].copy():
  for s in states:
    if s == State(final_state_name):
      s.set_final(True)

m = AfnLambda(states, [])

for t in input_data[4:]:
  src = t[0]
  symb = t[1]
  dests = t[2:]
  for dest in dests:
    m.add_transition(Transition(State(src), symb, State(dest)))

new_initial_state = State(INITIAL_STATE, initial=True)
for i in m.get_initial_states():
  m.add_transition(Transition(new_initial_state, LAMBDA_TRANSITION, i))
  i.set_initial(False)
m.add_state(new_initial_state)

new_final_state = State(FINAL_STATE, final=True)
for f in m.get_final_states():
  m.add_transition(Transition(f, LAMBDA_TRANSITION, new_final_state))
  i.set_final(False)
m.add_state(new_final_state)

d = Der(m)
r = RegExp(d)
r.build()
print(r)