import math
import sys
from dataclasses import dataclass, field
import xml.etree.ElementTree as ET

# Coordinate system: X is right, Y is up, the origin is at the center of the
# bottom of the faceplate. Key rotation is zero for normal orientation, positive
# for leftward tilt and negative for rightward tilt.
# Units are inches and degrees.
# Translation to svg coordinates (X left, Y down) happens on export.

def sind(degrees):
    return math.sin(math.radians(degrees))

def cosd(degrees):
    return math.cos(math.radians(degrees))

def atand(ratio):
    return math.degrees(math.atan(ratio))

def mm2in(mm):
    return mm / 25.4

def str_dict(d):
    return {k: str(v) for k, v in d.items()}

KEY_WIDTH = mm2in(14)

DEFAULT_STYLE = 'fill:none;stroke:#000000;stroke-width:0.01'

@dataclass
class KeyMount:
    x: float = 0
    y: float = 0
    rotation: float = 0

    def reflected_horizontal(self):
        return KeyMount(-self.x, self.y, -self.rotation)

    def translated(self, dx, dy):
        # uses the key's reference frame, i.e. includes rotation
        new_x = self.x + dx * cosd(self.rotation) - dy * sind(self.rotation)
        new_y = self.y + dx * sind(self.rotation) + dy * cosd(self.rotation)
        return KeyMount(new_x, new_y, self.rotation)

    def rotated(self, degrees):
        return KeyMount(self.x, self.y, self.rotation + degrees)

    def to_svg(self):
        options = str_dict({
                'x': self.x - KEY_WIDTH/2,
                'y': self.y - KEY_WIDTH/2,
                'width': KEY_WIDTH,
                'height': KEY_WIDTH,
                'style': DEFAULT_STYLE})
        if self.rotation:
            options['transform'] = f'rotate({self.rotation} {self.x} {self.y})'
        return ET.Element('rect', options)


def inkscape_svgargs(width, height, units):
    return str_dict({
        'viewBox': f'{-width / 2} {-height} {width} {height}',
        'viewBox': f'{-width / 2} {-height} {width} {height}',
        'width': f'{width}{units}',
        'height': f'{height}{units}',
        'version': '1.1',
        'id': 'diyb0xx',
        'sodipodi:docname': 'diyb0xx.svg',
        'inkscape:version': '1.1 (c68e22c387, 2021-05-23)',
        'xmlns:inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'xmlns:sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink'})


def namedview_svgargs(width, height):
    return str_dict({
        'id': 'namedview43',
        'pagecolor': '#ffffff',
        'bordercolor': '#666666',
        'borderopacity': '1.0',
        'inkscape:pageshadow': '2',
        'inkscape:pageopacity': '0.0',
        'inkscape:pagecheckerboard': '0',
        'showgrid': 'false',
        'inkscape:zoom': 0.7,
        'inkscape:cx': width * 2 // 3,
        'inkscape:cy': height * 2 // 3,
        'inkscape:window-width': width + 2,
        'inkscape:window-height': height + 2,
        'inkscape:window-x': width / 2,
        'inkscape:window-y': height / 2,
        'inkscape:window-maximized': '1',
        'inkscape:current-layer': 'diyb0xx'})


@dataclass
class Faceplate:
    width: float
    height: float
    keymounts: list
    corner_rounding: float = 1/10
    include_mounting_holes: bool = True
    units: str = 'in'
    mounting_hole_diameter: float = (1/5) * 1.02  # 2% margin so post screws fit
    mounting_hole_buffer: float = 1/8             # distance from closest edge
    mounting_hole_elevation: float = 9/10         # side hole distance from top/bottom edge
    mounting_hole_top_distance: float = None      # distance between two top holes, if want two


    def to_svg(self, name):
        g = ET.Element('g', {'transform': 'scale(1 -1)'})

        g.append(ET.Element('rect', str_dict({
            'x': -self.width/2,
            'y': 0,
            'width': self.width,
            'height': self.height,
            'rx': self.corner_rounding,
            'style': DEFAULT_STYLE})))

        for keymount in self.keymounts:
            g.append(keymount.to_svg())

        if self.include_mounting_holes:
            for x, y in self.mounting_hole_locations():
                g.append(ET.Element('circle', str_dict({'cx': x, 'cy': y, 'r': self.mounting_hole_diameter / 2, 'style': DEFAULT_STYLE})))

        svg = ET.Element('svg', inkscape_svgargs(self.width, self.height, self.units))
        svg.append(ET.Element('sodipodi:namedview', namedview_svgargs(self.width, self.height)))
        svg.append(ET.Element('defs'))
        svg.append(g)

        if sys.version_info.minor >= 9:
            ET.indent(svg)

        doc = ET.ElementTree(svg)
        doc.write(f'{name}.svg', encoding='utf-8', xml_declaration=True)

    def mounting_hole_locations(self):
        dist_from_close_edge = self.mounting_hole_buffer + self.mounting_hole_diameter / 2
        dist_from_far_edge = self.mounting_hole_elevation + self.mounting_hole_buffer / 2

        holes = [
                (0, dist_from_close_edge),
                (self.width / 2 - dist_from_close_edge, dist_from_far_edge),
                (self.width / 2 - dist_from_close_edge, self.height - dist_from_far_edge),
                (-self.width / 2 + dist_from_close_edge, dist_from_far_edge),
                (-self.width / 2 + dist_from_close_edge, self.height - dist_from_far_edge),
        ]

        if self.mounting_hole_top_distance is not None:
            pass
            holes.extend([
                (-self.mounting_hole_top_distance / 2, self.height - dist_from_close_edge),
                (self.mounting_hole_top_distance / 2, self.height - dist_from_close_edge),
            ])
        else:
            holes.append((0, self.height - dist_from_close_edge))

        return holes
        







