SimplifyPolyline
===

Polyline simplification dramatically reduces the number of points in a polyline while retaining its shape, giving a huge performance boost when processing it and also reducing visual noise. Based on [simplify.js](http://mourner.github.io/simplify-js/).

Given a list of signals representing coordinates in 2D space, this block will produce a new list of signals representing the same coordinate space in fewer points. The degree of simplification can be configured, at the expense of processing time and loss of detail. When using **Group By** each group in the input signals will be simplified independently.

Properties
---
- **High Quality**: If True skip distance-based preprocessing, increasing quality and decreasing speed of execution.
- **Tolerance**: Higher numbers result in greater simplification at the cost of detail (fewer points in the result).
- **X Attribute**: The *x* coordinate of the incoming signals.
- **Y Attribute**: The *y* coordinate of the imcoming signals.

Commands
---
None
