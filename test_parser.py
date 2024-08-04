import os
import re
import pytest
from jsonparser import runFile

testFileDirectory = 'tests'


def test_step1():
  for filename in os.listdir('tests/step1'):
    f = os.path.join('tests/step1', filename)
    print(f)
    if re.search(r"^valid\d*\.json$", filename):
      assert runFile(f) == True
    elif re.search(r"^invalid\d*\.json$", filename):
      assert runFile(f) == False

def test_step2():
  for filename in os.listdir('tests/step2'):
    f = os.path.join('tests/step2', filename)
    print(f)
    if re.search(r"^valid\d*\.json$", filename):
      assert runFile(f) == True
    elif re.search(r"^invalid\d*\.json$", filename):
      assert runFile(f) == False

def test_step3():
  for filename in os.listdir('tests/step3'):
    f = os.path.join('tests/step3', filename)
    print(f)
    if re.search(r"^valid\d*\.json$", filename):
      assert runFile(f) == True
    elif re.search(r"^invalid\d*\.json$", filename):
      assert runFile(f) == False

def test_step4():
  for filename in os.listdir('tests/step4'):
    f = os.path.join('tests/step4', filename)
    print(f)
    if re.search(r"^valid\d*\.json$", filename):
      assert runFile(f) == True
    elif re.search(r"^invalid\d*\.json$", filename):
      assert runFile(f) == False