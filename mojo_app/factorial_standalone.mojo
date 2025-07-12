import math

# Standalone factorial function for binary execution
fn factorial_int(n: Int) -> Int:
    return math.factorial(n)

# Main function for standalone execution
fn main():
    var result = factorial_int(5)
    print(result)