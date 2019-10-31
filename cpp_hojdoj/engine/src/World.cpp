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

void World::set_global_gravity(float32 gravity_constant){
    global_gravity_ = true;
    G_ = gravity_constant;
    compute_gravity_forces();
}

void World::compute_gravity_forces(){
    for(auto it1 = objects_.begin(); it1 != objects_.end(); ++it1){
        Object o1 = it1->second;

        auto it2 = it1;
        it2++;
        for(; it2 != objects_.end(); ++it2){
            Object o2 = it2->second;

            float32 r = o1.distance_to(o2.get_position());

            float32 F = G_*o1.get_mass()*o2.get_mass()/(r*r);

            float32 dx = o2.get_position().x-o1.get_position().x;
            float32 dy = o2.get_position().y-o1.get_position().y;

            float32 Fx = F*dx/r;
            float32 Fy = F*dy/r;
            o1.apply_force({Fx, Fy});
            o2.apply_force({-Fx, -Fy});
        }
    }
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


