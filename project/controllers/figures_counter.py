import cv2
from .image_processing import *
from . import Figure

COLORS = ['blue', 'green', 'red']

class FigureCounter:
    def __init__(self):
        self.figures = []
    
    def find_figures(self, img):
        masks = []
        for color in COLORS:
            mask = color_filter(img, encode_color(color))
            masks.append(mask)
        masks.append(filter_yellow(img))
        total_mask = masks[0].copy()
        for mask in masks:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            total_mask = cv2.bitwise_or(total_mask, mask)
            contours = find_contours(mask)
            locations = get_locations(contours)
            for location, contour in zip(locations, contours):
                shape = find_shape(contour)
                if self.figures:
                    id_ = self.figures[-1].id + 1
                else:
                    id_ = 0
                figure = Figure(id_, location, shape, color)
                if not figure in self.figures:
                    self.figures.append(figure)
                else:
                    self.figures[self.figures.index(figure)].location = location
        self.sort_figures(total_mask)
        display_analysis(img, self.figures)
    
    def sort_figures(self, mask):
        contours = find_contours(mask)
        locations = get_locations(contours)
        for id_, location in enumerate(locations):
            figure = Figure(id_, location, None, None)
            self.figures[self.figures.index(figure)].id = id_