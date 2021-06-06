#!/usr/bin/env python3.9

from faceplate import *

WIDTH = 16
HEIGHT = 8

INDEXF_X = 3.111
INDEXF_Y = 5.268

MIDDLEF_HORIZ_OFFSET = 1.035
RINGF_HORIZ_OFFSET = 1.126
PINKY_HORIZ_OFFSET = 1.032

MIDDLEF_VERT_OFFSET = 0.472
RINGF_VERT_OFFSET = -0.127
PINKY_VERT_OFFSET = -0.626

SECOND_ROW_VERT_OFFSET = 0.852

A_BUTTON_X = 2.272
A_BUTTON_Y = 2.638

C_HORIZ_OFFSET = 0.749
C_DOWN_VERT_OFFSET = -0.524
C_LEFTUPRIGHT_VERT_OFFSET = 1.049

START_Y = 5.056
HOME_SELECT_HORIZ_OFFSET = 0.852

if __name__ == '__main__':

    # Right Hand
    b = KeyMount(INDEXF_X, INDEXF_Y)
    x = b.translated(MIDDLEF_HORIZ_OFFSET, MIDDLEF_VERT_OFFSET)
    z = x.translated(RINGF_HORIZ_OFFSET, RINGF_VERT_OFFSET)
    up = z.translated(PINKY_HORIZ_OFFSET, PINKY_VERT_OFFSET)
    r = b.translated(0, SECOND_ROW_VERT_OFFSET)
    y = x.translated(0, SECOND_ROW_VERT_OFFSET)
    ls = z.translated(0, SECOND_ROW_VERT_OFFSET)
    ms = up.translated(0, SECOND_ROW_VERT_OFFSET)

    # Right Thumb
    a = KeyMount(A_BUTTON_X, A_BUTTON_Y)
    cd = a.translated(-C_HORIZ_OFFSET, C_DOWN_VERT_OFFSET)
    cl = cd.translated(0, C_LEFTUPRIGHT_VERT_OFFSET)
    cu = a.translated(0, C_LEFTUPRIGHT_VERT_OFFSET)
    cr = cl.translated(2 * C_HORIZ_OFFSET, 0)

    # Left Hand
    l = up.reflected_horizontal()
    lt = z.reflected_horizontal()
    dn = x.reflected_horizontal()
    rt = b.reflected_horizontal()

    # Left Thumb
    mx = a.reflected_horizontal()
    my = cd.reflected_horizontal()

    # Center Buttons
    s = KeyMount(0, START_Y)
    sel = s.translated(HOME_SELECT_HORIZ_OFFSET, 0)
    hom = sel.reflected_horizontal()

    faceplate = Faceplate(WIDTH, HEIGHT, [
        up, dn, lt, rt, a, b, x, y, z, r, l, ls, ms, mx, my, cu, cd, cl, cr, s, hom, sel
    ])

    faceplate.to_svg('diyb0xx-default')
