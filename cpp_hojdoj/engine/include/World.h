#ifndef WORLD_H
#define WORLD_H

#include <map>

#include "Box2D/Box2D.h"
#include "Shape.h"
#include "Object.h"
#include "data_types.h"

namespace hojdoj {

class World
{
    public:
        World();
        virtual ~World();

        void create_object(Shape* shape, Position pos, Index index);
        void step(Time step_time);

        const Position& get_object_position(Index index) const;
    private:
        std::map<Index, Object> objects_;
};

}

#endif // WORLD_H
