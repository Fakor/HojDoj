#include <gtest/gtest.h>

#include "World.h"
#include "Square.h"
#include "data_types.h"

#include <memory>

TEST(MotionTests, SetVelocity){
    hojdoj::World world;

    hojdoj::Square square(10, 5);
    hojdoj::Vector position{0, 0};
    hojdoj::Index index = 7;
    hojdoj::Time step_time = 1.0;

    world.create_object(&square, position, index);

    world.step(step_time);
    ASSERT_EQ(position, world[index].get_position());

    hojdoj::Vector velocity(1.5, -2);
    world[index].set_velocity(velocity);
    world.set_object_max_range(index, 6.25);

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(1.5, -2), world[index].get_position());

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(3, -4), world[index].get_position());

    world.step(step_time);
    ASSERT_EQ(hojdoj::Vector(3.75, -5), world[index].get_position());
}
