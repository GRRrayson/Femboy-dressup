import random
import tkinter as tk


WINDOW_W = 900
WINDOW_H = 620

SKIN_TONES = ["#f3d7c4", "#e3bfa3", "#c99674", "#8d5f44"]
HAIR_COLORS = ["#1c1c1c", "#6c4a2e", "#b98cff", "#8bd3dd", "#ff8fab"]
TOP_COLORS = ["#ff8fab", "#cdb4db", "#a2d2ff", "#bde0fe", "#ffc8dd"]
BOTTOM_COLORS = ["#22223b", "#4a4e69", "#2b2d42", "#3a5a40", "#1d3557"]
STOCKING_COLORS = ["#111111", "#2f2f2f", "#3d3d3d", "#5a189a"]
ACCESSORY_COLORS = ["#ff4d6d", "#ff85a1", "#f15bb5", "#ff99c8"]
POSES = ["Shy", "Confident", "Cheerful"]


class FemboyDressupGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Femboy Dress-Up Game")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.configure(bg="#1b1b2f")
        self.root.resizable(False, False)

        self.score = 0
        self.target_style = {}
        self.current = {
            "skin": SKIN_TONES[0],
            "hair": HAIR_COLORS[0],
            "top": TOP_COLORS[0],
            "bottom": BOTTOM_COLORS[0],
            "stockings": STOCKING_COLORS[0],
            "accessory": ACCESSORY_COLORS[0],
            "pose": POSES[0],
        }

        self.title_label = tk.Label(
            self.root,
            text="Femboy Dress-Up Challenge",
            bg="#1b1b2f",
            fg="#f8f9fa",
            font=("Segoe UI", 24, "bold"),
        )
        self.title_label.pack(pady=(12, 6))

        self.main_frame = tk.Frame(self.root, bg="#1b1b2f")
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=8)

        self.left = tk.Frame(self.main_frame, bg="#1b1b2f")
        self.left.pack(side="left", fill="both", expand=True)

        self.right = tk.Frame(self.main_frame, bg="#23233a", bd=0, highlightthickness=0)
        self.right.pack(side="right", fill="y", padx=(12, 0))

        self.canvas = tk.Canvas(
            self.left, width=520, height=500, bg="#2a2a40", highlightthickness=0
        )
        self.canvas.pack(pady=8)

        self.target_label = tk.Label(
            self.left,
            text="",
            bg="#1b1b2f",
            fg="#cddafd",
            font=("Segoe UI", 12, "bold"),
            justify="left",
        )
        self.target_label.pack(anchor="w", padx=8, pady=(0, 8))

        self.result_label = tk.Label(
            self.left,
            text="Press 'New Challenge' to start!",
            bg="#1b1b2f",
            fg="#f1faee",
            font=("Segoe UI", 12),
        )
        self.result_label.pack(anchor="w", padx=8, pady=(0, 10))

        self.score_label = tk.Label(
            self.left,
            text="Score: 0",
            bg="#1b1b2f",
            fg="#ffe66d",
            font=("Segoe UI", 14, "bold"),
        )
        self.score_label.pack(anchor="w", padx=8)

        self.build_controls()
        self.new_challenge()
        self.draw_character()

    def build_controls(self):
        tk.Label(
            self.right,
            text="Customize",
            bg="#23233a",
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(12, 16))

        self.add_color_control("Skin Tone", "skin", SKIN_TONES)
        self.add_color_control("Hair Color", "hair", HAIR_COLORS)
        self.add_color_control("Top Color", "top", TOP_COLORS)
        self.add_color_control("Bottom Color", "bottom", BOTTOM_COLORS)
        self.add_color_control("Stockings", "stockings", STOCKING_COLORS)
        self.add_color_control("Accessory", "accessory", ACCESSORY_COLORS)

        tk.Label(
            self.right,
            text="Pose",
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=12, pady=(16, 4))

        self.pose_var = tk.StringVar(value=self.current["pose"])
        pose_menu = tk.OptionMenu(self.right, self.pose_var, *POSES, command=self.set_pose)
        pose_menu.config(bg="#3f3f5f", fg="white", activebackground="#5f5f8f", width=18)
        pose_menu["menu"].config(bg="#3f3f5f", fg="white")
        pose_menu.pack(anchor="w", padx=12, pady=(0, 8))

        tk.Button(
            self.right,
            text="Randomize Outfit",
            command=self.randomize_outfit,
            bg="#7b2cbf",
            fg="white",
            activebackground="#9d4edd",
            relief="flat",
            width=20,
            height=2,
        ).pack(padx=12, pady=(12, 6))

        tk.Button(
            self.right,
            text="Submit Style",
            command=self.submit_style,
            bg="#ff4d6d",
            fg="white",
            activebackground="#ff758f",
            relief="flat",
            width=20,
            height=2,
        ).pack(padx=12, pady=6)

        tk.Button(
            self.right,
            text="New Challenge",
            command=self.new_challenge,
            bg="#06d6a0",
            fg="#14213d",
            activebackground="#33e0b6",
            relief="flat",
            width=20,
            height=2,
        ).pack(padx=12, pady=(6, 12))

    def add_color_control(self, label: str, key: str, palette: list):
        tk.Label(
            self.right,
            text=label,
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=12, pady=(4, 2))

        frame = tk.Frame(self.right, bg="#23233a")
        frame.pack(anchor="w", padx=12, pady=(0, 6))

        for color in palette:
            b = tk.Button(
                frame,
                bg=color,
                width=2,
                height=1,
                relief="flat",
                command=lambda c=color, k=key: self.set_color(k, c),
            )
            b.pack(side="left", padx=3)

    def set_color(self, key: str, color: str):
        self.current[key] = color
        self.draw_character()

    def set_pose(self, pose_value: str):
        self.current["pose"] = pose_value
        self.draw_character()

    def randomize_outfit(self):
        self.current["skin"] = random.choice(SKIN_TONES)
        self.current["hair"] = random.choice(HAIR_COLORS)
        self.current["top"] = random.choice(TOP_COLORS)
        self.current["bottom"] = random.choice(BOTTOM_COLORS)
        self.current["stockings"] = random.choice(STOCKING_COLORS)
        self.current["accessory"] = random.choice(ACCESSORY_COLORS)
        self.current["pose"] = random.choice(POSES)
        self.pose_var.set(self.current["pose"])
        self.draw_character()

    def new_challenge(self):
        self.target_style = {
            "hair": random.choice(HAIR_COLORS),
            "top": random.choice(TOP_COLORS),
            "bottom": random.choice(BOTTOM_COLORS),
            "accessory": random.choice(ACCESSORY_COLORS),
            "pose": random.choice(POSES),
        }
        self.target_label.config(
            text=(
                "Target style:\n"
                f"- Hair: {self.color_name(self.target_style['hair'])}\n"
                f"- Top: {self.color_name(self.target_style['top'])}\n"
                f"- Bottom: {self.color_name(self.target_style['bottom'])}\n"
                f"- Accessory: {self.color_name(self.target_style['accessory'])}\n"
                f"- Pose: {self.target_style['pose']}"
            )
        )
        self.result_label.config(text="Build the look, then press 'Submit Style'.")

    def color_name(self, c: str) -> str:
        return c.upper()

    def submit_style(self):
        matches = 0
        for key in ("hair", "top", "bottom", "accessory", "pose"):
            if self.current[key] == self.target_style[key]:
                matches += 1

        points = matches * 20
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

        if matches == 5:
            msg = "Perfect match! +100 points!"
        elif matches >= 3:
            msg = f"Nice fit! {matches}/5 matched. +{points} points."
        else:
            msg = f"Keep styling! {matches}/5 matched. +{points} points."

        self.result_label.config(text=msg)

    def draw_character(self):
        c = self.canvas
        c.delete("all")

        c.create_rectangle(0, 0, 520, 500, fill="#2a2a40", outline="")
        c.create_oval(350, 40, 470, 120, fill="#ffd6a5", outline="")
        c.create_oval(50, 380, 170, 460, fill="#3a3a57", outline="")

        # Body center coordinates
        cx = 260
        head_y = 110

        # Head
        c.create_oval(cx - 48, head_y - 52, cx + 48, head_y + 44, fill=self.current["skin"], outline="")

        # Hair
        c.create_arc(
            cx - 60,
            head_y - 72,
            cx + 60,
            head_y + 32,
            start=0,
            extent=180,
            fill=self.current["hair"],
            outline=self.current["hair"],
        )
        c.create_rectangle(cx - 55, head_y - 25, cx + 55, head_y - 5, fill=self.current["hair"], outline="")

        # Eyes + smile
        c.create_oval(cx - 22, head_y - 10, cx - 12, head_y, fill="#1a1a1a", outline="")
        c.create_oval(cx + 12, head_y - 10, cx + 22, head_y, fill="#1a1a1a", outline="")
        c.create_arc(cx - 18, head_y + 8, cx + 18, head_y + 24, start=180, extent=180, style="arc", width=2, outline="#7f5539")

        # Torso (top)
        c.create_rectangle(cx - 60, head_y + 42, cx + 60, head_y + 178, fill=self.current["top"], outline="")

        # Skirt/bottom
        c.create_polygon(
            cx - 70,
            head_y + 178,
            cx + 70,
            head_y + 178,
            cx + 90,
            head_y + 250,
            cx - 90,
            head_y + 250,
            fill=self.current["bottom"],
            outline="",
        )

        # Legs + stockings
        c.create_rectangle(cx - 45, head_y + 250, cx - 15, head_y + 360, fill=self.current["skin"], outline="")
        c.create_rectangle(cx + 15, head_y + 250, cx + 45, head_y + 360, fill=self.current["skin"], outline="")
        c.create_rectangle(cx - 45, head_y + 290, cx - 15, head_y + 380, fill=self.current["stockings"], outline="")
        c.create_rectangle(cx + 15, head_y + 290, cx + 45, head_y + 380, fill=self.current["stockings"], outline="")

        # Shoes
        c.create_oval(cx - 58, head_y + 370, cx - 2, head_y + 400, fill="#1a1a1a", outline="")
        c.create_oval(cx + 2, head_y + 370, cx + 58, head_y + 400, fill="#1a1a1a", outline="")

        # Arms vary by pose
        pose = self.current["pose"]
        if pose == "Shy":
            c.create_line(cx - 60, head_y + 90, cx - 95, head_y + 130, width=12, fill=self.current["skin"], smooth=True)
            c.create_line(cx + 60, head_y + 90, cx + 95, head_y + 130, width=12, fill=self.current["skin"], smooth=True)
        elif pose == "Confident":
            c.create_line(cx - 60, head_y + 100, cx - 120, head_y + 100, width=12, fill=self.current["skin"], smooth=True)
            c.create_line(cx + 60, head_y + 100, cx + 120, head_y + 100, width=12, fill=self.current["skin"], smooth=True)
        else:  # Cheerful
            c.create_line(cx - 60, head_y + 100, cx - 110, head_y + 50, width=12, fill=self.current["skin"], smooth=True)
            c.create_line(cx + 60, head_y + 100, cx + 110, head_y + 50, width=12, fill=self.current["skin"], smooth=True)

        # Accessory (heart clip)
        c.create_text(
            cx + 42,
            head_y - 25,
            text="❤",
            fill=self.current["accessory"],
            font=("Segoe UI Emoji", 18, "bold"),
        )


def main():
    root = tk.Tk()
    app = FemboyDressupGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
