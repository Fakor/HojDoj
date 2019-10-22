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

void Object::stop_after_range(Coord range){

}


}
