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

void Object::set_acceleration(Vector acceleration){
    body_->ApplyForceToCenter({acceleration.x, acceleration.y}, true);
}

float32 Object::get_mass() const {
    return body_->GetMass();
}

b2Body* Object::get_body(){
    return body_;
}

}
