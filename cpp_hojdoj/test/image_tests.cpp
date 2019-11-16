#include <gtest/gtest.h>

#include <vector>

#include "data_types.h"
#include "HojdojImage.h"

TEST(ImageTest, Construct){
    hojdoj::RGBAPixel p00{0,1,2,3};
    hojdoj::RGBAPixel p01{10,11,12,13};
    hojdoj::RGBAPixel p02{20,21,22,23};
    hojdoj::RGBAPixel p10{30,31,32,33};
    hojdoj::RGBAPixel p11{40,41,42,43};
    hojdoj::RGBAPixel p12{50,51,52,53};

    hojdoj::PixelVector pixels{
        p00,
        p01,
        p02,
        p10,
        p11,
        p12,
    };

    hojdoj::PixelSize p_size{2,3};

    hojdoj::HojdojImage image{pixels, p_size};

    ASSERT_EQ(image.get_size(), p_size);
}
