#ifndef OBJECT_H
#define OBJECT_H

#include "Box2D/Box2D.h"

#include <vector>

#include "Vector.h"
#include "data_types.h"

namespace hojdoj {

class Object
{
    public:
        Object(b2Body* body);
        virtual ~Object();

        Vector get_position() const;
        void set_velocity(Vector velocity);
        Vector get_velocity() const;
        void set_force(Vector force);
        float32 get_mass() const;

        b2Body* get_body();

    private:
        b2Body* body_;
};

}

#endif // OBJECT_H
