"""
Calculator module with pure Python functions for mathematical operations.
Includes comprehensive error handling for edge cases.
"""
import math
import re
from typing import Union


class CalculatorError(Exception):
    """Custom exception for calculator operations."""
    pass


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract second number from first."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide first number by second."""
    if b == 0:
        raise CalculatorError("Division by zero is not allowed")
    return a / b


def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    try:
        result = base ** exponent
        if math.isinf(result):
            raise CalculatorError("Result is infinity")
        if math.isnan(result):
            raise CalculatorError("Invalid operation resulting in NaN")
        return result
    except OverflowError:
        raise CalculatorError("Number too large to represent")


def square_root(n: float) -> float:
    """Calculate square root of a number."""
    if n < 0:
        raise CalculatorError("Cannot calculate square root of negative number")
    return math.sqrt(n)


def modulus(a: float, b: float) -> float:
    """Calculate modulus (remainder) of division."""
    if b == 0:
        raise CalculatorError("Modulus by zero is not allowed")
    return a % b


def evaluate_expression(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    Only allows basic mathematical operations and functions.
    """
    if not expression or not isinstance(expression, str):
        raise CalculatorError("Invalid expression")
    
    # Remove whitespace
    expression = expression.replace(" ", "")
    
    # Check for invalid characters
    allowed_chars = set("0123456789+-*/().**sqrt()log()sin()cos()tan()abs().")
    if not all(c in allowed_chars or c.isdigit() or c in "+-*/()" for c in expression):
        raise CalculatorError("Expression contains invalid characters")
    
    # Check for balanced parentheses
    if expression.count("(") != expression.count(")"):
        raise CalculatorError("Unbalanced parentheses")
    
    # Replace mathematical functions with math module equivalents
    safe_expression = expression.replace("sqrt", "math.sqrt")
    safe_expression = safe_expression.replace("log", "math.log")
    safe_expression = safe_expression.replace("sin", "math.sin")
    safe_expression = safe_expression.replace("cos", "math.cos")
    safe_expression = safe_expression.replace("tan", "math.tan")
    safe_expression = safe_expression.replace("abs", "abs")
    
    # Define safe namespace for evaluation
    safe_dict = {
        "__builtins__": {},
        "math": math,
        "abs": abs
    }
    
    try:
        result = eval(safe_expression, safe_dict)
        if math.isinf(result):
            raise CalculatorError("Result is infinity")
        if math.isnan(result):
            raise CalculatorError("Invalid operation resulting in NaN")
        return float(result)
    except ZeroDivisionError:
        raise CalculatorError("Division by zero in expression")
    except (ValueError, TypeError, SyntaxError) as e:
        raise CalculatorError(f"Invalid expression: {str(e)}")
    except Exception as e:
        raise CalculatorError(f"Error evaluating expression: {str(e)}")