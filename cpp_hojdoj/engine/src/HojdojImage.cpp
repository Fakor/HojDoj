#include "HojdojImage.h"

namespace hojdoj {

HojdojImage::HojdojImage(const PixelVector& pixels, PixelSize p_size)
: image_{Magick::Geometry(p_size.width, p_size.height), Magick::Color(0,0,0,0)}
{
    Magick::Pixels view(image_);
    Magick::Quantum *view_pixels = view.get(0, 0, p_size.width, p_size.height);
    for(size_t i = 0; i < pixels.size(); ++i){
        *view_pixels++ = ToQuantum(pixels[i].R);
        *view_pixels++ = ToQuantum(pixels[i].G);
        *view_pixels++ = ToQuantum(pixels[i].B);
        *view_pixels++ = ToQuantum(pixels[i].A);
    }
}

HojdojImage::~HojdojImage()
{
    //dtor
}

PixelSize HojdojImage::get_size() const{
    return {image_.columns(),image_.rows()};
}

RGBAPixel HojdojImage::get_pixel(size_t x, size_t y){
    Magick::Color color = image_.pixelColor(x, y);
    return {FromQuantum(color.quantumRed()),
            FromQuantum(color.quantumGreen()),
            FromQuantum(color.quantumBlue()),
            FromQuantum(color.quantumAlpha())};
}


}
