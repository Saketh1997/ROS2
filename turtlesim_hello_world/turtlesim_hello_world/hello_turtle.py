import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import math

LETTERS = {
    'H': [
        [(1.0, 2.0), (1.0, 4.0)],
        [(1.0, 3.0), (1.6, 3.0)],
        [(1.6, 2.0), (1.6, 4.0)],
    ],
    'E': [
        [(0.0, 2.0), (0.0, 4.0)],
        [(0.0, 4.0), (0.6, 4.0)],
        [(0.0, 3.0), (0.5, 3.0)],
        [(0.0, 2.0), (0.6, 2.0)],
    ],
    'L': [
        [(0.0, 2.0), (0.0, 4.0)],
        [(0.0, 2.0), (0.6, 2.0)],
    ],
    'O': [
        [(0.0, 2.0), (0.0, 4.0)],
        [(0.0, 4.0), (0.6, 4.0)],
        [(0.6, 4.0), (0.6, 2.0)],
        [(0.6, 2.0), (0.0, 2.0)],
    ],
    'W': [
        [(0.0, 4.0), (0.15, 2.0)],
        [(0.15, 2.0), (0.3, 3.2)],
        [(0.3, 3.2), (0.45, 2.0)],
        [(0.45, 2.0), (0.6, 4.0)],
    ],
    'R': [
        [(0.0, 2.0), (0.0, 4.0)],
        [(0.0, 4.0), (0.5, 4.0)],
        [(0.5, 4.0), (0.5, 3.0)],
        [(0.5, 3.0), (0.0, 3.0)],
        [(0.0, 3.0), (0.5, 2.0)],
    ],
    'D': [
        [(0.0, 2.0), (0.0, 4.0)],
        [(0.0, 4.0), (0.4, 3.8)],
        [(0.4, 3.8), (0.6, 3.2)],
        [(0.6, 3.2), (0.6, 2.8)],
        [(0.6, 2.8), (0.4, 2.2)],
        [(0.4, 2.2), (0.0, 2.0)],
    ],
}

STEPS = 20

class HelloWorldDrawer(Node):
    def __init__(self):
        super().__init__('hello_world_drawer')

        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.set_pen  = self.create_client(SetPen,           '/turtle1/set_pen')

        for svc in (self.teleport, self.set_pen):
            svc.wait_for_service(timeout_sec=5.0)

        # "Hello World" — letter : x offset pairs
        sequence = [
            ('H', 0.0),
            ('E', 1.9),
            ('L', 2.7),
            ('L', 3.4),
            ('O', 4.1),
            # gap
            ('W', 5.0),
            ('O', 5.9),
            ('R', 6.7),
            ('L', 7.5),
            ('D', 8.2),
        ]

        for letter, offset in sequence:
            self.draw_letter(LETTERS[letter], offset)

    # ------------------------------------------------------------------ helpers

    def call_pen(self, r, g, b, width, off):
        req = SetPen.Request()
        req.r, req.g, req.b = r, g, b
        req.width = width
        req.off   = off
        rclpy.spin_until_future_complete(self, self.set_pen.call_async(req))

    def call_teleport(self, x, y):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), 0.0
        rclpy.spin_until_future_complete(self, self.teleport.call_async(req))

    # ------------------------------------------------------------------ core

    def draw_letter(self, strokes, offset_x):
        for stroke in strokes:
            for i, (x, y) in enumerate(sstroke):
                if i == 0:
                    self.call_pen(255, 255, 255, 3, 1)   # pen up
                    self.call_teleport(x + offset_x, y)
                    self.call_pen(0, 0, 0, 3, 0)          # pen down
                else:
                    self.call_teleport(x + offset_x, y)  # draws segment

    # def _interpolate(self, stroke):
    #     """Return STEPS intermediate points along a multi-point stroke."""
    #     points = []
    #     for i in range(len(stroke) - 1):
    #         x0, y0 = stroke[i]
    #         x1, y1 = stroke[i + 1]
    #         for t in range(STEPS + 1):
    #             alpha = t / STEPS
    #             points.append((
    #                 x0 + alpha * (x1 - x0),
    #                 y0 + alpha * (y1 - y0),
    #             ))
    #     return points


def main():
    rclpy.init()
    rclpy.spin_once(HelloWorldDrawer(), timeout_sec=0)
    rclpy.shutdown()

if __name__ == '__main__':
    main()