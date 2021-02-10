import sys

DELIMITER = ','
LINE_BREAK = '\n'
INITIAL_STATE = "__INITIAL__"
FINAL_STATE = "__FINAL__"
LAMBDA_TRANSITION = ''

if len(sys.argv) != 2:
  print("Usage: ./tp1 <input file>")
  sys.exit()

input_file = sys.argv[1]

input_data = open(input_file).read()
input_data = input_data.split(LINE_BREAK)
input_data = [i.split(DELIMITER) for i in input_data]

class AfnLambda:
  def __init__(self, states, alphabet, initial_states, final_states, transitions):
    self.states = states
    self.alphabet = alphabet
    self.initial_states = initial_states
    self.final_states = final_states
    self.transitions = transitions

  def add_state(self, s):
    self.states.append(s)

  def set_initial_states(self, initial_states):
    self.initial_states = initial_states

  def set_final_states(self, final_states):
    self.final_states = final_states

  def add_transition(self, src, symb, dest):
    self.transitions.append([src, symb, dest])

m = AfnLambda(
  input_data[0].copy(),
  input_data[1].copy(),
  input_data[2].copy(),
  input_data[3].copy(),
  []
)
for t in input_data[4:]:
  src = t[0]
  symb = t[1]
  dests = t[2:]
  for dest in dests:
    m.add_transition(src, symb, dest)

m.add_state(INITIAL_STATE)
for i in m.initial_states:
  m.add_transition(INITIAL_STATE, LAMBDA_TRANSITION, i)
m.set_initial_states([INITIAL_STATE])

m.add_state(FINAL_STATE)
for f in m.final_states:
  m.add_transition(f, LAMBDA_TRANSITION, FINAL_STATE)
m.set_final_states([FINAL_STATE])

class Der:
  def __init__(self, afn_lambda):
    self.states = afn_lambda.states.copy()
    self.alphabet = afn_lambda.alphabet.copy()
    self.initial_states = afn_lambda.initial_states.copy()
    self.final_states = afn_lambda.final_states.copy()
    self.transitions = []
    self.transform_afn_lambda_transitions(afn_lambda.transitions)

  def transform_afn_lambda_transitions(self, afn_lambda_transitions):
    for src in self.states:
      state_transitions = [t for t in afn_lambda_transitions if t[0] == src]
      for dest in self.states:
        dest_transitions_symb = [t[1] for t in state_transitions if t[2] == dest]
        if len(dest_transitions_symb):
          self.transitions.append([src, " + ".join([symb for symb in dest_transitions_symb if symb]), dest])

d = Der(m)

print(d.transitions)

class RegExp:
  def __init__(self, der):
    self.states = der.states.copy()
    self.alphabet = der.alphabet.copy()
    self.initial_states = der.initial_states.copy()
    self.final_states = der.final_states.copy()
    self.transitions = der.transitions.copy()
  
  def remove_transition_if_exists(self, t):
    if t in self.transitions:
      self.transitions.remove(t)

  def remaining_transitions(self):
    return [t for t in self.transitions if not (t[0] == INITIAL_STATE and t[2] == FINAL_STATE)]

  def first_removable_transitions(self):
    rt = self.remaining_transitions()
    if len(rt) == 0:
      return []

    t1 = None # e1 - e
    for t in rt:
      if t[0] != t[2]:
        t1 = t
        break
    if not t1:
      return []

    e1 = t1[0]
    e = t1[2]

    t2 = None # e - e
    for t in rt:
      if t[0] == e and t[2] == e:
        t2 = t
        break

    t3s = [] # e - e2
    for t in rt:
      if t != t1 and t != t2 and t[0] == e:
        t3s.append(t)
        break

    print("@"*50)
    print(t1)
    print("@"*50)

    result = []
    for t3 in t3s:
      t0 = None # e1 - e2
      e2 = t3[2]

      for t in rt:
        if t[0] == e1 and t[2] == e2:
          t0 = t
          break

      result.append((t0, t1, t2, t3))

    return result

  def build(self):
    while True:
      removable_transitions = self.first_removable_transitions()
      if len(removable_transitions) == 0:
        return

      for t0, t1, t2, t3 in removable_transitions:
        print("%"*50)
        print(t0, t1, t2, t3)
        print("%"*50)
        r1 = t1[1]
        r3 = t3[1]

        r0 = None
        if t0:
          r0 = t0[1]

        r2 = None
        if t2:
          r2 = t2[1]

        r = ""
        if r2:
          r = f'{r1}{r2}*{r3}'
        else:
          r = f'{r1}{r3}'

        if r0:
          r = f'({r0} + {r})'

        self.transitions.append([t1[0], r, t3[2]])
        self.remove_transition_if_exists(t0)
        self.remove_transition_if_exists(t1)
        self.remove_transition_if_exists(t2)
        self.remove_transition_if_exists(t3)

        print("*"*50)
        print(self.transitions)
        print("*"*50)

r = RegExp(d)
print("#"*50)
r.build()
print("#"*50)

print("&"*50)
print(r.transitions)
print("&"*50)