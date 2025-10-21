from elliptic_curves.Point import Point
from finite_fields.FieldElement import FieldElement
from ECDSA.S256Point import S256Point
from ECDSA.spec256k1_constants import A, B, P, gx, gy, N


def generator_on_curve():
    print(gy**2 % P == (gx**3 + A * gx + B) % P)

def order_of_generator():
    x = FieldElement(gx, P)
    y = FieldElement(gy, P)
    a_fe = FieldElement(A, P)
    b_fe = FieldElement(B, P)
    G = Point(x, y, a_fe, b_fe)
    print(N * G)

def order_of_generator_2():
    G = S256Point(gx, gy)
    print(N * G)

def main():
    generator_on_curve()
    order_of_generator()
    order_of_generator_2()


if __name__ == "__main__":
    main()