"""
FastAPI Calculator API with endpoints for mathematical operations and history tracking.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import uvicorn

from .calculator import (
    add, subtract, multiply, divide, power, square_root, modulus, 
    evaluate_expression, CalculatorError
)


app = FastAPI(
    title="Calculator API",
    description="A comprehensive calculator API with basic and advanced mathematical operations",
    version="1.0.0"
)


class OperationRequest(BaseModel):
    a: float
    b: float


class SingleOperandRequest(BaseModel):
    value: float


class PowerRequest(BaseModel):
    base: float
    exponent: float


class ExpressionRequest(BaseModel):
    expression: str


class OperationResponse(BaseModel):
    operation: str
    input: Dict[str, Any]
    result: float
    timestamp: str


# In-memory history storage (in production, use a database)
calculation_history: List[OperationResponse] = []


def add_to_history(operation: str, input_data: Dict[str, Any], result: float) -> OperationResponse:
    """Add a calculation to the history."""
    response = OperationResponse(
        operation=operation,
        input=input_data,
        result=result,
        timestamp=datetime.datetime.now().isoformat()
    )
    calculation_history.append(response)
    return response


@app.get("/")
async def root():
    """Welcome message and API information."""
    return {
        "message": "Welcome to Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "operations": ["/add", "/subtract", "/multiply", "/divide", "/power", "/sqrt", "/modulus", "/evaluate"],
            "history": ["/history", "/history (DELETE)"]
        }
    }


@app.post("/add", response_model=OperationResponse)
async def add_numbers(request: OperationRequest):
    """Add two numbers."""
    try:
        result = add(request.a, request.b)
        return add_to_history("addition", {"a": request.a, "b": request.b}, result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/subtract", response_model=OperationResponse)
async def subtract_numbers(request: OperationRequest):
    """Subtract second number from first."""
    try:
        result = subtract(request.a, request.b)
        return add_to_history("subtraction", {"a": request.a, "b": request.b}, result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/multiply", response_model=OperationResponse)
async def multiply_numbers(request: OperationRequest):
    """Multiply two numbers."""
    try:
        result = multiply(request.a, request.b)
        return add_to_history("multiplication", {"a": request.a, "b": request.b}, result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/divide", response_model=OperationResponse)
async def divide_numbers(request: OperationRequest):
    """Divide first number by second."""
    try:
        result = divide(request.a, request.b)
        return add_to_history("division", {"a": request.a, "b": request.b}, result)
    except CalculatorError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/power", response_model=OperationResponse)
async def power_operation(request: PowerRequest):
    """Raise base to the power of exponent."""
    try:
        result = power(request.base, request.exponent)
        return add_to_history("power", {"base": request.base, "exponent": request.exponent}, result)
    except CalculatorError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sqrt", response_model=OperationResponse)
async def square_root_operation(request: SingleOperandRequest):
    """
    Calculate the square root of a number provided in the request.

    Args:
        request (SingleOperandRequest): A request object containing a single operand for the operation.

    Returns:
        JSONResponse: A JSON response containing the operation details and result.

    Raises:
        HTTPException: If a CalculatorError occurs, with a status code of 400.
        HTTPException: For any other exceptions, with a status code of 500.
    """
    try:
        # Compute the square root of the input value.
        result = square_root(request.value)
        # Add the operation to the history and return the result.
        return add_to_history("square_root", {"value": request.value}, result)
    except CalculatorError as e:
        # Handle specific calculator errors with a 400 response.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors with a 500 response.
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modulus", response_model=OperationResponse)
async def modulus_operation(request: OperationRequest):
    """Calculate modulus (remainder) of division."""
    try:
        result = modulus(request.a, request.b)
        return add_to_history("modulus", {"a": request.a, "b": request.b}, result)
    except CalculatorError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate", response_model=OperationResponse)
async def evaluate_math_expression(request: ExpressionRequest):
    """Evaluate a mathematical expression."""
    try:
        result = evaluate_expression(request.expression)
        return add_to_history("evaluate", {"expression": request.expression}, result)
    except CalculatorError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=List[OperationResponse])
async def get_history():
    """Get calculation history."""
    return calculation_history


@app.delete("/history")
async def clear_history():
    """Clear calculation history."""
    global calculation_history
    count = len(calculation_history)
    calculation_history.clear()
    return {"message": f"History cleared. Removed {count} entries."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)