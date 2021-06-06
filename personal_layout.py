#!/usr/bin/env python3.9

from faceplate import *

WIDTH = 16
HEIGHT = 8
BORDER_WIDTH = 3/4

HAND_TILT = 15 
ADDITIONAL_THUMB_TILT = 15

KEYS_HORIZONTAL_DIST = 13/16
KEYS_VERTICAL_DIST = 13/16

MIDDLE_FINGER_ELEVATION = 7/32
PINKY_DECLINATION = 17/32
CDOWN_DECLINATION = 1/4
CUP_VERTICAL_DISTANCE = (9/8) * KEYS_VERTICAL_DIST

EFFECTIVE_BORDER = BORDER_WIDTH + (math.sqrt(2) * KEY_WIDTH * cosd(45 - HAND_TILT))
MAX_X = (WIDTH / 2) - EFFECTIVE_BORDER

if __name__ == '__main__':
    ms_y = HEIGHT - EFFECTIVE_BORDER - max(
            (PINKY_DECLINATION + KEYS_VERTICAL_DIST) * cosd(HAND_TILT) - KEYS_HORIZONTAL_DIST * sind(HAND_TILT),
            (PINKY_DECLINATION + 2 * KEYS_VERTICAL_DIST) * cosd(HAND_TILT) - 3 * KEYS_HORIZONTAL_DIST * sind(HAND_TILT))

    # Right Hand
    ms = KeyMount(MAX_X, ms_y, HAND_TILT)
    l = ms.translated(0, KEYS_VERTICAL_DIST)
    ls = ms.translated(-KEYS_HORIZONTAL_DIST, PINKY_DECLINATION)
    z = ls.translated(0, KEYS_VERTICAL_DIST)
    y = z.translated(-KEYS_HORIZONTAL_DIST, MIDDLE_FINGER_ELEVATION)
    b = ms.translated(-2 * KEYS_HORIZONTAL_DIST, 0)
    r = b.translated(0, KEYS_VERTICAL_DIST)
    x = r.translated(0, KEYS_VERTICAL_DIST)

    # Right Thumb
    a = y.translated(-(1+9/16), -(3+3/16)).rotated(ADDITIONAL_THUMB_TILT)
    cd = a.translated(-KEYS_HORIZONTAL_DIST, -CDOWN_DECLINATION)
    cl = cd.translated(0, CUP_VERTICAL_DISTANCE)
    cu = a.translated(0, CUP_VERTICAL_DISTANCE)
    cr = cl.translated(2 * KEYS_HORIZONTAL_DIST, 0)

    # Left Hand
    rt = r.reflected_horizontal()
    dn = y.reflected_horizontal()
    lt = z.reflected_horizontal()
    up = l.reflected_horizontal()

    # Left Thumb
    mx = a.reflected_horizontal()
    my = cd.reflected_horizontal()

    # D-pad
    du = KeyMount(0, HEIGHT - 1.5 * EFFECTIVE_BORDER)
    dd = du.translated(0, -1.25 * KEYS_VERTICAL_DIST)
    dr = dd.translated(1.25 * KEYS_HORIZONTAL_DIST, 0.625 * KEYS_VERTICAL_DIST)
    dl = dr.reflected_horizontal()

    du = KeyMount(-2.8, 5, -45)
    dl = du.translated(0, -(9/8) * KEYS_VERTICAL_DIST)
    dr = du.translated((9/8) * KEYS_HORIZONTAL_DIST, 0)
    dd = dl.translated((9/8) * KEYS_HORIZONTAL_DIST, 0)

    # Start
    s = KeyMount(-WIDTH/2 + BORDER_WIDTH + KEY_WIDTH/1.5, HEIGHT - BORDER_WIDTH - KEY_WIDTH/1.5)

    faceplate = Faceplate(WIDTH, HEIGHT, [
        up, dn, lt, rt, a, b, x, y, z, r, l, ls, ms, mx, my, cu, cd, cl, cr, du, dd, dl, dr, s
    ])

    faceplate.to_svg('diyb0xx-personal')

    



