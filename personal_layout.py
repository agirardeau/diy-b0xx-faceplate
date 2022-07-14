#!/usr/bin/env python3.9

from faceplate import *

WIDTH = 16
HEIGHT = 8
BORDER_WIDTH = 3/4

HAND_TILT = 25 

KEYCAP_LENGTH = 5/7  # 18.15mm, from spec (pretty close to 23/32" also)
KEYS_DEFAULT_MARGIN = 1/10
KEYS_DIST_DEFAULT = KEYCAP_LENGTH + KEYS_DEFAULT_MARGIN  # 13/16 almost exactly
KEYS_DIST_SHORT = KEYCAP_LENGTH + KEYS_DEFAULT_MARGIN / 2  # 3/4 + 1/64 almost exactly
KEYS_DIST_LONG = KEYCAP_LENGTH + KEYS_DEFAULT_MARGIN * 3 / 2

MIDDLE_FINGER_ELEVATION = 7/32
RING_FINGER_DECLINATION = 1/4
PINKY_DECLINATION = 1+1/16
CDOWN_DECLINATION = 3/8
CUP_VERTICAL_DISTANCE = KEYS_DIST_SHORT

EFFECTIVE_BORDER = BORDER_WIDTH + 9/16

if __name__ == '__main__':
    l_x = WIDTH / 2 - EFFECTIVE_BORDER - 3/8
    l_y = HEIGHT - EFFECTIVE_BORDER + 1/16 - max(
            (PINKY_DECLINATION - RING_FINGER_DECLINATION + KEYS_DIST_SHORT) * cosd(HAND_TILT) - KEYS_DIST_DEFAULT * sind(HAND_TILT),  # Ring Finger
            (PINKY_DECLINATION + KEYS_DIST_SHORT) * cosd(HAND_TILT) - 3 * KEYS_DIST_DEFAULT * sind(HAND_TILT))  # Index Finger

    # Right Hand
    l = KeyMount(l_x, l_y, HAND_TILT)
    z = l.translated(-KEYS_DIST_DEFAULT, PINKY_DECLINATION - RING_FINGER_DECLINATION)
    x = z.translated(-KEYS_DIST_DEFAULT, RING_FINGER_DECLINATION + MIDDLE_FINGER_ELEVATION)
    r = x.translated(-KEYS_DIST_DEFAULT, -MIDDLE_FINGER_ELEVATION)

    ls = l.translated(0, KEYS_DIST_SHORT)
    ms = z.translated(0, KEYS_DIST_SHORT)
    y = r.translated(0, KEYS_DIST_SHORT)
    b = r.translated(0, -KEYS_DIST_LONG)

    # Right Thumb
    a = r.translated(-(1+7/16), -(2+3/8))

    cu = a.translated(-1/4, KEYS_DIST_DEFAULT + 5/16)
    cl = cu.translated(-KEYS_DIST_DEFAULT, -5/16)
    cr = cu.translated(KEYS_DIST_SHORT, 0)

    a = a.rotated(14)
    cd = a.translated(-KEYS_DIST_DEFAULT, -3/16).rotated(14)

    # Left Hand
    rt = r.reflected_horizontal()
    dn = x.reflected_horizontal()
    lt = z.reflected_horizontal()
    up = l.reflected_horizontal()

    # Left Thumb
    mx = rt.translated((1+1/16), -(2+1/4))
    my = mx.translated(KEYS_DIST_SHORT, -3/8).rotated(-14)

    # D-pad
    du = KeyMount(-2.1, 5.5, -45)
    dl = du.translated(0, -(9/8) * KEYS_DIST_DEFAULT)
    dr = du.translated((9/8) * KEYS_DIST_DEFAULT, 0)
    dd = dl.translated((9/8) * KEYS_DIST_DEFAULT, 0)

    # Start
    s = KeyMount(-WIDTH/2 + BORDER_WIDTH + 9/16, HEIGHT - BORDER_WIDTH - 9/16)

    faceplate = Faceplate(
            WIDTH,
            HEIGHT,
            [
                up, dn, lt, rt, a, b, x, y, z, r, l, ls, ms, mx, my, cu, cd, cl, cr, du, dd, dl, dr, s
            ],
            mounting_hole_buffer = 1/4,
            mounting_hole_top_distance = 4.8
    )

    faceplate.to_svg('diyb0xx-personal')
    



