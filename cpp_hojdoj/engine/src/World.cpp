#include "World.h"

namespace hojdoj {

World::World()
{
    //ctor
}

World::~World()
{
    //dtor
}

void World::create_object(Shape* shape, const Vector& pos, Index ind){
    objects_.emplace(ind, Object(shape, pos));
}

void World::step(Time step_time){
}

const Vector& World::get_object_position(Index index) const{
    return objects_.at(index).get_position();
}

} // hojdoj

