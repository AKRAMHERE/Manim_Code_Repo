from manim import *
import numpy as np

##############################################
# GLOBAL SETTINGS & HELPER FUNCTIONS
##############################################
BACKGROUND_COLOR = "#1E1E1E"
TITLE_COLOR = YELLOW
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = TEAL
BULLET_COLOR = GOLD_A
BLUE_E = "#1C758A"

def bullet_item(text, font_size=28, color=TEXT_COLOR, bullet_color=BULLET_COLOR):
    """
    Creates a bullet item of the form:
      (•) text
    using a VGroup of two Tex objects.
    """
    return VGroup(
        Tex(r"$\bullet$ ", font_size=font_size, color=bullet_color),
        Tex(text, font_size=font_size, color=color)
    ).arrange(RIGHT, buff=0.2)


##############################################
# SCENE 1: Introduction (~2 - 3 minutes)
##############################################
class IntroScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Title and Subtitle in LaTeX
        title = Tex(
            r"\textbf{Numbers to Signals}",
            font_size=64,
            color=TITLE_COLOR
        )
        subtitle = Tex(
            r"\textit{Basics of Complex Numbers, Exponents, and Logarithms}",
            font_size=36,
            color=HIGHLIGHT_COLOR
        ).next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(title, shift=DOWN), run_time=2)
        self.play(FadeIn(subtitle, shift=DOWN), run_time=2)
        self.wait(2)

        # Decorative line
        line = Line(LEFT, RIGHT).scale(6).set_stroke(width=2)
        line.next_to(subtitle, DOWN, buff=0.8)
        self.play(Create(line), run_time=1)

        # Intro Text
        intro_text = Tex(
            r"A 20-minute journey exploring core math concepts \\" 
            r"for circuit analysis \& signal processing. \\" 
            r"We'll connect the dots with simple explanations and plain humor!",
            font_size=30,
            color=TEXT_COLOR
        )
        intro_text.next_to(line, 2*DOWN)

        self.play(Write(intro_text), run_time=4)
        self.wait(3)

        # "What We'll Cover"
        bullet_title = Tex(r"\textbf{What We'll Cover:}", font_size=32, color=HIGHLIGHT_COLOR)
        bullet_title.next_to(intro_text, DOWN, buff=0.6)

        coverage_items = VGroup(
            bullet_item(r"Complex Numbers for AC signals", font_size=30),
            bullet_item(r"Exponents in electronic growth \& decay", font_size=30),
            bullet_item(r"Logarithms for decibels \& compression", font_size=30),
            bullet_item(r"Euler's Formula: The AC superstar", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bullet_title, DOWN, buff=0.3)

        self.play(FadeIn(bullet_title, shift=UP), run_time=2)
        self.wait(1)

        for item in coverage_items:
            self.play(FadeIn(item, shift=LEFT), run_time=2)
            self.wait(1)

        self.wait(2)

        # Fade everything out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)


##############################################
# SCENE 2: Complex Numbers (~4 - 5 minutes)
##############################################
class ComplexNumbersScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Scene Title
        scene_title = Tex(
            r"\textbf{Complex Numbers}", 
            font_size=48, 
            color=TITLE_COLOR
        )
        self.play(FadeIn(scene_title, shift=UP), run_time=2)
        self.wait(1)
        self.play(scene_title.animate.to_edge(UP), run_time=1)

        # Intro
        intro_text = Tex(
            r"Real + Imaginary parts help analyze AC signals. \\" 
            r"Crucial for magnitude \& phase representation.",
            font_size=30,
            color=TEXT_COLOR
        )
        intro_text.next_to(scene_title, DOWN, buff=0.5)

        self.play(Write(intro_text), run_time=3)
        self.wait(3)
        self.play(FadeOut(intro_text), run_time=2)

        # Complex Plane
        axes = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.3}
        ).shift(DOWN * 0.5)

        plane_label = Tex(
            r"\textit{Complex Plane}", 
            font_size=28, 
            color=HIGHLIGHT_COLOR
        ).to_edge(DOWN)

        real_label = Tex("Re", color=GRAY).scale(0.7)
        imag_label = Tex("Im", color=GRAY).scale(0.7)
        real_label.next_to(axes.x_axis.get_right(), UR, buff=0.2)
        imag_label.next_to(axes.y_axis.get_top(), UL, buff=0.2)

        self.play(Create(axes), run_time=3)
        self.play(FadeIn(plane_label), run_time=1)
        self.play(FadeIn(real_label, shift=RIGHT), FadeIn(imag_label, shift=UP))
        self.wait(2)

        # Example complex number
        z_point = Dot(axes.c2p(2, 3), color=YELLOW)
        z_label = MathTex(r"2 + j3").next_to(z_point, UR, buff=0.2).set_color(YELLOW)
        vector = Line(axes.c2p(0, 0), axes.c2p(2, 3), color=YELLOW)

        self.play(GrowFromCenter(z_point), run_time=2)
        self.play(Write(z_label), run_time=2)
        self.play(Create(vector), run_time=2)
        self.wait(2)

        # Arc to show angle
        angle_arc = ArcBetweenPoints(
            axes.c2p(1, 0), 
            axes.c2p(1, 1.5),
            radius=1.0,
            color=YELLOW
        )
        angle_arc_label = MathTex(r"\theta").scale(0.8).set_color(YELLOW)
        angle_arc_label.next_to(angle_arc, RIGHT, buff=0.1)

        self.play(Create(angle_arc), FadeIn(angle_arc_label, shift=UP))
        self.wait(1)

        # Magnitude & Phase
        mag = MathTex(r"\sqrt{2^2 + 3^2} = \sqrt{13}").scale(0.8).to_edge(RIGHT).shift(UP * 1.5)
        angle = MathTex(r"\tan^{-1}\!\bigl(\tfrac{3}{2}\bigr)").scale(0.8)
        angle.next_to(mag, DOWN, buff=0.5)

        self.play(Write(mag), run_time=2)
        self.wait(1)
        self.play(Write(angle), run_time=2)
        self.wait(3)

        # Euler form mention
        euler_form = MathTex(
            r"2 + j3 \;=\; r e^{j\theta}, \quad r=\sqrt{13},\; \theta=\tan^{-1}\!\bigl(\tfrac{3}{2}\bigr)",
            color=WHITE
        ).scale(0.7).next_to(angle, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(euler_form), run_time=2)
        self.wait(2)

        # Bullet points: Why complex numbers?
        bullet_title = Tex(
            r"\textbf{Why Complex Numbers?}",
            font_size=32,
            color=HIGHLIGHT_COLOR
        ).to_edge(UP)

        bullet_points = VGroup(
            bullet_item(r"Easier AC calculations (phasors)"),
            bullet_item(r"Captures magnitude \& phase neatly"),
            bullet_item(r"Reduces trigonometric juggling"),
            bullet_item(r"Used in everything from filters to communications")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 2)

        self.play(FadeIn(bullet_title), run_time=2)
        self.wait(1)

        for bp in bullet_points:
            self.play(FadeIn(bp, shift=LEFT), run_time=2)
            self.wait(1)

        self.wait(2)

        # AC mention
        ac_text = Tex(
            r"In AC circuits, \textit{impedances}: \\" 
            r"$Z_R = R,\quad Z_L = j\omega L,\quad Z_C = \tfrac{1}{j\omega C}.$ \\" 
            r"Complex notation ties them together seamlessly.",
            font_size=28,
            color=TEXT_COLOR
        ).to_edge(DOWN)

        self.play(FadeIn(ac_text, shift=UP), run_time=3)
        self.wait(4)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)


##############################################
# SCENE 3: Exponents (~4 - 5 minutes)
##############################################
class ExponentsScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Title
        title = Tex(r"\textbf{Exponents}", font_size=48, color=TITLE_COLOR)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)

        # Subtext
        subtitle = Tex(
            r"Modeling Rapid Growth \& Decay in Circuits",
            font_size=30,
            color=TEXT_COLOR
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=3)
        self.wait(3)
        self.play(FadeOut(subtitle), run_time=2)

        # Axes for e^x
        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[0, 20, 5],
            tips=True,
            axis_config={"include_numbers": True}
        ).shift(DOWN*0.5)

        graph_label = MathTex(r"y = e^x", font_size=36, color=HIGHLIGHT_COLOR).to_edge(UP)

        self.play(Create(axes), run_time=3)
        self.wait(1)

        func_graph = axes.plot(lambda x: np.e**x, x_range=[-1, 3], color=HIGHLIGHT_COLOR)
        self.play(Create(func_graph), run_time=4)

        self.play(Write(graph_label), run_time=2)
        self.wait(2)

        # Explanation
        explanation_text = Tex(
            r"Exponential growth shoots up for positive $x$, \\" 
            r"and rapidly approaches zero for negative $x$. \\" 
            r"Key in charging, discharging, transistor currents, etc.",
            font_size=28,
            color=TEXT_COLOR
        ).next_to(axes, RIGHT, buff=1)

        self.play(FadeIn(explanation_text, shift=LEFT), run_time=3)
        self.wait(4)

        # RC Discharge example
        rc_text = Tex(
            r"RC Discharge:  $V(t) = V_0 \, e^{-\tfrac{t}{RC}}$ \\" 
            r"Voltage decays exponentially over time.",
            font_size=28,
            color=TEXT_COLOR
        ).to_edge(DOWN)
        self.play(FadeIn(rc_text, shift=UP), run_time=2)
        self.wait(4)

        # Where exponents show up
        bullet_title = Tex(r"\textbf{Where Exponents Show Up:}", font_size=32, color=HIGHLIGHT_COLOR)
        bullet_title.to_edge(UP)

        bullet_points = VGroup(
            bullet_item(r"Amplifier gains (small changes $\to$ big output)"),
            bullet_item(r"Radioactive decay or LED brightness decay"),
            bullet_item(r"Transistor I-V relationships"),
            bullet_item(r"Any process with rate $\propto$ current state")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT*2)

        self.play(FadeIn(bullet_title, shift=DOWN), run_time=2)
        self.wait(1)

        for bp in bullet_points:
            self.play(FadeIn(bp, shift=LEFT), run_time=2)
            self.wait(1)

        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)


##############################################
# SCENE 4: Logarithms (~4 - 5 minutes)
##############################################
class LogsScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Title
        title = Tex(r"\textbf{Logarithms}", font_size=48, color=TITLE_COLOR)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)

        # Intro
        intro_text = Tex(
            r"Taming Huge Ratios with Logarithmic Scales (e.g., dB)",
            font_size=30,
            color=TEXT_COLOR
        ).next_to(title, DOWN)
        self.play(Write(intro_text), run_time=3)
        self.wait(3)
        self.play(FadeOut(intro_text), run_time=2)

        # Log rules
        log_rule_1 = MathTex(r"\log(ab) = \log(a) + \log(b)").scale(0.9)
        log_rule_2 = MathTex(r"\log\bigl(\tfrac{a}{b}\bigr) = \log(a) - \log(b)").scale(0.9)

        VGroup(log_rule_1, log_rule_2).arrange(DOWN, buff=1).to_edge(LEFT)

        self.play(Write(log_rule_1), run_time=3)
        self.wait(2)
        self.play(Write(log_rule_2), run_time=3)
        self.wait(2)

        # Decibel equation
        db_equation = MathTex(
            r"\text{Gain (dB)} = 20 \,\log_{10}\!\Bigl(\tfrac{V_{\text{out}}}{V_{\text{in}}}\Bigr)"
        ).scale(0.8).to_edge(RIGHT).shift(UP*1.5)
        self.play(Write(db_equation), run_time=3)
        self.wait(2)

        # Explanation
        explanation = Tex(
            r"Decibels: express large or small ratios more conveniently. \\" 
            r"Popular in audio levels, RF power, and signal gains.",
            font_size=28,
            color=TEXT_COLOR
        ).to_edge(DOWN)

        self.play(FadeIn(explanation, shift=UP), run_time=3)
        self.wait(3)

        # Additional bullet points
        bullet_title = Tex(r"\textbf{Logarithms in Engineering:}", font_size=32, color=HIGHLIGHT_COLOR)
        bullet_title.to_edge(UP)

        bullet_points = VGroup(
            bullet_item(r"Combine gains by adding dB values"),
            bullet_item(r"Represent wide dynamic ranges (audio, signal strengths)"),
            bullet_item(r"Helps in Bode plots \& frequency response analysis"),
            bullet_item(r"Avoids unwieldy large or tiny numbers")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT*2)

        self.play(FadeIn(bullet_title, shift=DOWN), run_time=2)
        self.wait(1)

        for bp in bullet_points:
            self.play(FadeIn(bp, shift=LEFT), run_time=2)
            self.wait(1)

        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)


##############################################
# SCENE 5: Euler's Formula (~4 - 5 minutes)
##############################################
class EulerScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Title
        title = Tex(r"\textbf{Euler’s Formula}", font_size=48, color=TITLE_COLOR)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)

        # Formula
        euler_formula = MathTex(r"e^{j\theta} = \cos(\theta)\;+\;j\,\sin(\theta)").scale(1.1)
        self.play(Write(euler_formula), run_time=3)
        self.wait(2)

        # Explanation
        explanation_text = Tex(
            r"It unites sine and cosine into a single exponential. \\" 
            r"Crucial for AC signals (phasors) in circuit analysis.",
            font_size=30,
            color=TEXT_COLOR
        )
        explanation_text.next_to(euler_formula, DOWN, buff=0.5)
        self.play(FadeIn(explanation_text, shift=DOWN), run_time=3)
        self.wait(4)

        self.play(FadeOut(explanation_text), run_time=2)

        # Phasor demonstration
        axes = NumberPlane(
            x_range=[-2,2,1], 
            y_range=[-2,2,1], 
            background_line_style={"stroke_opacity": 0.3}
        )
        axes.to_edge(DOWN)
        self.play(Create(axes), run_time=2)

        circle = Circle(radius=1.5, color=HIGHLIGHT_COLOR).move_to(axes.c2p(0,0))
        self.play(Create(circle), run_time=2)

        phasor = Line(axes.c2p(0,0), axes.c2p(1.5,0), color=YELLOW)
        self.play(Create(phasor), run_time=2)
        self.wait(1)

        # Rotate phasor
        self.play(Rotate(phasor, angle=TAU, about_point=axes.c2p(0,0)), run_time=4)
        self.wait(1)

        # Summation text
        sum_text = Tex(
            r"A phasor rotates at $\omega$ rad/s, representing AC magnitude \& phase. \\" 
            r"In real circuits, we often take $\operatorname{Re}\{ e^{\,j\omega t} \}.$",
            font_size=28,
            color=TEXT_COLOR
        ).to_edge(UP)
        self.play(FadeIn(sum_text, shift=UP), run_time=3)
        self.wait(4)

        # Additional bullet points
        bullet_title = Tex(r"\textbf{Euler’s Formula Benefits:}", font_size=32, color=HIGHLIGHT_COLOR)
        bullet_title.to_edge(UP).shift(DOWN*1.5)

        bullet_points = VGroup(
            bullet_item(r"Streamlines trig computations"),
            bullet_item(r"Natural fit for phasor notation"),
            bullet_item(r"Facilitates transformations (Laplace, Fourier)"),
            bullet_item(r"Reduces algebraic complexity in AC circuits")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT*2 + DOWN*0.5)

        self.play(FadeIn(bullet_title, shift=UP), run_time=2)
        self.wait(1)

        for bp in bullet_points:
            self.play(FadeIn(bp, shift=LEFT), run_time=2)
            self.wait(1)

        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(1)


##############################################
# SCENE 6: Conclusion (~2 - 3 minutes)
##############################################
class ConclusionScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # Title
        title = Tex(r"\textbf{Conclusion}", font_size=48, color=TITLE_COLOR)
        self.play(FadeIn(title, shift=UP), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)

        # Recap bullet points
        recap_title = Tex(r"\textbf{Key Takeaways:}", font_size=32, color=HIGHLIGHT_COLOR)
        recap_title.to_edge(LEFT).shift(UP*1.0)

        points = VGroup(
            bullet_item(r"1) Complex Numbers: magnitude \& phase for AC signals"),
            bullet_item(r"2) Exponents: core of growth \& decay in electronics"),
            bullet_item(r"3) Logarithms: decibels \& wide-ranging scales"),
            bullet_item(r"4) Euler’s Formula: merges sin \& cos for AC simplicity")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(recap_title, DOWN, aligned_edge=LEFT)

        self.play(FadeIn(recap_title, shift=UP), run_time=2)
        self.wait(1)

        for p in points:
            self.play(FadeIn(p, shift=RIGHT), run_time=3)
            self.wait(1)

        self.wait(2)

        # Closing text
        closing_text = Tex(
            r"We hope these concepts bring clarity \\" 
            r"to your circuit analysis \& signal processing journey. \\" 
            r"Stay curious, and see you in future sessions!",
            font_size=28,
            color=TEXT_COLOR
        ).to_edge(DOWN)

        self.play(FadeIn(closing_text, shift=UP), run_time=3)
        self.wait(5)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)
        self.wait(2)


# ---------------------------------------------------
# HOW TO RENDER (EXAMPLE):
# manim -pqh numbers_to_signals.py IntroScene ComplexNumbersScene ExponentsScene LogsScene EulerScene ConclusionScene
#
# Each Scene will render separately, preventing any overlap.
# ---------------------------------------------------
