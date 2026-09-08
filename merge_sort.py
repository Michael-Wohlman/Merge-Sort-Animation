from manim import *

class Test(Scene):
    def construct(self):
        title = Text("Hello World")
        self.play(Write(title))
        self.wait(2)