#!/usr/bin/env python
import argparse
import tkinter as tk

import PIL.ImageTk
import PIL.Image


IMAGE_SIZE = (600, 400)


class ImageManipulationWindow:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.grid_columnconfigure(3, weight=1)

        self.image = PIL.Image.open(image_path).convert('L')

        self.label_original = tk.Label(self.root)
        self.label_original.grid(row=0, column=0, columnspan=4)

        self.label_modified = tk.Label(self.root)
        self.label_modified.grid(row=0, column=4)

        self.set_original_image(self.image)
        self.set_modified_image(self.image)

        self.setup_operation_controls()

    def setup_operation_controls(self):
        self.add_label = tk.Label(self.root, text='Add')
        self.add_label.grid(row=1, column=0, sticky='W')
        self.add_entry = tk.Entry(self.root)
        self.add_entry.grid(row=1, column=1, sticky='W')
        self.add_button = tk.Button(self.root, text='Perform',
                                    command=self.perform_addition)
        self.add_button.grid(row=1, column=2, sticky='W')

        self.multiply_label = tk.Label(self.root, text='Multiply')
        self.multiply_label.grid(row=2, column=0, sticky='W')
        self.multiply_entry = tk.Entry(self.root)
        self.multiply_entry.grid(row=2, column=1, sticky='W')
        self.multiply_button = tk.Button(self.root, text='Perform',
                                         command=self.perform_multiplication)
        self.multiply_button.grid(row=2, column=2, sticky='W')

        self.exponentiate_label = tk.Label(self.root, text='Exponentiate')
        self.exponentiate_label.grid(row=3, column=0, sticky='W')
        self.exponentiate_entry = tk.Entry(self.root)
        self.exponentiate_entry.grid(row=3, column=1, sticky='W')
        self.exponentiate_button = tk.Button(
            self.root, text='Perform', command=self.perform_exponentiation
        )
        self.exponentiate_button.grid(row=3, column=2, sticky='W')

        self.logarithm_label = tk.Label(self.root, text='Logarithm')
        self.logarithm_label.grid(row=4, column=0, sticky='W')
        self.logarithm_button = tk.Button(
            self.root, text='Perform', command=self.perform_logarithm
        )
        self.logarithm_button.grid(row=4, column=1, sticky='W')

        self.negation_label = tk.Label(self.root, text='Negate')
        self.negation_label.grid(row=5, column=0, sticky='W')
        self.negation_button = tk.Button(
            self.root, text='Perform', command=self.perform_negation
        )
        self.negation_button.grid(row=5, column=1, sticky='W')

        self.contrast_label = tk.Label(self.root, text='Contrast')
        self.contrast_label.grid(row=6, column=0, sticky='W')
        self.contrast_button = tk.Button(
            self.root, text='Perform', command=self.perform_contrasting
        )
        self.contrast_button.grid(row=6, column=1, sticky='W')

    def set_original_image(self, image):
        self._scaled_tk_image_original = PIL.ImageTk.PhotoImage(
            self.scale_image(image)
        )
        self.label_original.config(image=self._scaled_tk_image_original)

    def set_modified_image(self, image):
        self._scaled_tk_image_modified = PIL.ImageTk.PhotoImage(
            self.scale_image(image)
        )
        self.label_modified.config(image=self._scaled_tk_image_modified)

    def perform_addition(self):
        pass

    def perform_multiplication(self):
        pass

    def perform_exponentiation(self):
        pass

    def perform_logarithm(self):
        pass

    def perform_negation(self):
        pass

    def perform_contrasting(self):
        pass

    @staticmethod
    def scale_image(image):
        scaled_image = image.copy()
        scaled_image.thumbnail(IMAGE_SIZE)
        return scaled_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()

    window = ImageManipulationWindow(args.image_path)
    window.root.mainloop()


if __name__ == '__main__':
    main()
