from nio import Block, Signal
from nio.block.mixins import GroupBy
from nio.properties import Property, BoolProperty, FloatProperty, \
                           VersionProperty


class SimplifyPolyline(GroupBy, Block):

    version = VersionProperty('0.1.0')
    high_quality = BoolProperty(default=True, title='High Quality')
    tolerance = FloatProperty(default=0.1, title='Tolerance')
    x_attr = Property(default='{{ $x }}', title='X Attribute')
    y_attr = Property(default='{{ $y }}', title='Y Attribute')

    def process_group_signals(self, signals, group, input_id=None):
        points = []
        for signal in signals:
            point = {'x': self.x_attr(signal),
                     'y': self.y_attr(signal)}
            points.append(point)

        simplified = simplify(points, self.tolerance(), self.high_quality())

        outgoing_signals = []
        for result in simplified:
            signal_dict = {'x': result['x'],
                           'y': result['y'],
                           'group': group}
            outgoing_signals.append(Signal(signal_dict))

        return outgoing_signals


# Reference:
# https://github.com/omarestrella/simplify.py
def getSquareDistance(p1, p2):
    """
    Square distance between two points
    """
    dx = p1['x'] - p2['x']
    dy = p1['y'] - p2['y']

    return dx * dx + dy * dy


def getSquareSegmentDistance(p, p1, p2):
    """
    Square distance between point and a segment
    """
    x = p1['x']
    y = p1['y']

    dx = p2['x'] - x
    dy = p2['y'] - y

    if dx != 0 or dy != 0:
        t = ((p['x'] - x) * dx + (p['y'] - y) * dy) / (dx * dx + dy * dy)

        if t > 1:
            x = p2['x']
            y = p2['y']
        elif t > 0:
            x += dx * t
            y += dy * t

    dx = p['x'] - x
    dy = p['y'] - y

    return dx * dx + dy * dy


def simplifyRadialDistance(points, tolerance):
    length = len(points)
    prev_point = points[0]
    new_points = [prev_point]

    for i in range(length):
        point = points[i]

        if getSquareDistance(point, prev_point) > tolerance:
            new_points.append(point)
            prev_point = point

    if prev_point != point:
        new_points.append(point)

    return new_points


def simplifyDouglasPeucker(points, tolerance):
    length = len(points)
    markers = [0] * length  # Maybe not the most efficent way?

    first = 0
    last = length - 1

    first_stack = []
    last_stack = []

    new_points = []

    markers[first] = 1
    markers[last] = 1

    while last:
        max_sqdist = 0

        for i in range(first, last):
            sqdist = getSquareSegmentDistance(points[i], points[first], points[last])

            if sqdist > max_sqdist:
                index = i
                max_sqdist = sqdist

        if max_sqdist > tolerance:
            markers[index] = 1

            first_stack.append(first)
            last_stack.append(index)

            first_stack.append(index)
            last_stack.append(last)

        try:
            first = first_stack.pop()
        except IndexError:
            # first_stack is empty
            first = None

        try:
            last = last_stack.pop()
        except IndexError:
            last = None

    for i in range(length):
        if markers[i]:
            new_points.append(points[i])

    return new_points

def simplify(points, tolerance=0.1, highestQuality=True):
    sqtolerance = tolerance * tolerance

    if not highestQuality:
        points = simplifyRadialDistance(points, sqtolerance)

    points = simplifyDouglasPeucker(points, sqtolerance)

    return points

