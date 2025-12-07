from manim import *

# Helper to create a node as a VGroup
def make_node(value_text: str, color=GREEN):
    box = Rectangle(width=3.8, height=1.2, stroke_color=color, stroke_width=3)

    left = box.get_left()
    right = box.get_right()
    top = box.get_top()
    bottom = box.get_bottom()
    mid_x = (left[0] + right[0]) / 2

    separator = Line(
        np.array([mid_x, top[1], 0]),
        np.array([mid_x, bottom[1], 0]),
        stroke_color=color,
        stroke_width=2
    )

    value = Text(str(value_text), font_size=30, color=WHITE)
    value.move_to(np.array([(left[0] + mid_x) / 2, box.get_center()[1], 0]))

    pointer = Text("ptr", font_size=26, color=WHITE)
    pointer.move_to(np.array([(mid_x + right[0]) / 2, box.get_center()[1], 0]))

    node = VGroup(box, separator, value, pointer)
    return node


class LinkedListDemo(Scene):
    def construct(self):
        # Title
        title = Text("Singly Linked List", font_size=60).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create three nodes vertically
        node1 = make_node("10")
        node2 = make_node("20")
        node3 = make_node("30")

        node1.shift(UP * 1)
        node2.next_to(node1, DOWN, buff=1.0)
        node3.next_to(node2, DOWN, buff=1.0)

        self.play(FadeIn(node1, shift=DOWN))
        self.play(FadeIn(node2, shift=DOWN))
        self.play(FadeIn(node3, shift=DOWN))
        self.wait(0.5)

        # Create HEAD box
        head_box = Rectangle(width=2.2, height=0.8, stroke_color=YELLOW, stroke_width=3)
        head_text = Text("HEAD", font_size=28, color=YELLOW)
        head_group = VGroup(head_box, head_text)
        head_text.move_to(head_box.get_center())
        head_group.to_edge(LEFT).shift(UP * 1.5)

        self.play(Create(head_box), Write(head_text))
        self.wait(0.5)

        # Head arrow to first node
        head_arrow = Arrow(
            start=head_box.get_right(),
            end=node1.get_left(),
            buff=0.2,
            stroke_color=YELLOW,
            stroke_width=3
        )
        self.play(Create(head_arrow))
        self.wait(0.5)

        # Link arrows between nodes (node1 -> node2 -> node3)
        arrow_1_2 = Arrow(
            start=node1.get_right(),
            end=node2.get_left(),
            buff=0.2,
            stroke_color=BLUE,
            stroke_width=3
        )
        arrow_2_3 = Arrow(
            start=node2.get_right(),
            end=node3.get_left(),
            buff=0.2,
            stroke_color=BLUE,
            stroke_width=3
        )

        self.play(Create(arrow_1_2))
        self.play(Create(arrow_2_3))
        self.wait(1)

        # Set last node pointer = NULL
        null_text = Text("NULL", font_size=28, color=RED)
        null_text.next_to(node3, RIGHT, buff=0.8)
        arrow_3_null = Arrow(
            start=node3.get_right(),
            end=null_text.get_left(),
            buff=0.1,
            stroke_color=RED,
            stroke_width=3
        )
        self.play(Write(null_text), Create(arrow_3_null))
        self.wait(1.5)

        # Highlight data vs pointer of middle node to explain
        mid_box = node2[0]      # full rectangle
        mid_separator = node2[1]

        left = mid_box.get_left()
        right = mid_box.get_right()
        center = mid_box.get_center()
        top = mid_box.get_top()
        bottom = mid_box.get_bottom()
        mid_x = (left[0] + right[0]) / 2

        # Data part highlight
        data_highlight = Rectangle(
            width=(mid_x - left[0]) * 2,
            height=top[1] - bottom[1],
            fill_color=BLUE,
            fill_opacity=0.4,
            stroke_color=BLUE,
            stroke_opacity=0
        )
        data_highlight.move_to(
            np.array([(left[0] + mid_x) / 2, center[1], 0])
        )

        data_caption = Text("DATA = 20", font_size=28, color=BLUE)
        data_caption.next_to(node2, LEFT, buff=0.6)

        self.play(FadeIn(data_highlight))
        self.play(Write(data_caption))
        self.wait(1.5)
        self.play(FadeOut(data_highlight), FadeOut(data_caption))

        # Pointer part highlight
        ptr_highlight = Rectangle(
            width=(right[0] - mid_x) * 2,
            height=top[1] - bottom[1],
            fill_color=ORANGE,
            fill_opacity=0.4,
            stroke_color=ORANGE,
            stroke_opacity=0
        )
        ptr_highlight.move_to(
            np.array([(mid_x + right[0]) / 2, center[1], 0])
        )

        ptr_caption = Text("Pointer to NEXT node", font_size=26, color=ORANGE)
        ptr_caption.next_to(node2, RIGHT, buff=0.6)

        self.play(FadeIn(ptr_highlight))
        self.play(Write(ptr_caption))
        self.wait(1.5)
        self.play(FadeOut(ptr_highlight), FadeOut(ptr_caption))

        # TRAVERSAL animation: move a "current" pointer from head to each node
        current_label = Text("current", font_size=26, color=YELLOW)
        current_box = SurroundingRectangle(node1, color=YELLOW, buff=0.15)
        current_label.next_to(node1, LEFT, buff=0.3)

        self.play(Create(current_box), Write(current_label))
        self.wait(0.5)

        # Move to node2
        self.play(
            current_box.animate.move_to(node2),
            current_label.animate.next_to(node2, LEFT, buff=0.3),
            run_time=1.2
        )
        self.wait(0.5)

        # Move to node3
        self.play(
            current_box.animate.move_to(node3),
            current_label.animate.next_to(node3, LEFT, buff=0.3),
            run_time=1.2
        )
        self.wait(0.5)

        # Move to NULL
        self.play(
            current_box.animate.move_to(null_text),
            current_label.animate.next_to(null_text, UP, buff=0.3),
            run_time=1.2
        )
        end_caption = Text("Traversal stops at NULL", font_size=28, color=RED)
        end_caption.next_to(null_text, DOWN, buff=0.4)
        self.play(Write(end_caption))
        self.wait(2)

        # Clear the scene
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)
