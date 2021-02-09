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

print(m.states)
print(m.alphabet)
print(m.initial_states)
print(m.final_states)
print(m.transitions)

# class Der:
#   def __init__(self, afn_lambda):
#     self.states = afn_lambda.states.copy()
#     self.alphabet = afn_lambda.alphabet.copy()
#     self.initial_states = afn_lambda.initial_states.copy()
#     self.final_states = afn_lambda.final_states.copy()
#     self.transitions = []
#     self.transform_afn_lambda_transitions(afn_lambda.transitions)

#   def transform_afn_lambda_transitions(self, afn_lambda_transitions):
#     for src in self.states:
#       state_transitions = [t for t in afn_lambda_transitions if t[0] == src]
#       for dest in self.states:
#         dest_transitions = [t[1] for t in state_transitions if t[0] == dest]
#         if len(dest_transitions):
#           print(dest_transitions)
#           # self.transitions.append([src, " + ".join(),dest])

# print(Der(m))