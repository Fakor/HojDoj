#include <gtest/gtest.h>

#include "Box2D/Box2D.h"

#include "World.h"
#include "data_types.h"

#include <memory>

TEST(MotionTests, SetVelocity){
    hojdoj::World world;

    b2PolygonShape shape;
    shape.SetAsBox(10, 5);

    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 7;
    hojdoj::Time step_time = 1.0;

    world.create_object(index, position, {&shape});

    world.step(step_time);
    ASSERT_EQ(position, world[index].get_position());

    hojdoj::Vector velocity(1.5, -2);
    world[index].set_velocity(velocity);
    world.set_leash(index, 6.25);

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(1.5, -2), world[index].get_position());

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(3, -4), world[index].get_position());

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(3.75, -5), world[index].get_position());

    ASSERT_EQ(hojdoj::Vector(0, 0), world[index].get_velocity());

    world[index].set_velocity(velocity);
    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(5.25, -7), world[index].get_position());
}

TEST(MotionTests, SetForce){
    hojdoj::World world;

    b2PolygonShape shape;
    shape.SetAsBox(1, 2);

    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 5;
    hojdoj::Time step_time = 1.0;

    world.create_object(index, position, {&shape});

    ASSERT_EQ(world[index].get_mass(), 2.0);

    /*world[index].set_force({-0.4, 1.0});

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(-0.2, 0.5), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(-0.2, 0.5), world[index].get_velocity());

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(-0.6, 1.5), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(-0.4, 1), world[index].get_velocity());*/
}
