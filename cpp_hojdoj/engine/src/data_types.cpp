#include "data_types.h"

namespace hojdoj{

bool operator==(const PixelSize& p1, const PixelSize& p2){
    //return false;
    return (p1.width == p2.width) &&
           (p1.height == p2.height);
}

std::ostream& operator<<(std::ostream& os, const PixelSize& ps){
    os << "(" << ps.width << "," << ps.height << ")";
    return os;
}

bool operator==(const RGBAPixel& p1, const RGBAPixel& p2){
    return (p1.R == p2.R) &&
           (p1.G == p2.G) &&
           (p1.B == p2.B) &&
           (p1.A == p2.A);
}


}
