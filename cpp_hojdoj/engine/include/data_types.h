#pragma once

namespace hojdoj{

    const double EPSILON = 0.00001;

    using Size = unsigned int;
    using Index = unsigned int;
    using Coord = int;

    struct Position {
        Coord x;
        Coord y;
    };

    using Time = double;

    bool compare_positon(const Position& p1, const Position& p2);
}
