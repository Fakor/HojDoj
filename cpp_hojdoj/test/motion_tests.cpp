#include <gtest/gtest.h>

#include "World.h"
#include "Square.h"
#include "data_types.h"

#include <memory>

TEST(MotionTests, SetVelocity){
    hojdoj::World world;

    hojdoj::Square square(10, 5);
    hojdoj::Position position{0, 0};
    hojdoj::Index index = 7;
    hojdoj::Time step_time = 1.0;

    world.create_object(&square, position, index);

    world.step(step_time);
    ASSERT_TRUE(hojdoj::compare_positon(position, world.get_object_position(index)));

    /*hojdoj::Velocity velocity(1.5, -2);
    world.SetMotion(velocity, index);
    world.StopAfterRange(6.25);

    world.Step(step_time);
    ASSERT_EQ(hojdoj::Position(1.5, -2), world.GetObjectPosition(index));

    world.Step(step_time);
    ASSERT_EQ(hojdoj::Position(3, -4), world.GetObjectPosition(index));

    world.Step(step_time);
    ASSERT_EQ(hojdoj::Position(3.75, -5), world.GetObjectPosition(index));*/
}
