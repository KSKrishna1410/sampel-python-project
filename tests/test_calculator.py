"""
Comprehensive unit tests for the calculator module.
Tests all operations and edge cases including error handling.
"""
import unittest
import math
import sys
import os

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from calculator import (
    add, subtract, multiply, divide, power, square_root, modulus, 
    evaluate_expression, CalculatorError
)


class TestCalculator(unittest.TestCase):
    
    def test_add(self):
        """Test addition operation."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(2.5, 3.7), 6.2)
        self.assertEqual(add(-5, -3), -8)
    
    def test_subtract(self):
        """Test subtraction operation."""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-3, -1), -2)
        self.assertEqual(subtract(10.5, 5.5), 5.0)
        self.assertEqual(subtract(1, 1), 0)
    
    def test_multiply(self):
        """Test multiplication operation."""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(0, 100), 0)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(-2, -3), 6)
        self.assertEqual(multiply(2.5, 4), 10.0)
    
    def test_divide(self):
        """Test division operation."""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(-8, 4), -2)
        self.assertEqual(divide(-6, -2), 3)
        self.assertEqual(divide(0, 5), 0)
    
    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with self.assertRaises(CalculatorError) as context:
            divide(5, 0)
        self.assertIn("Division by zero", str(context.exception))
    
    def test_power(self):
        """Test power operation."""
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(10, 1), 10)
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(9, 0.5), 3.0)
        self.assertEqual(power(-2, 2), 4)
        self.assertEqual(power(-2, 3), -8)
    
    def test_power_edge_cases(self):
        """Test power operation edge cases."""
        # Test for overflow
        with self.assertRaises(CalculatorError):
            power(10, 1000)
    
    def test_square_root(self):
        """Test square root operation."""
        self.assertEqual(square_root(9), 3)
        self.assertEqual(square_root(16), 4)
        self.assertEqual(square_root(0), 0)
        self.assertEqual(square_root(2), math.sqrt(2))
        self.assertAlmostEqual(square_root(0.25), 0.5)
    
    def test_square_root_negative(self):
        """Test square root of negative number raises error."""
        with self.assertRaises(CalculatorError) as context:
            square_root(-1)
        self.assertIn("Cannot calculate square root of negative number", str(context.exception))
    
    def test_modulus(self):
        """Test modulus operation."""
        self.assertEqual(modulus(10, 3), 1)
        self.assertEqual(modulus(15, 5), 0)
        self.assertEqual(modulus(7, 2), 1)
        self.assertEqual(modulus(-10, 3), 2)
        self.assertEqual(modulus(10, -3), -2)
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        with self.assertRaises(CalculatorError) as context:
            modulus(5, 0)
        self.assertIn("Modulus by zero", str(context.exception))
    
    def test_evaluate_expression_basic(self):
        """Test basic expression evaluation."""
        self.assertEqual(evaluate_expression("2 + 3"), 5)
        self.assertEqual(evaluate_expression("10 - 4"), 6)
        self.assertEqual(evaluate_expression("3 * 4"), 12)
        self.assertEqual(evaluate_expression("15 / 3"), 5)
        self.assertEqual(evaluate_expression("2 ** 3"), 8)
    
    def test_evaluate_expression_complex(self):
        """Test complex expression evaluation."""
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)
        self.assertEqual(evaluate_expression("10 + 2 * 3"), 16)
        self.assertEqual(evaluate_expression("(10 + 2) * (3 + 1)"), 48)
        self.assertAlmostEqual(evaluate_expression("3.14 * 2"), 6.28)
    
    def test_evaluate_expression_with_functions(self):
        """Test expression evaluation with mathematical functions."""
        self.assertAlmostEqual(evaluate_expression("sqrt(16)"), 4)
        self.assertAlmostEqual(evaluate_expression("sqrt(2) * sqrt(2)"), 2, places=10)
        self.assertAlmostEqual(evaluate_expression("abs(-5)"), 5)
    
    def test_evaluate_expression_errors(self):
        """Test expression evaluation error cases."""
        # Division by zero
        with self.assertRaises(CalculatorError):
            evaluate_expression("5 / 0")
        
        # Invalid expression
        with self.assertRaises(CalculatorError):
            evaluate_expression("2 +")
        
        # Unbalanced parentheses
        with self.assertRaises(CalculatorError):
            evaluate_expression("(2 + 3")
        
        # Empty expression
        with self.assertRaises(CalculatorError):
            evaluate_expression("")
        
        # Invalid characters
        with self.assertRaises(CalculatorError):
            evaluate_expression("2 + a")
    
    def test_evaluate_expression_square_root_negative(self):
        """Test square root of negative in expression."""
        with self.assertRaises(CalculatorError):
            evaluate_expression("sqrt(-1)")
    
    def test_calculator_error_inheritance(self):
        """Test that CalculatorError is properly inherited from Exception."""
        self.assertTrue(issubclass(CalculatorError, Exception))
    
    def test_floating_point_precision(self):
        """Test floating point operations maintain reasonable precision."""
        result = add(0.1, 0.2)
        self.assertAlmostEqual(result, 0.3, places=10)
        
        result = subtract(1.0, 0.9)
        self.assertAlmostEqual(result, 0.1, places=10)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests combining multiple operations."""
    
    def test_complex_calculation_sequence(self):
        """Test a sequence of operations working together."""
        # ((2 + 3) * 4) / 2 = 10
        step1 = add(2, 3)  # 5
        step2 = multiply(step1, 4)  # 20
        step3 = divide(step2, 2)  # 10
        self.assertEqual(step3, 10)
    
    def test_power_and_square_root(self):
        """Test power and square root are inverse operations."""
        original = 5
        powered = power(original, 2)  # 25
        rooted = square_root(powered)  # 5
        self.assertAlmostEqual(rooted, original)
    
    def test_expression_vs_manual_calculation(self):
        """Test that expression evaluation matches manual calculations."""
        manual_result = multiply(add(2, 3), subtract(10, 6))  # 5 * 4 = 20
        expression_result = evaluate_expression("(2 + 3) * (10 - 6)")
        self.assertEqual(manual_result, expression_result)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)