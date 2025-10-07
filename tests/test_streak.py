import pytest
import sys
import os

# Add the project root to the Python path to resolve the module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streak import longest_positive_streak

def test_empty_list():
    assert longest_positive_streak([]) == 0

def test_multiple_streaks():
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_with_zeros():
    assert longest_positive_streak([1, 2, 0, 3, 4, 5]) == 3

def test_with_negatives():
    assert longest_positive_streak([-1, -2, 1, 2, 3, -3, 4]) == 3

def test_all_positive():
    assert longest_positive_streak([1, 2, 3, 4, 5]) == 5

def test_all_non_positive():
    assert longest_positive_streak([-1, -2, 0, -5]) == 0

def test_single_element_positive():
    assert longest_positive_streak([5]) == 1

def test_single_element_non_positive():
    assert longest_positive_streak([-5]) == 0

def test_streaks_at_beginning_and_end():
    assert longest_positive_streak([1, 2, 3, -5, 4, 5]) == 3
    assert longest_positive_streak([1, 2, -5, 4, 5, 6]) == 3

def test_long_list():
    assert longest_positive_streak([1] * 100) == 100
    assert longest_positive_streak(([1, 2, -1] * 50)) == 2