#ifndef HOJDOJ_IMAGE_H
#define HOJDOJ_IMAGE_H

#define MAGICKCORE_QUANTUM_DEPTH 16
#define MAGICKCORE_HDRI_ENABLE 1


#include "data_types.h"

#include "Magick++/Image.h"

namespace hojdoj {

class HojdojImage
{
    public:
        HojdojImage(const PixelVector& pixels, PixelSize p_size);
        virtual ~HojdojImage();

        PixelSize get_size() const;
        RGBAPixel get_pixel(uint16_t x, uint16_t y) const;
    protected:

    private:
        Magick::Image image_;
};

}

#endif // HOJDOJ_IMAGE_H
