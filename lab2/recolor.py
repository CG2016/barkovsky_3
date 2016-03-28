#!/usr/bin/env python
import argparse
import tkinter as tk
import math

import numpy
import PIL.ImageTk
import PIL.Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


IMAGE_SIZE = (600, 400)


def cap_number(number, min_, max_):
    if number < min_:
        return min_
    elif number > max_:
        return max_
    else:
        return number


class RecolorWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()

        self.image = PIL.Image.open(image_path)

        self._original_tk_image = None
        self._result_tk_image = None

        self._from_lab = None
        self._to_lab = None

        self.label_original = tk.Label(self.root)
        self.label_original.grid(row=0, column=0, columnspan=3)
        self.set_original_image(self.image)

        self.label_result = tk.Label(self.root)
        self.label_result.grid(row=0, column=3, columnspan=3)
        self.set_result_image(self.image)

        self.from_r_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='From red'
        )
        self.from_r_scale.grid(row=1, column=0, sticky='nsew')

        self.from_g_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='From green'
        )
        self.from_g_scale.grid(row=1, column=1, sticky='nsew')

        self.from_b_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='From blue'
        )
        self.from_b_scale.grid(row=1, column=2, sticky='nsew')

        self.to_r_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='To red'
        )
        self.to_r_scale.grid(row=1, column=3, sticky='nsew')

        self.to_g_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='To green'
        )
        self.to_g_scale.grid(row=1, column=4, sticky='nsew')

        self.to_b_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='To blue'
        )
        self.to_b_scale.grid(row=1, column=5, sticky='nsew')

        self.range_scale = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='Range'
        )
        self.range_scale.grid(row=2, column=0, sticky='nsew')

        self.button = tk.Button(self.root, text="Recolor", command=self.recolor)
        self.button.grid(row=3, column=0, sticky='nsew')

    def set_original_image(self, image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)

        self.image = scaled_image
        self._original_tk_image = PIL.ImageTk.PhotoImage(scaled_image)
        self.label_original.config(image=self._original_tk_image)

    def set_result_image(self, image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)

        self._result_tk_image = PIL.ImageTk.PhotoImage(scaled_image)
        self.label_result.config(image=self._result_tk_image)

    @property
    def from_color(self):
        red = self.from_r_scale.get()
        green = self.from_g_scale.get()
        blue = self.from_b_scale.get()
        return (red, green, blue)

    @property
    def to_color(self):
        red = self.to_r_scale.get()
        green = self.to_g_scale.get()
        blue = self.to_b_scale.get()
        return (red, green, blue)

    @property
    def range(self):
        return self.range_scale.get()

    def recolor(self):
        self._from_lab = convert_color(sRGBColor(*self.from_color), LabColor)
        self._to_lab = convert_color(sRGBColor(*self.to_color), LabColor)
        range_ = self.range
        from_r, from_g, from_b = self.from_color
        to_r, to_g, to_b = self.to_color

        width, height = self.image.width, self.image.height
        pixel_count = width * height
        source_pixels = numpy.asarray(self.image)

        result_image = PIL.Image.new('RGB', (width, height), "black")
        target_pixels = result_image.load()

        pixels_done = 0
        for i in range(width):
            for j in range(height):
                r, g, b = source_pixels[j, i]

                distance = math.sqrt(
                    (r - from_r) ** 2 +
                    (g - from_g) ** 2 +
                    (b - from_b) ** 2
                )

                pixels_done += 1
                if pixels_done % 10000 == 0:
                    print('%d%%' % (pixels_done / pixel_count * 100))

                if distance > range_:
                    target_pixels[i, j] = (r, g, b)
                    continue

                r_diff = r - from_r
                g_diff = g - from_g
                b_diff = b - from_b

                r_new = cap_number(to_r + r_diff, 0, 255)
                g_new = cap_number(to_g + g_diff, 0, 255)
                b_new = cap_number(to_b + b_diff, 0, 255)
                target_pixels[i, j] = (
                    int(r_new), int(g_new), int(b_new)
                )

        self.set_result_image(result_image)

    def _calc_color(self, source_color):
        r, g, b = source_color
        delta_e = delta_e_cie2000(
            self._from_lab,
            convert_color(sRGBColor(r, g, b), LabColor),
        )

        if delta_e > self.range:
            return tuple(source_color)

        source_lab = convert_color(sRGBColor(r, g, b), LabColor)
        l_diff = source_lab.lab_l - self._from_lab.lab_l
        a_diff = source_lab.lab_a - self._from_lab.lab_a
        b_diff = source_lab.lab_b - self._from_lab.lab_b

        l_new = cap_number(self._to_lab.lab_l + l_diff, 0, 100)
        a_new = cap_number(self._to_lab.lab_a + a_diff, -128, 128)
        b_new = cap_number(self._to_lab.lab_b + b_diff, -128, 128)
        srgb = convert_color(LabColor(l_new, a_new, b_new), sRGBColor)
        return (srgb.rgb_r, srgb.rgb_g, srgb.rgb.b)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    window = RecolorWindow(args.image_path)
    window.root.mainloop()


if __name__ == '__main__':
    main()
