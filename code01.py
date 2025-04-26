from manim import *

class PalindromeVisualization(Scene):
    def construct(self):
        ############################################
        # 1. Introduction & Algorithm Explanation
        ############################################
        title = Tex(r"Palindrome Checker Visualization", font_size=56)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.8)

        algo_explanation = VGroup(
            Tex(r"\textbf{Algorithm Explanation:}", font_size=42),
            Tex(r"1. Normalize the string: remove non-alphanumerics \& convert to lowercase.", font_size=32),
            Tex(r"2. Initialize two pointers: one at the start, one at the end.", font_size=32),
            Tex(r"3. Compare characters from both ends.", font_size=32),
            Tex(r"4. If a mismatch is found, return False; else, return True.", font_size=32)
        )
        algo_explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        algo_explanation.to_edge(LEFT, buff=1)
        self.play(FadeIn(algo_explanation, shift=RIGHT))
        self.wait(3)

        # Fade out algorithm explanation
        self.play(FadeOut(algo_explanation), run_time=0.8)
        self.wait(0.5)

        ############################################
        # 2. Display Python Code
        ############################################
        code_title = Tex(r"Python Code for Palindrome Check", font_size=42)
        code_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(code_title))
        self.wait(0.5)

        code_str = r"""def is_palindrome(s: str) -> bool:
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(normalized) - 1
    while left < right:
        if normalized[left] != normalized[right]:
            return False
        left += 1
        right -= 1
    return True"""
        code = Code(
            code=code_str,
            language="Python",
            background="window",
            insert_line_no=False
        )
        code.scale(1.1)
        code.next_to(code_title, DOWN, buff=0.5)
        self.play(FadeIn(code))
        self.wait(3)

        self.play(FadeOut(VGroup(code_title, code)), run_time=0.8)
        self.wait(0.5)
        self.clear()

        ############################################
        # 3. Example 1: Palindrome Visualization
        ############################################
        ex1_title = Tex(r"Example 1: Palindrome", font_size=42, color=GREEN)
        ex1_title.to_edge(UP)
        self.play(Write(ex1_title))
        self.wait(0.5)

        orig1 = Tex(r"Original: A man, a plan, a canal: Panama", font_size=36)
        orig1.next_to(ex1_title, DOWN, aligned_edge=LEFT, buff=0.5)
        norm1 = Tex(r"Normalized: amanaplanacanalpanama", font_size=36)
        norm1.next_to(orig1, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(orig1), Write(norm1))
        self.wait(0.5)

        # Visualize normalized string with squares (smaller and centered)
        norm_str1 = "amanaplanacanalpanama"
        squares1 = VGroup(*[
            Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.5)
            for _ in norm_str1
        ])
        squares1.arrange(RIGHT, buff=0.1)
        squares1.move_to(ORIGIN)
        letters1 = VGroup(*[
            Tex(letter, font_size=32) for letter in list(norm_str1)
        ])
        for square, letter in zip(squares1, letters1):
            letter.move_to(square.get_center())
        self.play(FadeIn(squares1), FadeIn(letters1))
        self.wait(0.5)

        # Two-pointer animation for Example 1
        left_idx = 0
        right_idx = len(squares1) - 1
        left_arrow = Arrow(
            squares1[left_idx].get_bottom(),
            squares1[left_idx].get_bottom() + DOWN * 0.4,
            color=YELLOW
        )
        right_arrow = Arrow(
            squares1[right_idx].get_bottom(),
            squares1[right_idx].get_bottom() + DOWN * 0.4,
            color=YELLOW
        )
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.wait(0.5)

        while left_idx < right_idx:
            self.play(
                squares1[left_idx].animate.set_fill(RED, opacity=0.8),
                squares1[right_idx].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )
            self.wait(0.3)
            self.play(
                squares1[left_idx].animate.set_fill(GREEN, opacity=0.8),
                squares1[right_idx].animate.set_fill(GREEN, opacity=0.8),
                run_time=0.5
            )
            self.wait(0.3)
            left_idx += 1
            right_idx -= 1
            if left_idx < right_idx:
                new_left_arrow = Arrow(
                    squares1[left_idx].get_bottom(),
                    squares1[left_idx].get_bottom() + DOWN * 0.4,
                    color=YELLOW
                )
                new_right_arrow = Arrow(
                    squares1[right_idx].get_bottom(),
                    squares1[right_idx].get_bottom() + DOWN * 0.4,
                    color=YELLOW
                )
                self.play(
                    Transform(left_arrow, new_left_arrow),
                    Transform(right_arrow, new_right_arrow),
                    run_time=0.5
                )
                self.wait(0.3)

        result1 = Tex(r"Result: It's a Palindrome!", font_size=38, color=GREEN)
        result1.next_to(squares1, DOWN, buff=0.5)
        self.play(Write(result1))
        self.wait(2)

        self.play(FadeOut(VGroup(ex1_title, orig1, norm1, squares1, letters1, left_arrow, right_arrow, result1)), run_time=0.8)
        self.wait(0.5)
        self.clear()

        ############################################
        # 4. Example 2: Non-Palindrome Visualization
        ############################################
        ex2_title = Tex(r"Example 2: Not a Palindrome", font_size=42, color=RED)
        ex2_title.to_edge(UP)
        self.play(Write(ex2_title))
        self.wait(0.5)

        orig2 = Tex(r"Original: race a car", font_size=36)
        orig2.next_to(ex2_title, DOWN, aligned_edge=LEFT, buff=0.5)
        norm2 = Tex(r"Normalized: raceacar", font_size=36)
        norm2.next_to(orig2, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(orig2), Write(norm2))
        self.wait(0.5)

        norm_str2 = "raceacar"
        squares2 = VGroup(*[
            Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.5)
            for _ in norm_str2
        ])
        squares2.arrange(RIGHT, buff=0.1)
        squares2.move_to(ORIGIN)
        letters2 = VGroup(*[
            Tex(letter, font_size=32) for letter in list(norm_str2)
        ])
        for square, letter in zip(squares2, letters2):
            letter.move_to(square.get_center())
        self.play(FadeIn(squares2), FadeIn(letters2))
        self.wait(0.5)

        left_idx = 0
        right_idx = len(squares2) - 1
        left_arrow = Arrow(
            squares2[left_idx].get_bottom(),
            squares2[left_idx].get_bottom() + DOWN * 0.4,
            color=YELLOW
        )
        right_arrow = Arrow(
            squares2[right_idx].get_bottom(),
            squares2[right_idx].get_bottom() + DOWN * 0.4,
            color=YELLOW
        )
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.wait(0.5)

        is_palindrome_flag = True
        while left_idx < right_idx:
            self.play(
                squares2[left_idx].animate.set_fill(RED, opacity=0.8),
                squares2[right_idx].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )
            self.wait(0.3)
            if norm_str2[left_idx] == norm_str2[right_idx]:
                self.play(
                    squares2[left_idx].animate.set_fill(GREEN, opacity=0.8),
                    squares2[right_idx].animate.set_fill(GREEN, opacity=0.8),
                    run_time=0.5
                )
            else:
                self.play(
                    squares2[left_idx].animate.set_fill(ORANGE, opacity=0.8),
                    squares2[right_idx].animate.set_fill(ORANGE, opacity=0.8),
                    run_time=0.5
                )
                is_palindrome_flag = False
            self.wait(0.3)
            left_idx += 1
            right_idx -= 1
            if left_idx < right_idx:
                new_left_arrow = Arrow(
                    squares2[left_idx].get_bottom(),
                    squares2[left_idx].get_bottom() + DOWN * 0.4,
                    color=YELLOW
                )
                new_right_arrow = Arrow(
                    squares2[right_idx].get_bottom(),
                    squares2[right_idx].get_bottom() + DOWN * 0.4,
                    color=YELLOW
                )
                self.play(
                    Transform(left_arrow, new_left_arrow),
                    Transform(right_arrow, new_right_arrow),
                    run_time=0.5
                )
                self.wait(0.3)

        if is_palindrome_flag:
            result2 = Tex(r"Result: It's a Palindrome!", font_size=38, color=GREEN)
        else:
            result2 = Tex(r"Result: Not a Palindrome!", font_size=38, color=RED)
        result2.next_to(squares2, DOWN, buff=0.5)
        self.play(Write(result2))
        self.wait(2)

        self.play(FadeOut(VGroup(ex2_title, orig2, norm2, squares2, letters2, left_arrow, right_arrow, result2)), run_time=0.8)
        self.wait(0.5)
