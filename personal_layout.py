#!/usr/bin/env python3.9

from faceplate import *

WIDTH = 16
HEIGHT = 8
BORDER_WIDTH = 3/4

HAND_TILT = 15 
ADDITIONAL_THUMB_TILT = 25

KEYCAP_LENGTH = 5/7 # 18.15mm, from spec
KEYS_HORIZONTAL_DIST = 13/16
KEYS_VERTICAL_DIST = 13/16
KEYS_VERTICAL_MARGIN = KEYS_VERTICAL_DIST - KEYCAP_LENGTH
KEYS_VERTICAL_DIST_SHORT = KEYS_VERTICAL_DIST - KEYS_VERTICAL_MARGIN * 2/3

MIDDLE_FINGER_ELEVATION = 7/32
RING_FINGER_DECLINATION = 1/8
PINKY_DECLINATION = 25/32
CDOWN_DECLINATION = 3/8
CUP_VERTICAL_DISTANCE = KEYS_VERTICAL_DIST

EFFECTIVE_BORDER = BORDER_WIDTH + 9/16

if __name__ == '__main__':
    l_x = WIDTH / 2 - EFFECTIVE_BORDER - 1/8
    l_y = HEIGHT - EFFECTIVE_BORDER + 1/16 - max(
            (PINKY_DECLINATION - RING_FINGER_DECLINATION + KEYS_VERTICAL_DIST_SHORT) * cosd(HAND_TILT) - KEYS_HORIZONTAL_DIST * sind(HAND_TILT),  # Ring Finger
            (PINKY_DECLINATION + KEYS_VERTICAL_DIST_SHORT) * cosd(HAND_TILT) - 3 * KEYS_HORIZONTAL_DIST * sind(HAND_TILT))  # Index Finger

    # Right Hand
    l = KeyMount(l_x, l_y, HAND_TILT)
    z = l.translated(-KEYS_HORIZONTAL_DIST, PINKY_DECLINATION - RING_FINGER_DECLINATION)
    x = z.translated(-KEYS_HORIZONTAL_DIST, RING_FINGER_DECLINATION + MIDDLE_FINGER_ELEVATION)
    r = x.translated(-KEYS_HORIZONTAL_DIST, -MIDDLE_FINGER_ELEVATION)

    ls = l.translated(0, KEYS_VERTICAL_DIST_SHORT)
    ms = z.translated(0, KEYS_VERTICAL_DIST_SHORT)
    y = r.translated(0, KEYS_VERTICAL_DIST_SHORT)
    b = r.translated(0, -KEYS_VERTICAL_DIST)

    # Right Thumb
    cu = x.translated(-(2+1/16), -(1+7/8)).rotated(ADDITIONAL_THUMB_TILT)
    cl = cu.translated(-KEYS_HORIZONTAL_DIST, 0)
    cr = cu.translated(KEYS_HORIZONTAL_DIST / 2, -KEYS_VERTICAL_DIST - 1.5 * KEYS_VERTICAL_MARGIN)
    cd = cl.translated(-KEYS_HORIZONTAL_DIST / 2, -KEYS_VERTICAL_DIST - 1.5 * KEYS_VERTICAL_MARGIN)
    a = cu.translated(-KEYS_HORIZONTAL_DIST / 2, -KEYS_VERTICAL_DIST - 1.5 * KEYS_VERTICAL_MARGIN)

    cu = cu.rotated(-24)
    cl = cl.rotated(-12)
    cr = cr.rotated(-12)
    cd = cd.rotated(12)

    # Left Hand
    rt = r.reflected_horizontal()
    dn = x.reflected_horizontal()
    lt = z.reflected_horizontal()
    up = l.reflected_horizontal()

    # Left Thumb
    mx = dn.translated((1+7/8), -(2+11/16))
    my = mx.translated(KEYS_HORIZONTAL_DIST - 1/16, -3/8).rotated(-14)

    # D-pad
    du = KeyMount(-2.3, 5.7, -45)
    dl = du.translated(0, -(9/8) * KEYS_VERTICAL_DIST)
    dr = du.translated((9/8) * KEYS_HORIZONTAL_DIST, 0)
    dd = dl.translated((9/8) * KEYS_HORIZONTAL_DIST, 0)

    # Start
    s = KeyMount(-WIDTH/2 + BORDER_WIDTH + KEY_WIDTH/1.5, HEIGHT - BORDER_WIDTH - 3/8)

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

    



