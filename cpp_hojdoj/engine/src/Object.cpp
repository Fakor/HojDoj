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

void Object::apply_force(Vector force){
    body_->ApplyForceToCenter({force.x, force.y}, false);
}

float32 Object::get_mass() const {
    return body_->GetMass();
}

Vector Object::get_force() const {
    b2Vec2 force = body_->GetForce();
    return {force.x, force.y};
}

b2Body* Object::get_body(){
    return body_;
}

float32 Object::distance_to(Vector pos) const{
    float32 dx = body_->GetPosition().x - pos.x;
    float32 dy = body_->GetPosition().y - pos.y;
    return std::sqrt(dx*dx + dy*dy);
}

}
