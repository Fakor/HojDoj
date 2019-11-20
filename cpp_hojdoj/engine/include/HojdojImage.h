#ifndef HOJDOJ_IMAGE_H
#define HOJDOJ_IMAGE_H

#define MAGICKCORE_QUANTUM_DEPTH 16
#define MAGICKCORE_HDRI_ENABLE 1


#include "data_types.h"

#include "Magick++/Image.h"
#include "Magick++/Geometry.h"
#include "Magick++/Pixels.h"

namespace hojdoj {

class HojdojImage
{
    public:
        HojdojImage(const PixelVector& pixels, PixelSize p_size);
        virtual ~HojdojImage();

        PixelSize get_size() const;
        RGBAPixel get_pixel(size_t x, size_t y);

        constexpr Magick::Quantum ToQuantum(char c) {return c*QuantumRange/256;}
        constexpr char FromQuantum(Magick::Quantum c) {return c*256/QuantumRange;}
    protected:

    private:
        Magick::Image image_;
};

}

#endif // HOJDOJ_IMAGE_H
