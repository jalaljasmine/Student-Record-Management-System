from manim import *

class SingleNodeDemo(Scene):
    def construct(self):
        # Title
        title = Text("Node Structure", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Base rectangle for node
        node_box = Rectangle(
            width=3.8,
            height=1.4,
            stroke_color=GREEN,
            stroke_width=3
        )
        node_box.shift(DOWN * 0.5)

        # Vertical separator to split into "value" and "pointer"
        left = node_box.get_left()
        right = node_box.get_right()
        top = node_box.get_top()
        bottom = node_box.get_bottom()
        mid_x = (left[0] + right[0]) / 2

        separator = Line(
            np.array([mid_x, top[1], 0]),
            np.array([mid_x, bottom[1], 0]),
            stroke_color=GREEN,
            stroke_width=2
        )

        # Inner labels
        value_text = Text("value", font_size=30, color=WHITE)
        pointer_text = Text("next", font_size=30, color=WHITE)

        value_text.move_to(
            np.array([ (left[0] + mid_x) / 2, node_box.get_center()[1], 0 ])
        )
        pointer_text.move_to(
            np.array([ (mid_x + right[0]) / 2, node_box.get_center()[1], 0 ])
        )

        # Caption labels
        caption = Text("A Node in a Linked List", font_size=32, color=YELLOW)
        caption.next_to(node_box, UP, buff=0.8)

        # Draw node step by step
        self.play(Create(node_box))
        self.play(Create(separator))
        self.play(Write(value_text), Write(pointer_text))
        self.play(FadeIn(caption, shift=UP))
        self.wait(1)

        # Highlight value part
        value_highlight = node_box.copy()
        value_highlight.set_fill(color=BLUE, opacity=0.4)
        value_highlight.stretch_to_fit_width((mid_x - left[0]) * 2)
        value_highlight.move_to(
            np.array([ (left[0] + mid_x) / 2, node_box.get_center()[1], 0 ])
        )

        value_desc = Text("Stores actual data", font_size=28, color=BLUE)
        value_desc.next_to(node_box, DOWN, buff=0.6)

        self.play(FadeIn(value_highlight))
        self.play(Write(value_desc))
        self.wait(1.5)
        self.play(FadeOut(value_highlight), FadeOut(value_desc))

        # Highlight pointer part
        pointer_highlight = node_box.copy()
        pointer_highlight.set_fill(color=RED, opacity=0.4)
        pointer_highlight.stretch_to_fit_width((right[0] - mid_x) * 2)
        pointer_highlight.move_to(
            np.array([ (mid_x + right[0]) / 2, node_box.get_center()[1], 0 ])
        )

        pointer_desc = Text("Stores address of next node", font_size=28, color=RED)
        pointer_desc.next_to(node_box, DOWN, buff=0.6)

        self.play(FadeIn(pointer_highlight))
        self.play(Write(pointer_desc))
        self.wait(1.5)
        self.play(FadeOut(pointer_highlight), FadeOut(pointer_desc))

        # Show a dummy "next node" to the right
        next_node_box = Rectangle(
            width=3.0,
            height=1.2,
            stroke_color=GRAY,
            stroke_width=2
        )
        next_node_box.next_to(node_box, RIGHT, buff=2)

        next_label = Text("next node", font_size=26, color=GRAY)
        next_label.move_to(next_node_box.get_center())

        arrow = Arrow(
            start=node_box.get_right(),
            end=next_node_box.get_left(),
            buff=0.1,
            stroke_width=3
        )

        self.play(Create(next_node_box), Write(next_label))
        self.play(Create(arrow))
        self.wait(2)

        # Fade everything at end
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)
