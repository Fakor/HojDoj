#include <gtest/gtest.h>

#include "Box2D/Box2D.h"

#include "World.h"
#include "data_types.h"

#include <memory>

TEST(MotionTests, SetVelocity){
    hojdoj::World world(1/30.0);

    b2PolygonShape shape;
    shape.SetAsBox(10, 5);

    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 7;
    unsigned int step_time = 30;

    world.create_object(index, position, {&shape});

    ASSERT_NEAR(world[index].get_mass(), 50.0, 1e-7);

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

TEST(MotionTests, SetForceOneStep){
    float32 step_time = 1/60.0;
    hojdoj::World world(step_time);

    b2PolygonShape shape;
    shape.SetAsBox(0.1, 0.2);

    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 5;
    unsigned int steps = 1;

    world.create_object(index, position, {&shape});

    float32 expected_mass = 0.02;
    ASSERT_NEAR(world[index].get_mass(), expected_mass, 1e-7);

    hojdoj::Vector force{-0.2, 0.5};
    world[index].set_force(force);

    ASSERT_EQ(world[index].get_force(), force);

    world.step(steps);

    float32 t = step_time*steps;

    float32 expected_vel_x = force.x*t/expected_mass;
    float32 expected_vel_y = force.y*t/expected_mass;

    float32 expected_pos_x = force.x*t*t/(expected_mass*2) + expected_vel_x*step_time/2;
    float32 expected_pos_y = force.y*t*t/(expected_mass*2) + expected_vel_y*step_time/2;

    EXPECT_EQ(hojdoj::Vector(expected_pos_x, expected_pos_y), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(expected_vel_x, expected_vel_y), world[index].get_velocity());

    world.step(steps);

    t = 2*step_time*steps;

    expected_vel_x = force.x*t/expected_mass;
    expected_vel_y = force.y*t/expected_mass;

    expected_pos_x = force.x*t*t/(expected_mass*2) + expected_vel_x*step_time/2;
    expected_pos_y = force.y*t*t/(expected_mass*2) + expected_vel_y*step_time/2;

    EXPECT_EQ(hojdoj::Vector(expected_pos_x, expected_pos_y), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(expected_vel_x, expected_vel_y), world[index].get_velocity());
}


TEST(MotionTests, SetForceOneSecond){
    float32 step_time = 1/30.0;
    hojdoj::World world(step_time);

    b2PolygonShape shape;
    shape.SetAsBox(1, 2);

    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 5;
    unsigned int steps = 30;

    world.create_object(index, position, {&shape});

    float32 expected_mass = 2.0;
    ASSERT_NEAR(world[index].get_mass(), expected_mass, 1e-7);

    hojdoj::Vector force{-0.2, 0.5};
    world[index].set_force(force);

    world.step(steps);

    float32 t = step_time*steps;
    float32 expected_vel_x = force.x*t/expected_mass;
    float32 expected_vel_y = force.y*t/expected_mass;

    float32 expected_pos_x = force.x*t*t/expected_mass/2 + expected_vel_x*step_time/2;
    float32 expected_pos_y = force.y*t*t/expected_mass/2 + expected_vel_y*step_time/2;

    EXPECT_EQ(hojdoj::Vector(expected_pos_x, expected_pos_y), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(expected_vel_x, expected_vel_y), world[index].get_velocity());

    world.step(steps);

    t = 2*step_time*steps;

    expected_vel_x = force.x*t/expected_mass;
    expected_vel_y = force.y*t/expected_mass;

    expected_pos_x = force.x*t*t/expected_mass/2 + expected_vel_x*step_time/2;
    expected_pos_y = force.y*t*t/expected_mass/2 + expected_vel_y*step_time/2;

    EXPECT_EQ(hojdoj::Vector(expected_pos_x, expected_pos_y), world[index].get_position());
    ASSERT_EQ(hojdoj::Vector(expected_vel_x, expected_vel_y), world[index].get_velocity());
}

TEST(MotionTest, GravityTwoBodies){
    float32 step_time = 1/30.0;
    hojdoj::World world(step_time);

    hojdoj::Vector position1{0, 0};
    hojdoj::Index index1 = 0;
    b2PolygonShape shape1;
    shape1.SetAsBox(1, 2);

    world.create_object(index1, position1, {&shape1});

    hojdoj::Vector position2{20, 0};
    hojdoj::Index index2 = 1;
    b2PolygonShape shape2;
    shape2.SetAsBox(10, 2);

    world.create_object(index2, position2, {&shape2});

    float32 expected_mass1 = 2.0;
    float32 expected_mass2 = 20.0;

    ASSERT_NEAR(world[index1].get_mass(), expected_mass1, 1e-7);
    ASSERT_NEAR(world[index2].get_mass(), expected_mass2, 1e-7);

    world.set_global_gravity(0.3);

    hojdoj::Vector expected_force1{0.03, 0};
    hojdoj::Vector expected_force2{-0.03, 0};

    ASSERT_EQ(world[index1].get_force(), expected_force1);
    ASSERT_EQ(world[index2].get_force(), expected_force2);
}
