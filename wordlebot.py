#!/usr/bin/env python


import argparse
import pickle
import sys
from math import log
from wordledict import possible_answers as words
from wordledict import allowed_guesses as guesses

def compare(guess, target):
  # first of all, scan for greens
  r = list("_____")
  t = list(target)
  for i in range(5):
    if guess[i] == t[i]:
      r[i] = "G"
      t[i] = " "
  for i in range(5):
    if r[i] == "_" and guess[i] in t:
      r[i] = "Y"
      t.remove(guess[i])
  return ''.join(r)
      
      
def evaluate(guesses, words):
  t = []
  k = 1.0 / float(len(words))
  for guess in words:
    d = { }
    for w in words:
      r = compare(guess, w)
      d[r] = d.get(r, 0) + k
    e = sum([ d[r] * log(d[r])/log(2.) for r in d.keys()])
    t.append((-e, guess))
  t.sort()
  return t


try:
  print("::: reading entropy table...")
  entropy = pickle.load(open("wordle.p", "rb"))
except:
  print("::: entropy table not found, generating entropy table...")
  entropy = evaluate(guesses, words)
  pickle.dump(entropy, open("wordle.p", "wb"))

e, guess = entropy[-1]

while len(words) > 1:
  print('Guess "{}" (entropy = {:.2f})'.format(guess, e))
  response = input("What was the response? ")
  words = [ w for w in words if compare(guess, w) == response ]
  e, guess = evaluate(guesses, words)[0]

print("The secret word was {}".format(guess))
