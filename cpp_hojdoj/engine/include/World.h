#ifndef WORLD_H
#define WORLD_H

#include <map>

#include "Box2D/Box2D.h"
#include "Box2D/Dynamics/Joints/b2RopeJoint.h"
#include "Box2D/Dynamics/Joints/b2Joint.h"

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

        void set_object_max_range(Index index, Coord range);

    private:
        std::map<Index, Object> objects_;
        std::map<Index, b2Body*> joint_objects_;
        std::map<Index, b2Joint*> joints_;
        b2World world_;

};

}

#endif // WORLD_H
