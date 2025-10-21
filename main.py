from elliptic_curves.Point import Point
from finite_fields.FieldElement import FieldElement

def main():
    n = 12
    p = 59
    a = FieldElement(n, p)
    one = FieldElement(1, p)
    print((827**2)%868)
    

if __name__ == "__main__":
    main()