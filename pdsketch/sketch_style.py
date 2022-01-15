import os
from ds2viz.styles import StyleSheet

dir_path = os.path.dirname(os.path.realpath(__file__))
sketch_style = StyleSheet.fromyaml(dir_path+"/sketch_stylesheet.yaml")