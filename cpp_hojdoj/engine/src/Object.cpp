#include "Object.h"

namespace hojdoj {

Object::Object(b2Body* body)
:body_{body}
{
}

Object::~Object()
{
    //dtor
}

Vector Object::get_position() const {
    return {body_->GetPosition().x, body_->GetPosition().y};
}

void Object::set_velocity(Vector velocity){
    body_->SetLinearVelocity({velocity.x, velocity.y});
}

Vector Object::get_velocity() const {
    return {body_->GetLinearVelocity().x, body_->GetLinearVelocity().y};
}


b2Body* Object::get_body(){
    return body_;
}

/*void Object::set_leash_objects(b2Body* anchor, b2RopeJoint* joint){
    leash_anchor_ = anchor;
    leash_joint_ = joint;
}

std::vector<b2Joint*> Object::get_joints_for_termination(){
    std::vector<b2Joint*> joints;
    if(leash_joint_ != NULL && leash_joint_->GetLimitState() == b2LimitState::e_atUpperLimit){
        joints.push_back(leash_joint_);
    }

    return joints;
}*/

}
