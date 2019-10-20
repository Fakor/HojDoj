#ifndef SQUARE_H
#define SQUARE_H

#include "data_types.h"
#include "Shape.h"

namespace hojdoj{

class Square: public Shape
{
    public:
        Square(Size width, Size height);
        virtual ~Square();

    protected:

    private:
    Size width_, height_;
};

}

#endif // SQUARE_H
