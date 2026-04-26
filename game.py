import random
import tkinter as tk
import webbrowser
from pathlib import Path
from typing import Dict, Mapping
try:
    import winsound
except ImportError:
    winsound = None


WINDOW_W = 900
WINDOW_H = 700

SKIN_TONES = ["#f3d7c4", "#e3bfa3", "#c99674", "#8d5f44"]
HAIR_COLORS = ["#1c1c1c", "#6c4a2e", "#b98cff", "#8bd3dd", "#ff8fab"]
TOP_COLORS = ["#ff8fab", "#cdb4db", "#a2d2ff", "#bde0fe", "#ffc8dd"]
BOTTOM_COLORS = ["#22223b", "#4a4e69", "#2b2d42", "#3a5a40", "#1d3557"]
STOCKING_COLORS = ["#111111", "#2f2f2f", "#3d3d3d", "#5a189a"]
ACCESSORY_COLORS = ["#ff4d6d", "#ff85a1", "#f15bb5", "#ff99c8"]
POSES = ["Shy", "Confident", "Cheerful", "Wave", "Hands Up", "Crossed Arms"]
HAIR_STYLES = ["Soft Fringe", "Bob Cut", "Twin Tails", "Side Part", "Messy Fluff"]
ACCESSORY_TYPES = ["Heart Clip", "Star Clip", "Bow", "Choker", "Glasses"]
GOOGLE_IMAGE_SEARCH_URL = (
    "https://www.google.com/search?tbm=isch&q=femboy+fashion+portrait+safe"
)

STYLE_FIELDS = (
    "hair",
    "hair_style",
    "top",
    "bottom",
    "accessory",
    "accessory_type",
    "pose",
)
TARGET_LABELS = {
    "hair": "Hair",
    "hair_style": "Hair Style",
    "top": "Top",
    "bottom": "Bottom",
    "accessory": "Accessory",
    "accessory_type": "Accessory Type",
    "pose": "Pose",
}
COLOR_NAMES = {
    "#f3d7c4": "Soft Peach",
    "#e3bfa3": "Warm Beige",
    "#c99674": "Caramel",
    "#8d5f44": "Mocha",
    "#1c1c1c": "Jet Black",
    "#6c4a2e": "Chestnut",
    "#b98cff": "Lavender",
    "#8bd3dd": "Aqua",
    "#ff8fab": "Rose Pink",
    "#cdb4db": "Lilac",
    "#a2d2ff": "Sky Blue",
    "#bde0fe": "Powder Blue",
    "#ffc8dd": "Blush Pink",
    "#22223b": "Ink",
    "#4a4e69": "Slate",
    "#2b2d42": "Midnight",
    "#3a5a40": "Forest",
    "#1d3557": "Deep Navy",
    "#111111": "Black",
    "#2f2f2f": "Charcoal",
    "#3d3d3d": "Graphite",
    "#5a189a": "Royal Purple",
    "#ff4d6d": "Candy Red",
    "#ff85a1": "Pink Coral",
    "#f15bb5": "Bubblegum",
    "#ff99c8": "Light Rose",
}
PALETTES: Mapping[str, list[str]] = {
    "skin": SKIN_TONES,
    "hair": HAIR_COLORS,
    "top": TOP_COLORS,
    "bottom": BOTTOM_COLORS,
    "stockings": STOCKING_COLORS,
    "accessory": ACCESSORY_COLORS,
}
CHANGE_DIALOGUE = {
    "skin": ["This skin tone looks great.", "Nice vibe for this look."],
    "hair": ["I like this hair color.", "This color pops nicely."],
    "hair_style": ["This hair style is cute.", "This style really fits."],
    "top": ["Love this top choice.", "This top is super stylish."],
    "bottom": ["Great bottom style pick.", "That pairs well with the top."],
    "stockings": ["Those stockings look clean.", "Good stockings match."],
    "accessory": ["Nice accessory color.", "That color accent works."],
    "accessory_type": ["I like this accessory.", "That accessory is adorable."],
    "pose": ["This pose has attitude.", "Nice pose choice."],
}


class FemboyDressupGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Femboy Dress-Up Game")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.configure(bg="#1b1b2f")
        self.root.resizable(False, False)

        self.score = 0
        self.target_style: Dict[str, str] = {}
        self.current = self._build_default_style()

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
        self.controls_canvas = tk.Canvas(
            self.right, width=280, height=500, bg="#23233a", highlightthickness=0
        )
        self.controls_scrollbar = tk.Scrollbar(
            self.right, orient="vertical", command=self.controls_canvas.yview
        )
        self.controls_container = tk.Frame(self.controls_canvas, bg="#23233a")
        self.controls_container.bind(
            "<Configure>",
            lambda _e: self.controls_canvas.configure(
                scrollregion=self.controls_canvas.bbox("all")
            ),
        )
        self.controls_canvas.create_window(
            (0, 0), window=self.controls_container, anchor="nw"
        )
        self.controls_canvas.configure(yscrollcommand=self.controls_scrollbar.set)
        self.controls_canvas.pack(side="left", fill="y")
        self.controls_scrollbar.pack(side="right", fill="y")
        self.controls_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.canvas = tk.Canvas(
            self.left, width=520, height=430, bg="#2a2a40", highlightthickness=0
        )
        self.canvas.pack(pady=8)

        self.challenge_title_label = tk.Label(
            self.left,
            text="Challenge",
            bg="#1b1b2f",
            fg="#9bf6ff",
            font=("Segoe UI", 12, "bold"),
        )
        self.challenge_title_label.pack(anchor="w", padx=8)

        self.target_label = tk.Label(
            self.left,
            text="",
            bg="#1b1b2f",
            fg="#cddafd",
            font=("Segoe UI", 12, "bold"),
            justify="left",
            wraplength=500,
        )
        self.target_label.pack(anchor="w", padx=8, pady=(0, 8))

        self.dialogue_title_label = tk.Label(
            self.left,
            text="Dialogue",
            bg="#1b1b2f",
            fg="#ffd6a5",
            font=("Segoe UI", 11, "bold"),
        )
        self.dialogue_title_label.pack(anchor="w", padx=8)

        self.dialogue_label = tk.Label(
            self.left,
            text="Press 'New Challenge' to start.",
            bg="#1b1b2f",
            fg="#f1faee",
            font=("Segoe UI", 12),
            justify="left",
            wraplength=500,
        )
        self.dialogue_label.pack(anchor="w", padx=8, pady=(0, 8))

        self.status_label = tk.Label(
            self.left,
            text="Status: Waiting for your style choices.",
            bg="#1b1b2f",
            fg="#bde0fe",
            font=("Segoe UI", 11, "italic"),
            justify="left",
            wraplength=500,
        )
        self.status_label.pack(anchor="w", padx=8, pady=(0, 10))

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
            self.controls_container,
            text="Customize",
            bg="#23233a",
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(12, 16))

        self.add_color_control("Skin Tone", "skin", PALETTES["skin"])
        self.add_color_control("Hair Color", "hair", PALETTES["hair"])
        self.add_color_control("Top Color", "top", PALETTES["top"])
        self.add_color_control("Bottom Color", "bottom", PALETTES["bottom"])
        self.add_color_control("Stockings", "stockings", PALETTES["stockings"])
        self.add_color_control("Accessory", "accessory", PALETTES["accessory"])

        tk.Label(
            self.controls_container,
            text="Hair Style",
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=12, pady=(16, 4))

        self.hair_style_var = tk.StringVar(value=self.current["hair_style"])
        hair_style_menu = tk.OptionMenu(
            self.controls_container,
            self.hair_style_var,
            *HAIR_STYLES,
            command=self.set_hair_style,
        )
        hair_style_menu.config(
            bg="#3f3f5f", fg="white", activebackground="#5f5f8f", width=18
        )
        hair_style_menu["menu"].config(bg="#3f3f5f", fg="white")
        hair_style_menu.pack(anchor="w", padx=12, pady=(0, 8))

        tk.Label(
            self.controls_container,
            text="Accessory Type",
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=12, pady=(8, 4))

        self.accessory_type_var = tk.StringVar(value=self.current["accessory_type"])
        accessory_type_menu = tk.OptionMenu(
            self.controls_container,
            self.accessory_type_var,
            *ACCESSORY_TYPES,
            command=self.set_accessory_type,
        )
        accessory_type_menu.config(
            bg="#3f3f5f", fg="white", activebackground="#5f5f8f", width=18
        )
        accessory_type_menu["menu"].config(bg="#3f3f5f", fg="white")
        accessory_type_menu.pack(anchor="w", padx=12, pady=(0, 8))

        tk.Label(
            self.controls_container,
            text="Pose",
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=12, pady=(16, 4))

        self.pose_var = tk.StringVar(value=self.current["pose"])
        pose_menu = tk.OptionMenu(
            self.controls_container, self.pose_var, *POSES, command=self.set_pose
        )
        pose_menu.config(bg="#3f3f5f", fg="white", activebackground="#5f5f8f", width=18)
        pose_menu["menu"].config(bg="#3f3f5f", fg="white")
        pose_menu.pack(anchor="w", padx=12, pady=(0, 8))

        tk.Button(
            self.controls_container,
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
            self.controls_container,
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
            self.controls_container,
            text="New Challenge",
            command=self.new_challenge,
            bg="#06d6a0",
            fg="#14213d",
            activebackground="#33e0b6",
            relief="flat",
            width=20,
            height=2,
        ).pack(padx=12, pady=(6, 12))

        tk.Button(
            self.controls_container,
            text="Open Google Images",
            command=self.open_google_images,
            bg="#4361ee",
            fg="white",
            activebackground="#5a74f0",
            relief="flat",
            width=20,
            height=1,
        ).pack(padx=12, pady=(0, 6))

        tk.Button(
            self.controls_container,
            text="Open Local Image Folder",
            command=self.open_local_image_folder,
            bg="#4cc9f0",
            fg="#14213d",
            activebackground="#72d9f4",
            relief="flat",
            width=20,
            height=1,
        ).pack(padx=12, pady=(0, 10))

    def _build_default_style(self) -> Dict[str, str]:
        return {
            "skin": SKIN_TONES[0],
            "hair": HAIR_COLORS[0],
            "hair_style": HAIR_STYLES[0],
            "top": TOP_COLORS[0],
            "bottom": BOTTOM_COLORS[0],
            "stockings": STOCKING_COLORS[0],
            "accessory": ACCESSORY_COLORS[0],
            "accessory_type": ACCESSORY_TYPES[0],
            "pose": POSES[0],
        }

    def add_color_control(self, label: str, key: str, palette: list[str]):
        tk.Label(
            self.controls_container,
            text=label,
            bg="#23233a",
            fg="#d9d9ef",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=12, pady=(4, 2))

        frame = tk.Frame(self.controls_container, bg="#23233a")
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
        self.notify_style_change(key)
        self.draw_character()

    def set_pose(self, pose_value: str):
        self.current["pose"] = pose_value
        self.notify_style_change("pose")
        self.draw_character()

    def set_hair_style(self, style_value: str):
        self.current["hair_style"] = style_value
        self.notify_style_change("hair_style")
        self.draw_character()

    def set_accessory_type(self, accessory_value: str):
        self.current["accessory_type"] = accessory_value
        self.notify_style_change("accessory_type")
        self.draw_character()

    def on_mousewheel(self, event: tk.Event):
        self.controls_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def play_change_sound(self):
        if winsound is not None:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

    def notify_style_change(self, field: str):
        self.play_change_sound()
        message = random.choice(CHANGE_DIALOGUE.get(field, ["Looking good!"]))
        self.dialogue_label.config(text=message)
        self.status_label.config(text=f"Status: Updated {TARGET_LABELS.get(field, field)}.")

    def open_google_images(self):
        webbrowser.open_new_tab(GOOGLE_IMAGE_SEARCH_URL)
        self.status_label.config(
            text="Opened Google Images. Save pictures locally, then use your folder."
        )

    def open_local_image_folder(self):
        # Opens the game directory so you can manage your own image files.
        webbrowser.open_new_tab(Path.cwd().resolve().as_uri())
        self.status_label.config(
            text="Opened local folder view. Add your reference images there."
        )

    def randomize_outfit(self):
        for key, palette in PALETTES.items():
            self.current[key] = random.choice(palette)
        self.current["hair_style"] = random.choice(HAIR_STYLES)
        self.current["accessory_type"] = random.choice(ACCESSORY_TYPES)
        self.current["pose"] = random.choice(POSES)
        self.hair_style_var.set(self.current["hair_style"])
        self.accessory_type_var.set(self.current["accessory_type"])
        self.pose_var.set(self.current["pose"])
        self.play_change_sound()
        self.dialogue_label.config(text="Fresh random fit! This look is fire.")
        self.status_label.config(text="Status: Outfit randomized.")
        self.draw_character()

    def new_challenge(self):
        self.target_style = {
            "hair": random.choice(HAIR_COLORS),
            "hair_style": random.choice(HAIR_STYLES),
            "top": random.choice(TOP_COLORS),
            "bottom": random.choice(BOTTOM_COLORS),
            "accessory": random.choice(ACCESSORY_COLORS),
            "accessory_type": random.choice(ACCESSORY_TYPES),
            "pose": random.choice(POSES),
        }
        self.target_label.config(text=self.format_target_text())
        self.status_label.config(text="Status: Build the look, then press Submit Style.")

    def color_name(self, c: str) -> str:
        return COLOR_NAMES.get(c.lower(), c.upper())

    def format_target_text(self) -> str:
        lines = ["Target style:"]
        for key in STYLE_FIELDS:
            value = self.target_style[key]
            if key in ("pose", "hair_style", "accessory_type"):
                lines.append(f"- {TARGET_LABELS[key]}: {value}")
            else:
                lines.append(f"- {TARGET_LABELS[key]}: {self.color_name(value)}")
        return "\n".join(lines)

    def submit_style(self):
        matches = sum(
            1 for key in STYLE_FIELDS if self.current[key] == self.target_style[key]
        )

        points = matches * 20
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

        if matches == 5:
            msg = "Perfect match! +100 points!"
        elif matches >= 3:
            msg = f"Nice fit! {matches}/5 matched. +{points} points."
        else:
            msg = f"Keep styling! {matches}/5 matched. +{points} points."

        self.status_label.config(text=f"Status: {msg}")

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

        self.draw_hair(c, cx, head_y)

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
        for left, right in ((cx - 45, cx - 15), (cx + 15, cx + 45)):
            c.create_rectangle(
                left,
                head_y + 250,
                right,
                head_y + 360,
                fill=self.current["skin"],
                outline="",
            )
            c.create_rectangle(
                left,
                head_y + 290,
                right,
                head_y + 380,
                fill=self.current["stockings"],
                outline="",
            )

        # Shoes
        c.create_oval(cx - 58, head_y + 370, cx - 2, head_y + 400, fill="#1a1a1a", outline="")
        c.create_oval(cx + 2, head_y + 370, cx + 58, head_y + 400, fill="#1a1a1a", outline="")

        self.draw_arms(c, cx, head_y)

        self.draw_accessory(c, cx, head_y)

    def draw_hair(self, canvas: tk.Canvas, cx: int, head_y: int):
        hair_color = self.current["hair"]
        style = self.current["hair_style"]
        if style == "Soft Fringe":
            canvas.create_arc(
                cx - 60,
                head_y - 72,
                cx + 60,
                head_y + 32,
                start=0,
                extent=180,
                fill=hair_color,
                outline=hair_color,
            )
            canvas.create_rectangle(
                cx - 55, head_y - 25, cx + 55, head_y - 5, fill=hair_color, outline=""
            )
        elif style == "Bob Cut":
            canvas.create_oval(
                cx - 62, head_y - 68, cx + 62, head_y + 22, fill=hair_color, outline=""
            )
            canvas.create_rectangle(
                cx - 58, head_y - 18, cx + 58, head_y - 2, fill=hair_color, outline=""
            )
        elif style == "Twin Tails":
            canvas.create_oval(
                cx - 50, head_y - 68, cx + 50, head_y + 14, fill=hair_color, outline=""
            )
            canvas.create_oval(
                cx - 84, head_y - 5, cx - 54, head_y + 62, fill=hair_color, outline=""
            )
            canvas.create_oval(
                cx + 54, head_y - 5, cx + 84, head_y + 62, fill=hair_color, outline=""
            )
        elif style == "Side Part":
            canvas.create_oval(
                cx - 60, head_y - 68, cx + 60, head_y + 18, fill=hair_color, outline=""
            )
            canvas.create_polygon(
                cx - 10,
                head_y - 56,
                cx + 52,
                head_y - 12,
                cx + 16,
                head_y - 2,
                fill=hair_color,
                outline="",
            )
        else:  # Messy Fluff
            canvas.create_oval(
                cx - 62, head_y - 72, cx + 62, head_y + 16, fill=hair_color, outline=""
            )
            for offset in (-38, -16, 8, 28):
                canvas.create_polygon(
                    cx + offset,
                    head_y - 60,
                    cx + offset + 8,
                    head_y - 88,
                    cx + offset + 18,
                    head_y - 56,
                    fill=hair_color,
                    outline="",
                )

    def draw_accessory(self, canvas: tk.Canvas, cx: int, head_y: int):
        color = self.current["accessory"]
        accessory_type = self.current["accessory_type"]
        if accessory_type == "Heart Clip":
            canvas.create_text(
                cx + 42,
                head_y - 25,
                text="❤",
                fill=color,
                font=("Segoe UI Emoji", 18, "bold"),
            )
        elif accessory_type == "Star Clip":
            canvas.create_text(
                cx + 42,
                head_y - 25,
                text="★",
                fill=color,
                font=("Segoe UI Symbol", 18, "bold"),
            )
        elif accessory_type == "Bow":
            canvas.create_polygon(
                cx + 24,
                head_y - 30,
                cx + 42,
                head_y - 18,
                cx + 24,
                head_y - 6,
                fill=color,
                outline="",
            )
            canvas.create_polygon(
                cx + 60,
                head_y - 30,
                cx + 42,
                head_y - 18,
                cx + 60,
                head_y - 6,
                fill=color,
                outline="",
            )
            canvas.create_oval(
                cx + 38, head_y - 22, cx + 46, head_y - 14, fill="#f1f1f1", outline=""
            )
        elif accessory_type == "Choker":
            canvas.create_rectangle(
                cx - 22, head_y + 36, cx + 22, head_y + 44, fill=color, outline=""
            )
            canvas.create_oval(
                cx - 3, head_y + 39, cx + 3, head_y + 45, fill="#f8f9fa", outline=""
            )
        else:  # Glasses
            canvas.create_oval(
                cx - 24, head_y - 14, cx - 2, head_y + 8, outline=color, width=3
            )
            canvas.create_oval(
                cx + 2, head_y - 14, cx + 24, head_y + 8, outline=color, width=3
            )
            canvas.create_line(
                cx - 2, head_y - 3, cx + 2, head_y - 3, fill=color, width=3
            )

    def draw_arms(self, canvas: tk.Canvas, cx: int, head_y: int):
        # Arm lines are mirrored around center for each pose.
        arm_points = {
            "Shy": ((-60, 90, -95, 130), (60, 90, 95, 130)),
            "Confident": ((-60, 100, -120, 100), (60, 100, 120, 100)),
            "Cheerful": ((-60, 100, -110, 50), (60, 100, 110, 50)),
            "Wave": ((-60, 96, -112, 96), (60, 100, 108, 48)),
            "Hands Up": ((-56, 94, -84, 32), (56, 94, 84, 32)),
            "Crossed Arms": ((-58, 110, 24, 128), (58, 110, -24, 128)),
        }
        for x1, y1, x2, y2 in arm_points[self.current["pose"]]:
            canvas.create_line(
                cx + x1,
                head_y + y1,
                cx + x2,
                head_y + y2,
                width=12,
                fill=self.current["skin"],
                smooth=True,
            )


def main():
    root = tk.Tk()
    app = FemboyDressupGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
