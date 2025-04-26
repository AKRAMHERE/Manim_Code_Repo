from manim import *
import itertools

class ContainerWaterScene(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # 1) OPTIONAL IMAGE AT TOP & INTUITION TEXT
        # -------------------------------------------------------------
        # (Fade out later to avoid overlapping)
        image = ImageMobject("container_problem.png")  # Replace if you have an image
        image.scale(1.1)
        image.to_edge(UP, buff=1.51)
        self.play(FadeIn(image))
        self.wait(1)

        intuition_text = Tex(
            r"Goal: Maximize the water between two vertical lines!"
        ).scale(0.8)
        intuition_text.next_to(image, DOWN)
        self.play(Write(intuition_text))
        self.wait(2)

        intuition_text2 = Tex(
            r"Container with most water = Maximize area between two lines!"
        ).scale(0.8)
        intuition_text2.next_to(image, UP)
        self.play(Write(intuition_text2))
        self.wait(2)
        # -------------------------------------------------------------
        # 2) PROOF OUTLINE (Tex with line breaks)
        # -------------------------------------------------------------
        proof_outline_text = Tex(
            r"\textbf{Proof Outline:}\\",
            r"1) Start with two pointers: L at the left, R at the right.\\",
            r"2) Compute area using the smaller value's height as the limit.\\",
            r"3) Move the pointer at the smaller value inward to find a bigger value.\\",
            r"4) We can ensure that no global maximum is missed by this approach.\\"
        ).scale(0.55)
        proof_outline_text.next_to(intuition_text, DOWN, buff=-0.20)
        #proof_outline_text.to_edge(LEFT)
        #proof_outline_text.shift(DOWN* 0.5)  # adjust 0.5 as needed

        self.play(FadeTransform(intuition_text, proof_outline_text))
        self.wait(3)

        # Fade out both the image and the outline to avoid overlap
        self.play(FadeOut(intuition_text2, shift=UP),FadeOut(image, shift=UP), FadeOut(proof_outline_text, shift=DOWN))
        self.wait(1)

        # -------------------------------------------------------------
        # 3) FINAL FORMULA (MathTex)
        # -------------------------------------------------------------
        formula = MathTex(
            r"\mathrm{Area}(i, j) = (j - i)\times \min\bigl(h_i,\,h_j\bigr)"
        ).scale(0.8)
        formula.to_edge(UP)
        self.play(Write(formula))
        self.wait(2)

        # -------------------------------------------------------------
        # 4) DISPLAY C++ CODE (IDE Style), then Fade Out
        # -------------------------------------------------------------
        cpp_code_text = (
            "#include <iostream>\n"
            "#include <vector>\n"
            "using namespace std;\n\n"
            "int maxArea(vector<int>& height) {\n"
            "    int left = 0, right = height.size() - 1;\n"
            "    int maxWater = 0;\n"
            "    while (left < right) {\n"
            "        maxWater = max(\n"
            "            maxWater,\n"
            "            (right - left) * min(height[left], height[right])\n"
            "        );\n"
            "        if (height[left] < height[right]) {\n"
            "            left++;\n"
            "        } else {\n"
            "            right--;\n"
            "        }\n"
            "    }\n"
            "    return maxWater;\n"
            "}\n\n"
            "int main() {\n"
            "    vector<int> height = {1,8,6,2,5,4,8,3,7};\n"
            "    cout << \"Max Water: \" << maxArea(height) << endl;\n"
            "}"
        )

        cpp_code = Code(
            code=cpp_code_text,
            language="C++",
            font_size=20,
            style="monokai"
        )
        cpp_code.scale(0.8)
        cpp_code.to_edge(DOWN)

        self.play(FadeIn(cpp_code))
        self.wait(3)
        # Fade out code to avoid overlapping with bars
        self.play(FadeOut(cpp_code, shift=DOWN))
        self.wait(1)

        # -------------------------------------------------------------
        # 5) CREATE & ANIMATE THE BAR CHART + TWO POINTERS
        #    (LOOP FULLY, NOT JUST PARTIAL STEPS)
        # -------------------------------------------------------------
        heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        bars = self.create_bars(heights)
        self.play(LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.1))
        self.wait(1)

        left_pointer = Arrow(start=DOWN, end=UP, color=YELLOW)
        left_pointer.move_to(bars[0].get_bottom() + 0.4 * DOWN)
        left_label = MathTex("L").scale(0.8).next_to(left_pointer, DOWN, buff=0.15)

        right_pointer = Arrow(start=DOWN, end=UP, color=YELLOW)
        right_pointer.move_to(bars[-1].get_bottom() + 0.4 * DOWN)
        right_label = MathTex("R").scale(0.8).next_to(right_pointer, DOWN, buff=0.15)

        self.play(
            Create(left_pointer),
            Create(right_pointer),
            Write(left_label),
            Write(right_label)
        )
        self.wait(1)

        # Full loop of 2-pointer approach
        L = 0
        R = len(heights) - 1
        max_area_so_far = 0

        # We'll pick from a set of colors for each water highlight
        highlight_colors = [BLUE, GREEN, RED, ORANGE, PURPLE, GOLD, TEAL]
        color_cycle = itertools.cycle(highlight_colors)
        iteration_count = 1
        while L < R:
            current_height = min(heights[L], heights[R])
            current_width = R - L
            current_area = current_height * current_width

            # Update max area if needed
            if current_area > max_area_so_far:
                max_area_so_far = current_area

            # Create a different color each step
            water_color = next(color_cycle)
            water_rect = self.create_area_rectangle(
                bars[L], bars[R], current_height, water_color
            )

            # Show the water area
            self.play(FadeIn(water_rect, shift=UP))

            # Display current area text near the highlighted rectangle
            area_text = Tex(f"Iteration {iteration_count}: Area = {current_area}").scale(0.8)
            area_text.next_to(water_rect, UP, buff=0.1)
            self.play(FadeIn(area_text, shift=UP))
            self.wait(0.5)

            # Fade out both the area rectangle and the text
            self.play(
                FadeOut(water_rect, shift=DOWN),
                FadeOut(area_text, shift=DOWN)
            )
            self.wait(0.3)

            # Move pointer at smaller height
            if heights[L] < heights[R]:
                L += 1
                self.play(
                    left_pointer.animate.move_to(bars[L].get_bottom() + 0.3 * DOWN),
                    left_label.animate.next_to(left_pointer, DOWN, buff=0.15)
                )
            else:
                R -= 1
                self.play(
                    right_pointer.animate.move_to(bars[R].get_bottom() + 0.3 * DOWN),
                    right_label.animate.next_to(right_pointer, DOWN, buff=0.15)
                )
            iteration_count += 1
            self.wait(0.3)
        # -------------------------------------------------------------
        # 6) SHOW FINAL RESULT & TIME COMPLEXITY
        # -------------------------------------------------------------
        max_area_text = MathTex(
            r"\text{Max Area Found: }", str(max_area_so_far)
        ).scale(0.8)
        max_area_text.to_edge(DOWN, buff=1.0)
        self.play(Write(max_area_text))
        self.wait(1)

        complexity_text = MathTex(
            r"\text{Time Complexity: } O(n)"
        ).scale(0.8)
        complexity_text.next_to(max_area_text, DOWN)
        self.play(Write(complexity_text))
        self.wait(2)

    # ----------------------------------------------------------------
    # HELPER: Create Bars
    # ----------------------------------------------------------------
    def create_bars(self, heights):
        bars = []
        bar_width = 0.5
        gap = 0.2
        n = len(heights)
        total_width = n * (bar_width + gap) - gap
        left_x_start = -total_width / 2

        for i, h in enumerate(heights):
            x_pos = left_x_start + i * (bar_width + gap)
            bar = Rectangle(
                width=bar_width,
                height=h * 0.2,
                color=BLUE,
                fill_opacity=0.8,
                stroke_opacity=1
            )
            # Position so bar's bottom is at y=0
            bar.move_to([x_pos, (h * 0.2) / 2, 0])
            bars.append(bar)
        return bars

    # ----------------------------------------------------------------
    # HELPER: Create "Water" Rectangle with a Given Color
    # ----------------------------------------------------------------
    def create_area_rectangle(self, bar_left, bar_right, water_height, color):
        left_x = bar_left.get_left()[0]
        right_x = bar_right.get_right()[0]
        left_bar_top_y = bar_left.get_top()[1]
        right_bar_top_y = bar_right.get_top()[1]
        water_level_y = min(left_bar_top_y, right_bar_top_y)

        rect = Rectangle(
            width=(right_x - left_x),
            height=(water_level_y - 0),
            fill_color=color,
            fill_opacity=0.3,
            stroke_opacity=0
        )
        rect.move_to([
            (left_x + right_x) / 2,
            water_level_y / 2,
            0
        ])
        return rect
