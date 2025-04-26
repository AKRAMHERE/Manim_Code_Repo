from manim import *

class ElectronDiffusionCurrent(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Display the question using MathTex only
        question_title = MathTex(r"\textbf{Question:}")
        question_line1 = MathTex(r"\text{Calculate the electron diffusion current }")
        question_line2 = MathTex(r"J_n = -q D_n \frac{dn}{dx}")
        question_line3 = MathTex(r"\text{given that } n(x) \text{ decreases from } 10^{17}\text{ cm}^{-3}")
        question_line4 = MathTex(r"\text{to } 6\times10^{16}\text{ cm}^{-3} \text{ over } 2\,\mu\text{m,}")
        question_line5 = MathTex(r"q = 1.6\times10^{-19}\text{ C},\quad D_n = 35\text{ cm}^2/\text{s}")
        question = VGroup(question_title, question_line1, question_line2, question_line3, question_line4, question_line5)
        question.arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        self.play(Write(question))
        self.wait(3)
        self.play(FadeOut(question))
        
        # Start the solution
        
        # Title
        title = MathTex(r"\text{Electron Diffusion Current}", color=WHITE)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.wait(0.5)
        
        # Semiconductor channel - simple line
        channel = Line(LEFT * 3, RIGHT * 3, color=BLUE)
        channel.shift(UP * 1)  # Position higher to avoid crowding
        self.play(Create(channel))
        
        # Concentration labels
        left_conc = MathTex(r"10^{17}\text{ cm}^{-3}", color=GREEN, font_size=24)
        left_conc.next_to(channel.get_left(), UP)
        right_conc = MathTex(r"6\times10^{16}\text{ cm}^{-3}", color=RED, font_size=24)
        right_conc.next_to(channel.get_right(), UP)
        self.play(FadeIn(left_conc, right_conc))
        
        # Given information
        given_info = MathTex(r"\text{Given: } n(x) \text{ decreases over } 2\mu\text{m}", font_size=24)
        given_info.to_edge(DOWN, buff=1)
        self.play(FadeIn(given_info))
        self.wait(1)
        
        # Draw gradient arrow and label
        gradient = Arrow(channel.get_left(), channel.get_right(), color=YELLOW)
        gradient.next_to(channel, DOWN, buff=0.2)
        gradient_label = MathTex(r"\text{dn/dx}", font_size=24)
        gradient_label.next_to(gradient, DOWN)
        self.play(Create(gradient), Write(gradient_label))
        self.wait(1)
        
        # Show formula
        formula = MathTex(r"J_n = -q D_n \frac{dn}{dx}")
        formula.next_to(title, DOWN, buff=0.8)
        self.play(Write(formula))
        self.wait(1)
        
        # Fade out channel visualization elements
        self.play(
            FadeOut(channel),
            FadeOut(left_conc),
            FadeOut(right_conc),
            FadeOut(gradient),
            FadeOut(gradient_label),
            FadeOut(given_info)
        )
        self.wait(0.5)
        
        # Rearrange formula to center
        self.play(formula.animate.move_to(UP * 2))
        self.wait(0.5)
        
        # Calculation step 1
        calc1 = MathTex(r"\frac{dn}{dx} = \frac{6 \times 10^{16} - 10^{17}}{2 \times 10^{-4}}")
        calc1.next_to(formula, DOWN, buff=0.5)
        self.play(Write(calc1))
        self.wait(1)
        
        calc2 = MathTex(r"= -2 \times 10^{20}\text{ cm}^{-4}")
        calc2.next_to(calc1, DOWN, aligned_edge=LEFT)
        self.play(Write(calc2))
        self.wait(1)
        
        # Final current calculation
        final_calc = MathTex(r"J_n = -(1.6 \times 10^{-19})(35)(-2 \times 10^{20})")
        final_calc.next_to(calc2, DOWN, buff=0.8)
        self.play(Write(final_calc))
        self.wait(1)
        
        result = MathTex(r"= -1112\text{ A/cm}^2")
        result.next_to(final_calc, DOWN, aligned_edge=LEFT)
        self.play(Write(result))
        self.wait(0.5)
        
        # Highlight result with a surrounding rectangle
        box = SurroundingRectangle(result, color=GREEN)
        self.play(Create(box))
        self.wait(1)
        
        # Fade out calculation elements (except the result)
        self.play(
            FadeOut(formula),
            FadeOut(calc1),
            FadeOut(calc2),
            FadeOut(final_calc),
            FadeOut(box)
        )
        self.play(result.animate.next_to(title, DOWN, buff=0.5))
        self.wait(0.5)
        
        # Draw channel again for electron animation
        channel = Line(LEFT * 3, RIGHT * 3, color=BLUE)
        channel.move_to(ORIGIN)
        self.play(Create(channel))
        
        # Animate electrons using MathTex (\bullet symbol)
        electrons = VGroup(*[MathTex(r"\bullet", color=BLUE_B).scale(0.5) for _ in range(8)])
        for i, electron in enumerate(electrons):
            electron.move_to(channel.get_start() + RIGHT * 0.2 * i + UP * 0.1)
        self.play(FadeIn(electrons))
        
        # Move electrons to the right with a slight rotation for flair
        self.play(
            electrons.animate.shift(RIGHT * 5),
            rate_func=linear,
            run_time=2
        )
        self.play(Rotate(electrons, angle=0.2 * PI), run_time=1)
        self.wait(1)
        
        # Fade out elements to prepare for the final answer
        self.play(
            FadeOut(title),
            FadeOut(result),
            FadeOut(channel),
            FadeOut(electrons)
        )
        
        # Show final answer with a scaling pulse effect
        final = MathTex(r"\text{Final Answer: } J_n = -1112\text{ A/cm}^2", color=WHITE)
        self.play(Write(final))
        self.play(final.animate.scale(1.2))
        self.play(final.animate.scale(1/1.2))
        self.wait(2)
