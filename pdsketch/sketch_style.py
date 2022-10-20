import os
from ds2viz.styles import StyleSheet
from ds2viz.default_styles import default_styles

dir_path = os.path.dirname(os.path.realpath(__file__))
sketch_stylesheet = StyleSheet.fromyaml(dir_path+"/sketch_stylesheet.yaml")
