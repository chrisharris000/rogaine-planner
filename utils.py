from dataclasses import dataclass

@dataclass
class PixelCoordinate:
    """
    x: x location pixel, 0 being left edge of pdf, positive rightwards
    y: y location of pixel, 0 being top edge of pdf, positive downwards
    """
    x: int
    y: int