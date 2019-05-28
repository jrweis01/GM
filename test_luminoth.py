import pytest
from local_luminoth import Perception

def test_analyze_image_fast():
    save = True
    images = [".\\GM\\Images\\traffic-843309_960_720.jpg"]
    my_luminoth = Perception(images, save, 'fast')
    objects = my_luminoth.run()
    assert objects

def test_analyze_image_accurate():
    save = True
    images = [".\\GM\\Images\\traffic-843309_960_720.jpg"]
    my_luminoth = Perception(images, save, 'accurate')
    objects = my_luminoth.run()
    assert objects