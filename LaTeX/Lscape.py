## This is a simply file to add supporting classes for external latex packages using pylatex

# Pylatex libaries/base classes
import pylatex as pyl
import pylatex.base_classes as pylb

class Landscape(pylb.Environment):
    _latex_name = "landscape"
    packages = [pyl.Package("lscape")]