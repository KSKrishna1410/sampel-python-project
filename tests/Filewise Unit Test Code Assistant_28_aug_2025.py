from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import uvicorn
import os
os.environ['PYTHONPATH'] = os.getcwd()
print(os.environ['PYTHONPATH'])
from app.calculator import (
    add, subtract, multiply, divide, power, square_root, modulus, 
    evaluate_expression, CalculatorError
)
import unittest
import pytest

# Test addition endpoint with valid inputs
# Data:[[{"a":5,"b":3}]]
def test_addition_valid(client):
    response = client.post('/add', json={'a': 5, 'b': 3})
    assert response.status_code == 200
    assert response.json() == {'result': 8}