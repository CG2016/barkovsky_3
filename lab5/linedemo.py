#!/usr/bin/env python
import tkinter as tk
import tkinter.messagebox


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300
CANVAS_PADDING = 3
CANVAS_BORDER_SIZE = 1

ZOOM_CELL_SIZE = 10
ZOOM_CELL_WIDTH = (CANVAS_WIDTH - CANVAS_PADDING - CANVAS_BORDER_SIZE) // \
                  (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE)
ZOOM_CELL_HEIGHT = (CANVAS_HEIGHT - CANVAS_PADDING - CANVAS_BORDER_SIZE) // \
                   (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE)


class LineDemoWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.main_canvas = tk.Canvas(self.root,
                                     width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.main_canvas.grid(row=0, column=0, rowspan=7)
        self.zoom_canvas = tk.Canvas(self.root,
                                     width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.zoom_canvas.grid(row=7, column=0)

        self.from_label = tk.Label(self.root, text='From')
        self.from_label.grid(row=0, column=1)
        self.from_x_entry = tk.Entry(self.root)
        self.from_x_entry.insert(0, '5')
        self.from_x_entry.grid(row=0, column=2)
        self.from_y_entry = tk.Entry(self.root)
        self.from_y_entry.insert(0, '5')
        self.from_y_entry.grid(row=0, column=3)

        self.to_label = tk.Label(self.root, text='To')
        self.to_label.grid(row=1, column=1)
        self.to_x_entry = tk.Entry(self.root)
        self.to_x_entry.insert(0, '30')
        self.to_x_entry.grid(row=1, column=2)
        self.to_y_entry = tk.Entry(self.root)
        self.to_y_entry.insert(0, '20')
        self.to_y_entry.grid(row=1, column=3)

        self.step_button = tk.Button(
            self.root, text='Пошаговый алгоритм',
            command=self.draw_step
        )
        self.step_button.grid(row=2, column=1, sticky='w', columnspan=3)
        self.dda_button = tk.Button(
            self.root, text='Алгоритм ЦДА',
            command=self.draw_dda
        )
        self.dda_button.grid(row=3, column=1, sticky='w', columnspan=3)
        self.bresenham_button = tk.Button(
            self.root, text='Алгоритм Брезенхема',
            command=self.draw_bresenham
        )
        self.bresenham_button.grid(row=4, column=1, sticky='w', columnspan=3)
        self.bresenham_circle_button = tk.Button(
            self.root, text='Алгоритм Брезенхема (окружность)',
            command=self.draw_bresenham_circle
        )
        self.bresenham_circle_button.grid(row=5, column=1, sticky='w',
                                          columnspan=3)
        self.root.grid_rowconfigure(6, weight=1)

        self.clear()
        self.draw_pixel(0, 0)

    def get_points(self):
        from_x = int(self.from_x_entry.get())
        from_y = int(self.from_y_entry.get())
        to_x = int(self.to_x_entry.get())
        to_y = int(self.to_y_entry.get())
        return (from_x, from_y), (to_x, to_y)

    def draw_step(self):
        try:
            (from_x, from_y), (to_x, to_y) = self.get_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

    def draw_dda(self):
        try:
            (from_x, from_y), (to_x, to_y) = self.get_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

    def draw_bresenham(self):
        try:
            (from_x, from_y), (to_x, to_y) = self.get_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

    def draw_bresenham_circle(self):
        try:
            (from_x, from_y), (to_x, to_y) = self.get_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

    def clear(self):
        self.main_canvas.delete('all')
        self.zoom_canvas.delete('all')
        self.draw_borders()

    def draw_pixel(self, x, y):
        if x < 0 or x > CANVAS_WIDTH or y < 0 or y > CANVAS_HEIGHT:
            return

        self.main_canvas.create_rectangle(
            x + CANVAS_PADDING + CANVAS_BORDER_SIZE,
            y + CANVAS_PADDING + CANVAS_BORDER_SIZE,
            x + CANVAS_PADDING + CANVAS_BORDER_SIZE,
            y + CANVAS_PADDING + CANVAS_BORDER_SIZE,
        )

        if x > ZOOM_CELL_WIDTH or y > ZOOM_CELL_HEIGHT:
            return

        zoom_x0 = (
            x * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + CANVAS_BORDER_SIZE +
            CANVAS_PADDING
        )
        zoom_x1 = zoom_x0 + ZOOM_CELL_SIZE - 1
        zoom_y0 = (
            y * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + CANVAS_BORDER_SIZE +
            CANVAS_PADDING
        )
        zoom_y1 = zoom_y0 + ZOOM_CELL_SIZE - 1
        self.zoom_canvas.create_rectangle(zoom_x0, zoom_y0, zoom_x1, zoom_y1,
                                          fill='black')

    def draw_borders(self):
        self.main_canvas.create_rectangle(
            CANVAS_PADDING, CANVAS_PADDING,
            CANVAS_WIDTH, CANVAS_HEIGHT,
            outline='grey'
        )
        self.main_canvas.create_rectangle(
            CANVAS_PADDING + CANVAS_BORDER_SIZE,
            CANVAS_PADDING + CANVAS_BORDER_SIZE,
            CANVAS_PADDING + CANVAS_BORDER_SIZE + ZOOM_CELL_WIDTH,
            CANVAS_PADDING + CANVAS_BORDER_SIZE + ZOOM_CELL_HEIGHT,
            fill='#EEEEEE', outline='#EEEEEE',
        )

        max_y = ZOOM_CELL_HEIGHT * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + \
                CANVAS_PADDING
        for i in range(0, ZOOM_CELL_WIDTH + 1):
            x = i * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + CANVAS_PADDING
            self.zoom_canvas.create_line(x, 0, x, max_y, fill='gray')

        max_x = ZOOM_CELL_WIDTH * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + \
                CANVAS_PADDING
        for j in range(0, ZOOM_CELL_HEIGHT + 1):
            y = j * (ZOOM_CELL_SIZE + CANVAS_BORDER_SIZE) + CANVAS_PADDING
            self.zoom_canvas.create_line(0, y, max_x, y, fill='gray')


def main():
    window = LineDemoWindow()
    window.root.mainloop()


if __name__ == '__main__':
    main()
