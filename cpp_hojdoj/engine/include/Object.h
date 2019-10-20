#ifndef OBJECT_H
#define OBJECT_H

#include "Shape.h"
#include "data_types.h"

namespace hojdoj {

class Object
{
    public:
        Object(Shape* shape, Position position);
        virtual ~Object();

        const Position& get_position() const;
    private:
        Shape* shape_;
        Position position_;
};

}

#endif // OBJECT_H
