#include "Object.h"

namespace hojdoj {

Object::Object(Shape* shape, Vector position)
:shape_{shape}, position_{position}
{
    //ctor
}

Object::~Object()
{
    //dtor
}

const Vector& Object::get_position() const {
    return position_;
}

}
