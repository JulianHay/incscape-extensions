import inkex

class DuplicateAndTransform(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--transformation_center", type=str, default="c", help="Transformation center")
        pars.add_argument("--rotate_around", type=str, default="duplicate", help="Rotation center")
        pars.add_argument("--scale", type=float, default=1.0, help="Scaling factor")
        pars.add_argument("--rotate", type=float, default=0, help="Rotation angle (degrees)")
        pars.add_argument("--translate_x", type=float, default=0, help="Translation X")
        pars.add_argument("--translate_y", type=float, default=0, help="Translation Y")
        pars.add_argument("--skew_x", type=float, default=0, help="Skew X angle (degrees)")
        pars.add_argument("--skew_y", type=float, default=0, help="Skew Y angle (degrees)")
        pars.add_argument("--iterations", type=int, default=10, help="Number of iterations")
        pars.add_argument("--scale_stroke", type=inkex.Boolean, default=False, help="Scale Stroke Width with Object")

    def get_transform_center(self, obj, transformation_center):
        bbox = obj.bounding_box()
        if bbox is None:
            return inkex.Vector2d(0, 0)

        # Define a mapping for transformation_center options to corresponding bbox points
        center_points = {
            'c': bbox.center,
            'nw': inkex.Vector2d(bbox.left, bbox.top),
            'ne': inkex.Vector2d(bbox.right, bbox.top),
            'sw': inkex.Vector2d(bbox.left, bbox.bottom),
            'se': inkex.Vector2d(bbox.right, bbox.bottom),
            'n': inkex.Vector2d(bbox.center_x, bbox.top),
            's': inkex.Vector2d(bbox.center_x, bbox.bottom),
            'e': inkex.Vector2d(bbox.right, bbox.center_y),
            'w': inkex.Vector2d(bbox.left, bbox.center_y)
        }

        return center_points.get(transformation_center, bbox.center)

    def effect(self):
        for elem in self.svg.selected.values():
            document = elem.getparent()
            original_transform = elem.transform

            # Define the center point for rotation and scaling
            transformation_center = self.get_transform_center(elem, self.options.transformation_center)

            # Store the original stroke width
            original_stroke_width = float(elem.style.get('stroke-width', '1'))

            for i in range(self.options.iterations):
                # Create a fresh duplicate from the original element
                duplicate = elem.duplicate()

                # Reset to original transform for each new duplicate
                duplicate.transform = original_transform

                # Initialize a composite transformation for this iteration
                composite_transform = inkex.Transform()

                # Apply scale transformation without compounding
                if self.options.scale != 1:
                    scale_transform = inkex.Transform()
                    scale_factor = self.options.scale ** (i + 1)
                    scale_transform.add_translate(transformation_center)
                    scale_transform.add_scale(scale_factor, scale_factor)
                    scale_transform.add_translate(-transformation_center)
                    composite_transform = composite_transform @ scale_transform

                    # Conditionally scale the stroke width
                    if not self.options.scale_stroke:
                        duplicate.style['stroke-width'] = str(original_stroke_width / scale_factor)  # Reset to original width
                    else:
                        duplicate.style['stroke-width'] = str(original_stroke_width)  # Scaled width

                # Apply rotation transformation around the transformation_center, with incremental rotation
                if self.options.rotate != 0:
                    rotate_transform = inkex.Transform()
                    if self.options.rotate_around == 'original':
                        rotate_transform.add_rotate(self.options.rotate * (i + 1), transformation_center.x, transformation_center.y)
                    elif self.options.rotate_around == 'duplicate':
                        rotate_transform.add_rotate(self.options.rotate * (i + 1),
                                                transformation_center.x + self.options.translate_x * (i + 1),
                                                transformation_center.y + self.options.translate_y * (i + 1))
                    composite_transform = composite_transform @ rotate_transform

                # Apply skew transformation around the transformation_center
                if self.options.skew_x != 0 or self.options.skew_y != 0:
                    skew_transform = inkex.Transform()
                    skew_transform.add_translate(transformation_center)
                    skew_transform.add_skewx(self.options.skew_x * (i + 1))
                    skew_transform.add_skewy(self.options.skew_y * (i + 1))
                    skew_transform.add_translate(-transformation_center)
                    composite_transform = composite_transform @ skew_transform

                # Apply translation in the same direction each time (linear)
                if self.options.translate_x != 0 or self.options.translate_y != 0:
                    translate_transform = inkex.Transform()
                    translate_transform.add_translate(self.options.translate_x * (i + 1),
                                                      self.options.translate_y * (i + 1))
                    composite_transform = composite_transform @ translate_transform

                # Apply the composite transformation to the duplicate
                duplicate.transform = composite_transform

                # Append the duplicate to the SVG document
                document.append(duplicate)

# Run the extension
if __name__ == "__main__":
    DuplicateAndTransform().run()