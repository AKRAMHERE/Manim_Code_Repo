from manim import *
import numpy as np

class EVInverterVisualization(Scene):
    def construct(self):
        self.setup_scene()
        self.create_title()
        self.create_components()
        self.show_dc_side()
        self.show_inverter_operation()
        self.show_ac_side()
        self.demonstrate_full_operation()
        self.conclude()

    def setup_scene(self):
        self.camera.background_color = "#1a1a1a"
        self.component_group = VGroup()
        self.waveform_group = VGroup()

    def create_title(self):
        title = Text("EV Inverter Operation", font_size=40, gradient=(BLUE_A, BLUE_D))
        subtitle = Text("DC to 3-Phase AC Conversion", font_size=28, color=GRAY_A)
        title_group = VGroup(title, subtitle).arrange(DOWN)
        self.play(Write(title_group))
        self.wait()
        self.play(
            title_group.animate.scale(0.7).to_edge(UP, buff=0.2),
            run_time=1.5
        )
        self.title_group = title_group

    def create_components(self):
        # Battery
        self.battery = VGroup(
            Rectangle(height=2, width=3, fill_opacity=0.2, stroke_color=BLUE_A),
            VGroup(*[
                Rectangle(height=1.8, width=0.3, fill_opacity=0.5, fill_color=BLUE)
                for _ in range(6)
            ]).arrange(RIGHT, buff=0.3),
            Text("Li-ion Battery\n400V DC", font_size=22, color=BLUE_A)
        ).arrange(DOWN, buff=0.3).shift(LEFT*4)
        
        # Inverter
        self.inverter = self.create_inverter_module()
        
        # Motor
        self.motor = VGroup(
            Circle(radius=1, fill_opacity=0.2, stroke_color=YELLOW_A),
            VGroup(
                Circle(radius=0.8, fill_opacity=0.3),
                Triangle(fill_opacity=0.5).scale(0.3).rotate(PI/2)
            ),
            Text("3-Phase Motor", font_size=22, color=YELLOW_A)
        ).arrange(DOWN, buff=0.3).shift(RIGHT*4)

        self.component_group.add(self.battery, self.inverter, self.motor)

    def create_inverter_module(self):
        inverter = VGroup(
            RoundedRectangle(height=3, width=2.5, corner_radius=0.2, 
                           fill_opacity=0.1, stroke_color=GREEN_A),
            Text("IGBT Inverter", font_size=24, color=GREEN_A)
        )
        
        # Create switch pairs
        switch_positions = [UP, DOWN] * 3
        switches = VGroup()
        for i, pos in enumerate(switch_positions):
            switch = VGroup(
                Rectangle(height=0.5, width=0.3, fill_opacity=0.3, color=GREEN),
                Triangle(fill_opacity=0.5, color=RED).scale(0.2).next_to(pos, RIGHT, buff=0.1)
            )
            switch.move_to(inverter[0].get_center() + pos*(0.7 + (i//2)*0.5))
            switches.add(switch)
        
        inverter.add(switches)
        return inverter

    def show_dc_side(self):
        self.play(
            LaggedStart(
                DrawBorderThenFill(self.battery),
                DrawBorderThenFill(self.inverter),
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.wait()

        # Animate DC voltage
        dc_line = Line(self.battery.get_right(), self.inverter.get_left(), 
                      color=BLUE, stroke_width=4)
        dc_arrows = VGroup(*[Arrow(ORIGIN, RIGHT*0.5, color=BLUE).next_to(dc_line, UP, buff=0.1) 
                           for _ in range(3)])
        
        self.play(
            Create(dc_line),
            dc_arrows.animate.shift(RIGHT*5.5),
            rate_func=linear,
            run_time=3
        )
        self.remove(dc_arrows)

    def show_inverter_operation(self):
        # Highlight switching components
        switches = self.inverter[2]
        self.play(
            LaggedStart(*[
                Indicate(switch[0], color=GREEN, scale_factor=1.3)
                for switch in switches
            ], lag_ratio=0.2),
            run_time=3
        )

        # Create PWM animation
        pwm = self.create_pwm_animation()
        self.play(Create(pwm), run_time=2)
        self.wait()

    def create_pwm_animation(self):
        # Create synchronized PWM visualization
        pwm_group = VGroup()
        for i in range(3):
            axes = Axes(x_range=[0, 4], y_range=[0, 1.5], 
                       x_length=3, y_length=1.5,
                       axis_config={"color": GREEN_A}).shift(DOWN*2 + RIGHT*i*1.5)
            graph = axes.plot(lambda x: (np.sin(x*PI*2) > 0.5*np.sin(x*PI*4)).astype(float),
                            color=GREEN, use_smoothing=False)
            pwm_group.add(VGroup(axes, graph))
        
        return pwm_group

    def show_ac_side(self):
        # Create 3-phase waveforms
        phases = VGroup()
        colors = [RED_A, GREEN_A, BLUE_A]
        for i, color in enumerate(colors):
            axes = Axes(
                x_range=[0, 4], y_range=[-1.5, 1.5], 
                x_length=3, y_length=1.5,
                axis_config={"color": color}
            ).shift(UP*1.5 + RIGHT*i*1.5)
            graph = axes.plot(lambda x: np.sin(x*PI*2 + i*PI*2/3), color=color)
            phases.add(VGroup(axes, graph))
        
        # Animate AC generation
        self.play(
            Transform(self.waveform_group, phases),
            run_time=2,
            lag_ratio=0.2
        )
        self.wait()

        # Show rotating magnetic field
        rotor = self.create_rotating_field()
        self.add(rotor)  # Add the rotor to the scene
        self.play(
            Rotate(rotor, angle=2*PI, about_point=rotor.get_center(), run_time=4),
            rate_func=smooth
        )
        self.wait()

    def create_rotating_field(self):
        rotor = VGroup(
            Circle(radius=0.8, color=YELLOW_A, stroke_width=3),
            Vector(UP).scale(0.7),
            Vector(DOWN).scale(0.7)
        )
        rotor.move_to(self.motor)
        return rotor
    def demonstrate_full_operation(self):
        # Create energy flow animation
        flow_lines = VGroup(*[
            self.create_energy_flow(color)
            for color in [RED_A, GREEN_A, BLUE_A]
        ])
        
        self.play(
            LaggedStart(*[
                ShowPassingFlash(line.copy().set_color(color).set_stroke(width=5))
                for line, color in zip(flow_lines, [RED_A, GREEN_A, BLUE_A])
            ], lag_ratio=0.3),
            run_time=5
        )

    def create_energy_flow(self, color):
        return ArcBetweenPoints(
            self.inverter.get_right(),
            self.motor.get_left(),
            angle=-PI/3,
            stroke_color=color,
            stroke_width=3,
            stroke_opacity=0.7
        )

    def conclude(self):
        # Final summary
        summary = BulletedList(
            "400V DC Battery Input",
            "IGBT PWM Switching @ 10kHz",
            "3-Phase AC Output",
            "Variable Frequency Control",
            height=4,
            width=6
        ).scale(0.8).to_edge(DOWN)
        
        self.play(
            Write(summary),
            self.title_group.animate.set_opacity(0.3),
            run_time=2
        )
        self.wait(3)

if __name__ == "__main__":
    scene = EVInverterVisualization()
    scene.render()