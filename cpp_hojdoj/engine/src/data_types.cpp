#include "data_types.h"

#include <cmath>

namespace hojdoj {

    bool compare_positon(const Position& p1, const Position& p2){
        double dx = p1.x - p2.x;
        double dy = p1.y - p2.y;
        return std::sqrt(dx*dx + dy*dy) < EPSILON;
    }

}
