"""
Topic: Custom Classes in Python

Rectangle class that:
1. Takes length and width as integers during initialization.
2. Can be iterated over.
3. When iterated, first gives {'length': <value>} then {'width': <value>}
"""


class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}


# Testing the Rectangle class
if __name__ == "__main__":
    rect = Rectangle(10, 5)

    print("Iterating over Rectangle instance:")
    for item in rect:
        print(item)

    # We can also do it multiple times
    print("\nIterating again to show it works repeatedly:")
    for item in rect:
        print(item)
