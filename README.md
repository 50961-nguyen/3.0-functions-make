## Setup
- `func_make.py` in your Unit 2 Make Folder

## Autograding
Put `func_make.py` in the repository root. The GitHub Actions workflow runs the
tests on each push and reports a score out of 100:

| Test group | Points |
| --- | ---: |
| Header comments | 10 |
| Function docstrings | 20 |
| Type annotations | 15 |
| IPO comments | 15 |
| Triangle calculation | 20 |
| Slope calculation | 20 |

All tests in a group must pass to earn that group's points. View the score in
the GitHub Actions workflow run. GitHub Classroom was retired in August 2026,
so scores cannot be reported to the Classroom application.

## Instructions
Within this file, you will create two functions: `calculate_triangle(num)` `and calculate_slope(x1, x2, y1, y2)` that both return their respective calculations. [Make sure these are the exact names of the functions]

**What is a triangle?**
    - The triangle of a number is a summation of all the numbers from 1 up to and including the number. 
    - For example, the triangle of 6 is 1 + 2 + 3 + 4 + 5 + 6 = 21
    - To accomplish this, use a `for loop`!

**Recap: Slope of a Line**
    - To calculate the slope of a line, you need two points that are on this line: Point 1 (x1, y1) and Point 2 (x2, y2)
    - The equation is `slope = (y2 - y1) / (x2 - x1)`.
    - The function `calculate_slope(x1, x2, y1, y2)` should return the slope of the line (float) OR returns `undefined` (str). When you use type annotation, you will need to do `float|str` as the return value.  
    - Hint: think about WHEN does the slope does not exist! 

Don't forget Header Comments, IPO comments in main(), and docstrings for your functions!

## Starter code
```python
"""
HEADER COMMENTS
"""

## TODO: make calculate_triangle function here
## TODO: make calculate_factorial function here

def main():
    """
    TODO: write a sentence to describe what you're doing in your main().
    """
    # Call calculate_triangle and calculate_factorial here and print out their answers
    # Feel free to free style here. My autotesting will check the return value of your functions above.
    pass # again, delete this when you write in main()
```
