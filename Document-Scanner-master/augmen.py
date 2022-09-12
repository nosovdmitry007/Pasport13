import Augmentor
p = Augmentor.Pipeline ("photo")
# Initialised with 100 images found in selected directory.
p.rotate(probability = 0.7, max_left_rotation= 5, max_right_rotation= 5)
# p.zoom(probability = 0.3, min_factor = 1.1, max_factor = 1.6)

p.sample(10)
