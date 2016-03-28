#!/usr/bin/env python
import argparse
import tkinter as tk

import PIL.ImageTk
import PIL.Image


IMAGE_SIZE = (600, 400)


def get_scaled_image(image_path):
    image = PIL.Image.open(image_path)
    image.thumbnail(IMAGE_SIZE)
    return image


class RecolorWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()

        self.image = PIL.Image.open(image_path)

        self._original_tk_image = None
        self._result_tk_image = None

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

        self.range = tk.Scale(
            self.root, from_=0, to=255,
            orient=tk.HORIZONTAL, label='Range'
        )
        self.range.grid(row=2, column=0, sticky='nsew')

        self.button = tk.Button(self.root, text="Recolor", command=self.recolor)
        self.button.grid(row=3, column=0, sticky='nsew')

    def set_original_image(self, image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)

        self._original_tk_image = PIL.ImageTk.PhotoImage(scaled_image)
        self.label_original.config(image=self._original_tk_image)

    def set_result_image(self, image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)

        self._result_tk_image = PIL.ImageTk.PhotoImage(scaled_image)
        self.label_result.config(image=self._result_tk_image)

    def recolor(self):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    window = RecolorWindow(args.image_path)
    window.root.mainloop()


if __name__ == '__main__':
    main()
