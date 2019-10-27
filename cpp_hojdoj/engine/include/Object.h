#ifndef OBJECT_H
#define OBJECT_H

#include "Box2D/Box2D.h"

#include <vector>

#include "Shape.h"
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

        b2Body* get_body();

        //void set_leash_objects(b2Body* anchor, b2RopeJoint* joint);

//        std::vector<b2Joint*> get_joints_for_termination();
//        void cleanup_temporary_joints();
    private:
        b2Body* body_;

//        b2Body* leash_anchor_;
//        b2RopeJoint* leash_joint_;
};

}

#endif // OBJECT_H
