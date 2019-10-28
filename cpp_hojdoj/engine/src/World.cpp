#include "World.h"


namespace hojdoj {

World::World(float32 step_time)
: world_{{0,0}}, step_time_{step_time}
{
    world_.SetAutoClearForces(false);
}

World::~World()
{
    //dtor
}

void World::create_object(Index ind, const Vector& pos,std::vector<b2Shape*> shapes){
    b2BodyDef body_def;
    body_def.type = b2_dynamicBody;
    body_def.position.Set(pos.x, pos.y);

    b2Body* body = world_.CreateBody(&body_def);
    for(auto shape: shapes){
        b2FixtureDef fixture;
        fixture.shape = shape;
        fixture.density = 0.25f; // TODO: Figure out why this have to be set as 0.25
                                 // instead of 1 in order to get expected mass computation
                                 // at least thats what happens with box shapes.
        body->CreateFixture(&fixture);
    }
    objects_.emplace(ind, Object(body));
}

void World::step(unsigned int nr_of_steps){
    int32 velocityIterations = 1;
    int32 positionIterations = 1;

    for(unsigned int i = 0; i < nr_of_steps; ++i){
        world_.Step(step_time_, velocityIterations, positionIterations);
    }

    clean_up_temporary_joints();
}

const Object& World::operator[](Index index) const{
    return objects_.at(index);
}

Object& World::operator[](Index index){
    return objects_.at(index);
}

void World::set_leash(Index index, Coord range){
    Object& obj = this->operator[](index);
    Vector position = obj.get_position();

    b2BodyDef anchor_def;
    anchor_def.type = b2_staticBody;
    anchor_def.position.Set(position.x, position.y);

    b2Body* anchor = world_.CreateBody(&anchor_def);

    b2RopeJointDef rope_def;
    rope_def.bodyA = obj.get_body();
    rope_def.bodyB = anchor;
    rope_def.maxLength = range;
    rope_def.localAnchorA.Set(0,0);
    rope_def.localAnchorB.Set(0,0);

    b2RopeJoint* joint = (b2RopeJoint*)world_.CreateJoint(&rope_def);

    leash_constraints_.emplace_back(joint, anchor);
}


void World::clean_up_temporary_joints(){
    std::vector<std::pair<b2RopeJoint*, b2Body*>> updated_leashes;
    for(auto& leash: leash_constraints_){
        if(leash.first->GetLimitState() == b2LimitState::e_atUpperLimit){
            world_.DestroyJoint(leash.first);
            world_.DestroyBody(leash.second);
        }
        else {
            updated_leashes.push_back(leash);
        }
    }
    leash_constraints_ = updated_leashes;
}

} // hojdoj


