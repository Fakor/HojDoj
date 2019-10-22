#include "Vector.h"

namespace hojdoj {

Vector::Vector(Coord init_x, Coord init_y)
: x{init_x}, y{init_y}
{
    //ctor
}

Vector::~Vector()
{
    //dtor
}

bool Vector::operator==(const Vector& other) const{
    double dx = x - other.x;
    double dy = y - other.y;
    return std::sqrt(dx*dx + dy*dy) < EPSILON;
}

std::ostream& operator<<(std::ostream& os, const Vector& v){
    os << "(" << v.x << ", " << v.y << ")";
    return os;
}

}
