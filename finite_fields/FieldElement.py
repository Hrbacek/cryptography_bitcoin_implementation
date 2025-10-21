
class FieldElement:
    def __init__(self, num: int, prime: int):
        self._check_num_range(num, prime)
        
        self.num = num
        self.prime = prime
    
    def __repr__(self) -> str:

        return "FieldElement_{}({})".format(self.prime, self.num)
    
    def __eq__(self, other) -> bool:
        if other is None:
            return False

        return (self.num == other.num) and (self.prime == other.prime)

    def __ne__(self, other):
        return not (self == other)
    
    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        
        num = (self.num + other.num) % self.prime

        return self.__class__(num, self.prime)
    
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        
        num = (self.num - other.num) % self.prime

        return self.__class__(num, self.prime)
    
    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        
        num = (self.num * other.num) % self.prime

        return self.__class__(num, self.prime)
    
    # This uses Fermats litttle theorem to reduce equivalent exponent
    def __pow__(self, exponent:int):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)

        return self.__class__(num, self.prime)

    # This operation uses fermats little theorem to calculate inverse
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")

        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)

    def _check_num_range(self, num: int, prime: int):
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(
                num, prime - 1
            )
            raise ValueError(error)
        