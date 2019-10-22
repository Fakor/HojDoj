#include "World.h"

namespace hojdoj {

World::World()
: world_{{0,0}}
{
    //ctor
}

World::~World()
{
    //dtor
}

void World::create_object(Shape* shape, const Vector& pos, Index ind){
    b2BodyDef body_def;
    body_def.type = b2_dynamicBody;
    body_def.position.Set(pos.x, pos.y);

    b2Body* body = world_.CreateBody(&body_def);

    objects_.emplace(ind, Object(body));

}

void World::step(Time step_time){
    int32 velocityIterations = 1;
    int32 positionIterations = 1;

    unsigned int full_steps = step_time/STEP_TIME;

    for(unsigned int i = 0; i < full_steps; ++i){
        world_.Step(STEP_TIME, velocityIterations, positionIterations);
    }

    Time last_step = step_time - full_steps * STEP_TIME;
    world_.Step(last_step, velocityIterations, positionIterations);
}

const Object& World::operator[](Index index) const{
    return objects_.at(index);
}

Object& World::operator[](Index index){
    return objects_.at(index);
}


} // hojdoj


