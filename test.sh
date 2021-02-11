#!/bin/bash

for case in test_cases/*.in
do
  echo "${case%.in}"
  ./tp1.py "$case" > tmp.out
  cat tmp.out
  cmp tmp.out "${case%.in}".out && echo "PASSED"
  echo ""
done
