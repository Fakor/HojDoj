#include "Object.h"

namespace hojdoj {

Object::Object(Shape* shape, Position position)
:shape_{shape}, position_{position}
{
    //ctor
}

Object::~Object()
{
    //dtor
}

const Position& Object::get_position() const {
    return position_;
}

}
