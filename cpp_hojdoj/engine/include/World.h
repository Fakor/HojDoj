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


class World
{
    public:
        World(float32 step_time);
        virtual ~World();

        void create_object(Index ind, const Vector& pos, std::vector<b2Shape*> shapes);
        void step(unsigned int nr_of_steps);

        const Object& operator[](Index index) const;
        Object& operator[](Index index);

        void set_global_gravity(float32 gravity_constant);
        void compute_gravity_forces();

        void set_leash(Index index, Coord range);
    private:
        b2World world_;
        float32 step_time_;

        bool global_gravity_{false};
        float32 G_;

        void clean_up_temporary_joints();

        std::map<Index, Object> objects_;

        std::vector<std::pair<b2RopeJoint*, b2Body*>> leash_constraints_;
};

}

#endif // WORLD_H
