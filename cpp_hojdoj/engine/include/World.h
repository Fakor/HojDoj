#ifndef WORLD_H
#define WORLD_H

#include <map>

#include "Box2D/Box2D.h"
#include "Shape.h"
#include "Object.h"
#include "data_types.h"

namespace hojdoj {

const Time STEP_TIME=1.0/30;

class World
{
    public:
        World();
        virtual ~World();

        void create_object(Shape* shape, const Vector& pos, Index index);
        void step(Time step_time);

        const Object& operator[](Index index) const;
        Object& operator[](Index index);
    private:
        std::map<Index, Object> objects_;
        b2World world_;
};

}

#endif // WORLD_H
