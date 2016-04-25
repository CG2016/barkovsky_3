#!/usr/bin/env python
import argparse
import statistics
import tkinter as tk

import numpy
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import PIL.ImageTk
import PIL.Image


IMAGE_SIZE = (600, 400)


class ColorStatsWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()

        self.image = PIL.Image.open(image_path).convert('RGB')

        self.label_original = tk.Label(self.root)
        self.label_original.grid(row=0, column=0)
        self.set_original_image(self.image)

        red_counts, green_counts, blue_counts = self.get_color_stats()
        red_mean = statistics.mean(self.get_values_from_counts(red_counts))
        green_mean = statistics.mean(self.get_values_from_counts(green_counts))
        blue_mean = statistics.mean(self.get_values_from_counts(blue_counts))
        print('red mean: %.2f' % red_mean)
        print('green mean: %.2f' % green_mean)
        print('blue mean: %.2f' % blue_mean)

        red_figure = self.draw_figure(red_counts, red_mean, 'r')
        green_figure = self.draw_figure(green_counts, green_mean, 'g')
        blue_figure = self.draw_figure(blue_counts, blue_mean, 'b')

        red_canvas = self.get_tk_canvas(red_figure)
        green_canvas = self.get_tk_canvas(green_figure)
        blue_canvas = self.get_tk_canvas(blue_figure)

        red_canvas.grid(row=0, column=1)
        green_canvas.grid(row=1, column=0)
        blue_canvas.grid(row=1, column=1)

    def set_original_image(self, image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)

        self._scaled_tk_image = PIL.ImageTk.PhotoImage(scaled_image)
        self.label_original.config(image=self._scaled_tk_image)

    def get_tk_canvas(self, figure):
        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.show()
        return canvas.get_tk_widget()

    def draw_figure(self, counts, mean, plot_color):
        figure = Figure(figsize=(8, 5.3333333), dpi=75)
        plot = figure.add_subplot(111)
        plot.set_xlim([0, 255])
        plot.plot(range(0, 256), counts, color=plot_color)
        plot.axvline(mean, color='purple')
        return figure

    def get_color_stats(self):
        width, height = self.image.width, self.image.height

        red_counts = [0] * 256
        green_counts = [0] * 256
        blue_counts = [0] * 256

        for i in range(width):
            for j in range(height):
                r, g, b = self.image.getpixel((i, j))
                red_counts[r] += 1
                green_counts[g] += 1
                blue_counts[b] += 1

        return red_counts, green_counts, blue_counts

    @staticmethod
    def get_values_from_counts(counts):
        values = []
        for v, count in enumerate(counts):
            values.extend([v] * count)
        return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    window = ColorStatsWindow(args.image_path)
    window.root.mainloop()


if __name__ == '__main__':
    main()
