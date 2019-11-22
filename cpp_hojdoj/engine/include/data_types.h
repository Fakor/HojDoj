#pragma once

#include <vector>
#include <iostream>

#include "Box2D/Box2D.h"

namespace hojdoj{

    const double EPSILON = 0.00001;

    struct PixelSize{
        size_t width;
        size_t height;
    };
    using PixelSize = struct PixelSize;

    using Index = unsigned int;
    using Coord = float32;

    using Time = float32;

    struct RGBAPixel{
        unsigned char R;
        unsigned char G;
        unsigned char B;
        unsigned char A;
    };
    using RGBAPixel = struct RGBAPixel;
    using PixelVector = std::vector<RGBAPixel>;

    bool operator==(const PixelSize& p1, const PixelSize& p2);
    bool operator!=(const RGBAPixel& p1, const RGBAPixel& p2);
    bool operator==(const RGBAPixel& p1, const RGBAPixel& p2);

    std::ostream& operator<<(std::ostream& os, const PixelSize& ps);
    std::ostream& operator<<(std::ostream& os, const RGBAPixel& ps);
}
