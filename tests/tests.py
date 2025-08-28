from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import uvicorn
from calculator import (
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

# Test addition endpoint with invalid inputs
# Data:[[{"a":"five","b":3}]]
def test_addition_invalid(client):
    response = client.post('/add', json={'a': 'five', 'b': 3})
    assert response.status_code == 422

# Test subtraction endpoint with valid inputs
# Data:[[{"a":10,"b":4}]]
def test_subtraction_valid(client):
    response = client.post('/subtract', json={'a': 10, 'b': 4})
    assert response.status_code == 200
    assert response.json() == {'result': 6}