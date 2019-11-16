#include "HojdojImage.h"

namespace hojdoj {

HojdojImage::HojdojImage(const PixelVector& pixels, PixelSize p_size)
{
    image_.read(p_size.width, p_size.height, "RGBA", MagickCore::StorageType::CharPixel, &pixels);
}

HojdojImage::~HojdojImage()
{
    //dtor
}

PixelSize HojdojImage::get_size() const{
    return {image_.columns(),image_.rows()};
}

RGBAPixel HojdojImage::get_pixel(uint16_t x, uint16_t y) const{
    return {0,0,0,0};
}


}
