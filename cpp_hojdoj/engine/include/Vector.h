#ifndef VECTOR_H
#define VECTOR_H

#include <cmath>

#include "data_types.h"

namespace hojdoj {

class Vector
{
    public:
        Vector(Coord init_x, Coord init_y);
        virtual ~Vector();

        bool operator==(const Vector& other) const;

        Coord x, y;
};

}

#endif // VECTOR_H
