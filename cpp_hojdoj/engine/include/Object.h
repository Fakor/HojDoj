#ifndef OBJECT_H
#define OBJECT_H

#include "Shape.h"
#include "Vector.h"
#include "data_types.h"

namespace hojdoj {

class Object
{
    public:
        Object(Shape* shape, Vector position);
        virtual ~Object();

        const Vector& get_position() const;
    private:
        Shape* shape_;
        Vector position_;
};

}

#endif // OBJECT_H
