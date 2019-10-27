#ifndef WORLD_H
#define WORLD_H

#include <map>
#include <vector>

#include "Box2D/Box2D.h"
#include "Box2D/Dynamics/Joints/b2Joint.h"

#include "Vector.h"
#include "Object.h"
#include "data_types.h"

namespace hojdoj {

const Time STEP_TIME=1.0/30;

class World
{
    public:
        World();
        virtual ~World();

        void create_object(Index ind, const Vector& pos, std::vector<b2Shape*> shapes);
        void step(Time step_time);

        const Object& operator[](Index index) const;
        Object& operator[](Index index);

        void set_leash(Index index, Coord range);
    private:
        void clean_up_temporary_joints();

        std::map<Index, Object> objects_;
        b2World world_;

        std::vector<std::pair<b2RopeJoint*, b2Body*>> leash_constraints_;
};

}

#endif // WORLD_H
