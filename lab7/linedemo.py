#!/usr/bin/env python
import math
import tkinter as tk
import tkinter.messagebox


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
CANVAS_PADDING = 3
CANVAS_BORDER_SIZE = 1


class ClippingDemoWindow:
    def __init__(self):
        self.root = tk.Tk()

        self.main_canvas = tk.Canvas(self.root,
                                     width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.main_canvas.grid(row=0, column=0, rowspan=8)

        self.from_label = tk.Label(self.root, text='Upper left rectangle')
        self.from_label.grid(row=0, column=1)
        self.from_x_entry = tk.Entry(self.root)
        self.from_x_entry.insert(0, '100')
        self.from_x_entry.grid(row=0, column=2)
        self.from_y_entry = tk.Entry(self.root)
        self.from_y_entry.insert(0, '100')
        self.from_y_entry.grid(row=0, column=3)

        self.to_label = tk.Label(self.root, text='Lower right rectangle')
        self.to_label.grid(row=1, column=1)
        self.to_x_entry = tk.Entry(self.root)
        self.to_x_entry.insert(0, '400')
        self.to_x_entry.grid(row=1, column=2)
        self.to_y_entry = tk.Entry(self.root)
        self.to_y_entry.insert(0, '300')
        self.to_y_entry.grid(row=1, column=3)

        self.segment1_label = tk.Label(self.root, text='Segment point 1')
        self.segment1_label.grid(row=2, column=1)
        self.segment1_x = tk.Entry(self.root)
        self.segment1_x.insert(0, '100')
        self.segment1_x.grid(row=2, column=2)
        self.segment1_y = tk.Entry(self.root)
        self.segment1_y.insert(0, '5')
        self.segment1_y.grid(row=2, column=3)

        self.segment2_label = tk.Label(self.root, text='Segment point 2')
        self.segment2_label.grid(row=3, column=1)
        self.segment2_x = tk.Entry(self.root)
        self.segment2_x.insert(0, '500')
        self.segment2_x.grid(row=3, column=2)
        self.segment2_y = tk.Entry(self.root)
        self.segment2_y.insert(0, '350')
        self.segment2_y.grid(row=3, column=3)

        self.midpoint_button = tk.Button(
            self.root, text='Алгоритм средней точки',
            command=self.perform_midpoint
        )
        self.midpoint_button.grid(row=4, column=1, sticky='w', columnspan=3)
        self.barsky_button = tk.Button(
            self.root, text='Алгоритм Лианга-Барского',
            command=self.perform_barsky
        )
        self.barsky_button.grid(row=5, column=1, sticky='w', columnspan=3)
        self.polygon_button = tk.Button(
            self.root, text='Алгоритм отсечения выпуклого многоугольника',
            command=self.perform_polygon
        )
        self.polygon_button.grid(row=6, column=1, sticky='w', columnspan=3)
        self.root.grid_rowconfigure(7, weight=1)

        self.clear()

    def get_rectangle_points(self):
        from_x = int(self.from_x_entry.get())
        from_y = int(self.from_y_entry.get())
        to_x = int(self.to_x_entry.get())
        to_y = int(self.to_y_entry.get())
        return (from_x, from_y), (to_x, to_y)

    def get_segment_points(self):
        from_x = int(self.segment1_x.get())
        from_y = int(self.segment1_y.get())
        to_x = int(self.segment2_x.get())
        to_y = int(self.segment2_y.get())
        return (from_x, from_y), (to_x, to_y)

    def perform_midpoint(self):
        try:
            rect1, rect2 = self.get_rectangle_points()
            segm1, segm2 = self.get_segment_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

        self.clear()
        self.draw_rectangle(rect1, rect2)
        self.draw_segment(segm1, segm2)

        self.draw_midpoint(rect1, rect2, segm1, segm2)

    @classmethod
    def line_coeffs(cls, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])
        return A, B, -C

    @classmethod
    def intersection(cls, l1, l2):
        d = l1[0] * l2[1] - l1[1] * l2[0]
        dx = l1[2] * l2[1] - l1[1] * l2[2]
        dy = l1[0] * l2[2] - l1[2] * l2[0]
        if d != 0:
            x = dx / d
            y = dy / d
            return x, y
        else:
            return False

    @classmethod
    def intersects_rectangle(cls, rect1, rect2, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        rect1_x, rect1_y = rect1
        rect2_x, rect2_y = rect2

        int1 = cls.intersection(
            cls.line_coeffs((rect1_x, rect1_y), (rect2_x, rect1_y)),
            cls.line_coeffs(p1, p2)
        )
        int2 = cls.intersection(
            cls.line_coeffs((rect2_x, rect1_y), (rect2_x, rect2_y)),
            cls.line_coeffs(p1, p2)
        )
        int3 = cls.intersection(
            cls.line_coeffs((rect1_x, rect2_y), (rect2_x, rect2_y)),
            cls.line_coeffs(p1, p2)
        )
        int4 = cls.intersection(
            cls.line_coeffs((rect1_x, rect1_y), (rect1_x, rect2_y)),
            cls.line_coeffs(p1, p2)
        )
        return int1 or int2 or int3 or int4

    @staticmethod
    def distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def draw_midpoint(self, rect1, rect2, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        rect1_x, rect1_y = rect1
        rect2_x, rect2_y = rect2

        def point_inside(x, y):
            if x < rect1_x or x > rect2_x:
                return False
            if y < rect1_y or y > rect2_y:
                return False
            return True

        if self.distance(p1, p2) < 1:
            return

        inside1 = point_inside(x1, y1)
        inside2 = point_inside(x2, y2)
        if inside1 and inside2:
            self.draw_segment(p1, p2, color='red')

        if not inside1 and not inside2 and not self.intersects_rectangle(
                rect1, rect2, p1, p2):
            return

        self.draw_midpoint(rect1, rect2, p1, ((x1 + x2) / 2, (y1 + y2) / 2))
        self.draw_midpoint(rect1, rect2, ((x1 + x2) / 2, (y1 + y2) / 2), p2)

    def perform_barsky(self):
        try:
            rect1, rect2 = self.get_rectangle_points()
            segm1, segm2 = self.get_segment_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

        self.clear()
        self.draw_rectangle(rect1, rect2)
        self.draw_segment(segm1, segm2)

        pts = self.barsky_coords(rect1, rect2, segm1, segm2)
        if pts:
            self.draw_segment(pts[0], pts[1], color='red')

    def barsky_coords(self, rect1, rect2, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        rect1_x, rect1_y = rect1
        rect2_x, rect2_y = rect2

        p = [x1 - x2, x2 - x1, y1 - y2, y2 - y1]
        q = [x1 - rect1_x, rect2_x - x1, y1 - rect1_y, rect2_y - y1]
        u1 = -math.inf
        u2 = math.inf

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return False
            else:
                t = q[i] / p[i]
                if p[i] < 0 and u1 < t:
                    u1 = t
                elif p[i] > 0 and u2 > t:
                    u2 = t

        if u2 < u1:
            return []
        elif u1 < 0 < 1 < u2:
            return [p1, p2]
        elif 0 < u1 < u2 < 1:
            coll1 = (
                x1 + (x2 - x1) * u1,
                y1 + (y2 - y1) * u1
            )
            coll2 = (
                x1 + (x2 - x1) * u2,
                y1 + (y2 - y1) * u2
            )
            return [coll1, coll2]
        elif 0 < u1 < 1:
            coll1 = (
                x1 + (x2 - x1) * u1,
                y1 + (y2 - y1) * u1
            )
            return [coll1, p2]
        elif 0 < u2 < 1:
            coll2 = (
                x1 + (x2 - x1) * u2,
                y1 + (y2 - y1) * u2
            )
            return [p1, coll2]
        else:
            return []

    def perform_polygon(self):
        vertices = [
            (200, 50), (450, 200), (300, 350), (150, 250), (50, 50)
        ]

        try:
            rect1, rect2 = self.get_rectangle_points()
            segm1, segm2 = self.get_segment_points()
        except ValueError:
            tkinter.messagebox.showerror('Error', 'Invalid coordinates')
            return

        self.clear()
        self.draw_rectangle(rect1, rect2)
        self.draw_polygon_points(vertices)

        pass

    def draw_polygon_points(self, points):
        for p1, p2 in zip(points, points[1:] + [points[0]]):
            self.draw_segment(p1, p2)

    def draw_segment(self, point1, point2, color='black'):
        x1, y1 = point1
        x2, y2 = point2
        self.main_canvas.create_line(
            CANVAS_PADDING + x1, CANVAS_PADDING + y1,
            CANVAS_PADDING + x2, CANVAS_PADDING + y2,
            fill=color,
        )

    def draw_rectangle(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        self.main_canvas.create_rectangle(
            CANVAS_PADDING + x1, CANVAS_PADDING + y1,
            CANVAS_PADDING + x2, CANVAS_PADDING + y2,
            outline='black',
        )

    def clear(self):
        self.main_canvas.delete('all')
        self.draw_borders()

    def draw_borders(self):
        self.main_canvas.create_rectangle(
            CANVAS_PADDING, CANVAS_PADDING,
            CANVAS_WIDTH, CANVAS_HEIGHT,
            outline='grey'
        )


def main():
    window = ClippingDemoWindow()
    window.root.mainloop()


if __name__ == '__main__':
    main()
