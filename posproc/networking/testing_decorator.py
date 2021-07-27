class Class1:
    def decorator(self):
        def wrapper():
            return function
        return wrapper

class Class2:
    def __init__(self) -> None:
        self.cl1 = Class1()
    
    @Class1.decorator()
    def square(self, x):
        return x**2

cl2 = Class2()
print(cl2.square(2))