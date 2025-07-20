import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from datetime import datetime
from itertools import cycle
import random

class SkyHexPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KREDIX CORP")
        self.geometry("700x700")
        self.configure(bg="#121212")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.setup_styles()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.anim_running = True

    def setup_styles(self):
        self.style.configure("TLabel", background="#121212", foreground="#00ffcc", font=("Segoe UI", 12))
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"))
        self.style.configure("Section.TLabelframe", background="#1E1E1E", foreground="#00ffcc", font=("Segoe UI", 14, "bold"))
        self.style.configure("Toggle.TCheckbutton",
                             background="#121212", foreground="#00ffcc", font=("Segoe UI", 11),
                             focuscolor="none")
        self.style.map('Toggle.TCheckbutton',
                       background=[('selected', '#00cc66')],
                       foreground=[('selected', 'black')])
        self.style.configure("TNotebook", background="#121212", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#222222", foreground="#00ffcc", font=("Segoe UI", 12, "bold"), padding=[12,8])
        self.style.map("TNotebook.Tab", background=[("selected", "#00cc66")], foreground=[("selected", "#121212")])
        self.style.configure("TButton", font=("Segoe UI", 13, "bold"), padding=10)

    def create_widgets(self):
        header = ttk.Label(self, text="KREDIX CORP", style="Header.TLabel")
        header.pack(pady=(10, 5))

        info = ttk.Label(self, text="AIMFUCK", font=("Segoe UI", 10, "italic"))
        info.pack()

        license_frame = ttk.Frame(self, padding=10, style="Section.TLabelframe")
        license_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(license_frame, text="License Key:").pack(side="left", padx=5)
        self.license_var = tk.StringVar()
        self.license_entry = ttk.Entry(license_frame, textvariable=self.license_var, width=30)
        self.license_entry.pack(side="left", padx=5)
        self.validate_btn = ttk.Button(license_frame, text="Validate License", command=self.validate_license)
        self.validate_btn.pack(side="left", padx=10)

        status_frame = ttk.Frame(self, style="Section.TLabelframe")
        status_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(status_frame, text="Server Status:").pack(side="left", padx=5)
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20, highlightthickness=0, bg="#121212")
        self.status_canvas.pack(side="left")
        self.status_indicator = self.status_canvas.create_oval(3, 3, 17, 17, fill="red")
        self.status_text = ttk.Label(status_frame, text="Disconnected", foreground="red", background="#121212")
        self.status_text.pack(side="left", padx=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=10)

        self.aimbot_tab = ttk.Frame(self.notebook)
        self.visual_tab = ttk.Frame(self.notebook)
        self.misc_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.aimbot_tab, text="🎯 Aimbot")
        self.notebook.add(self.visual_tab, text="👁️ Visual")
        self.notebook.add(self.misc_tab, text="⚙️ Misc")

        self.create_aimbot_tab()
        self.create_visual_tab()
        self.create_misc_tab()

        self.log_box = tk.Text(self, height=10, bg="#0f0f0f", fg="#00ff00",
                               font=("Consolas", 11), bd=0, relief="sunken", state="disabled")
        self.log_box.pack(fill="both", padx=20, pady=(0, 10))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(padx=20, pady=(0, 20), fill="x")

        self.save_logs_btn = ttk.Button(btn_frame, text="💾 Save Logs", command=self.save_logs)
        self.save_logs_btn.pack(side="left")

        self.activate_btn = ttk.Button(btn_frame, text="▶ Inject & Activate", command=self.on_activate)
        self.activate_btn.pack(side="right")

        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=(0,10))

        self.injecting_label = ttk.Label(self, text="", font=("Segoe UI", 14, "bold"), foreground="#00ffcc", background="#121212")
        self.injecting_label.pack(pady=(0, 10))

        footer = ttk.Label(self, text="SKYHEX CrackTool v6.9 | Simulation Build - Do NOT use in real games.",
                           font=("Segoe UI", 8), foreground="#666666", background="#121212")
        footer.pack(side="bottom", pady=5)

        self.license_valid = False
        self.server_connected = False

        self.connect_to_server()

    def create_aimbot_tab(self):
        cheats = [
            "Enable Aimbot",
            "Triggerbot",
            "No Recoil",
            "No Spread",
            "Silent Aim"
        ]
        self.aimbot_toggles = []
        for cheat in cheats:
            toggle = ttk.Checkbutton(self.aimbot_tab, text=cheat, style="Toggle.TCheckbutton")
            toggle.var = tk.BooleanVar()
            toggle.config(variable=toggle.var)
            toggle.pack(anchor="w", padx=20, pady=5)
            self.aimbot_toggles.append(toggle)

    def create_visual_tab(self):
        cheats = [
            "Wallhack / ESP",
            "Radar Hack",
            "Skin Unlocker",
            "Chams",
            "Glow Hack",
            "Third Person View",
            "Crosshair Overlay"
        ]
        self.visual_toggles = []
        for cheat in cheats:
            toggle = ttk.Checkbutton(self.visual_tab, text=cheat, style="Toggle.TCheckbutton")
            toggle.var = tk.BooleanVar()
            toggle.config(variable=toggle.var)
            toggle.pack(anchor="w", padx=20, pady=5)
            self.visual_toggles.append(toggle)

    def create_misc_tab(self):
        cheats = [
            "Speedhack",
            "Teleport Hack",
            "Packet Editor",
            "DLL Injector",
            "Fake Currency Injector",
            "Fly / Noclip",
            "Macro / Script Hack",
            "Anti-Ban Spoofer (Fake)"
        ]
        self.misc_toggles = []
        for cheat in cheats:
            toggle = ttk.Checkbutton(self.misc_tab, text=cheat, style="Toggle.TCheckbutton")
            toggle.var = tk.BooleanVar()
            toggle.config(variable=toggle.var)
            toggle.pack(anchor="w", padx=20, pady=5)
            self.misc_toggles.append(toggle)

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state="disabled")

    def save_logs(self):
        logs = self.log_box.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(
            title="Save Logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, "w") as f:
                f.write(logs)
            messagebox.showinfo("Save Logs", f"Logs saved to:\n{filename}")

    def validate_license(self):
        key = self.license_var.get().strip()
        if len(key) == 16 and key.isalnum():
            self.license_valid = True
            self.log(f"License key '{key}' validated successfully.")
            messagebox.showinfo("License Validation", "License is valid!")
        else:
            self.license_valid = False
            self.log(f"License key '{key}' is invalid.")
            messagebox.showerror("License Validation", "Invalid license key.")

    def connect_to_server(self):
        def run():
            dots_cycle = cycle(["", ".", "..", "..."])
            while self.anim_running:
                self.status_text.config(text=f"Connecting{next(dots_cycle)}", foreground="yellow")
                time.sleep(0.7)
                if random.random() > 0.3:
                    self.server_connected = True
                    self.status_canvas.itemconfig(self.status_indicator, fill="green")
                    self.status_text.config(text="Connected", foreground="lime")
                else:
                    self.server_connected = False
                    self.status_canvas.itemconfig(self.status_indicator, fill="red")
                    self.status_text.config(text="Disconnected", foreground="red")
                time.sleep(4)
        threading.Thread(target=run, daemon=True).start()

    def on_activate(self):
        if not self.license_valid:
            messagebox.showwarning("License Error", "Please validate your license key first!")
            self.log("Attempted activation without valid license.")
            return
        if not self.server_connected:
            messagebox.showwarning("Server Error", "Cannot activate cheats while disconnected from server.")
            self.log("Activation failed: server disconnected.")
            return

        enabled = []
        for toggle in self.aimbot_toggles + self.visual_toggles + self.misc_toggles:
            if toggle.var.get():
                enabled.append(toggle.cget("text"))

        if not enabled:
            messagebox.showwarning("No Cheats Enabled", "Please select at least one cheat module to activate.")
            self.log("Activate pressed with no cheats selected.")
            return

        self.activate_btn.config(state="disabled")
        self.license_entry.config(state="disabled")
        self.validate_btn.config(state="disabled")
        self.save_logs_btn.config(state="disabled")
        self.progress["value"] = 0

        threading.Thread(target=self.simulate_injection, args=(enabled,), daemon=True).start()

    def simulate_injection(self, enabled):
        self.log("Starting injection sequence...")

        steps = [
            ("Connecting to SKYHEX Cloud Servers", 15),
            ("Verifying license key", 25),
            ("Injecting cheat modules", 15),
            ("Activating cheat modules", 35),
            ("Finalizing injection", 10)
        ]

        for text, percent in steps:
            self.log(text + "...")
            self.animate_injecting_text(text, percent)
            for _ in range(percent):
                time.sleep(0.05)
                self.progress["value"] += 1
                self.progress.update()

        self.injecting_label.config(text="DLL Injection Complete ✔", foreground="#00cc66")
        self.injecting_label.update()

        for cheat in enabled:
            self.log(f"Activating {cheat} ...")
            time.sleep(0.4)
            self.log(f"✔ {cheat} activated successfully.")

        self.log("Injection sequence complete.")
        self.progress["value"] = 100

        self.activate_btn.config(state="normal")
        self.license_entry.config(state="normal")
        self.validate_btn.config(state="normal")
        self.save_logs_btn.config(state="normal")

        self.injecting_label.config(text="", foreground="#00ffcc")

    def animate_injecting_text(self, base_text, duration_percent):
        # Animate blinking text with cycling dots for the duration of the step
        total_steps = duration_percent
        dots_cycle = cycle(["", ".", "..", "..."])
        for _ in range(total_steps):
            if not self.anim_running:
                break
            dots = next(dots_cycle)
            # Blink color every other step
            if _ % 2 == 0:
                fg_color = "#00ffcc"
            else:
                fg_color = "#008877"
            self.injecting_label.config(text=f"{base_text}{dots}", foreground=fg_color)
            time.sleep(0.05)

    def on_closing(self):
        self.anim_running = False
        if messagebox.askokcancel("Quit", "Are you sure you want to exit KREDIX INJECTOR?"):
            self.destroy()

if __name__ == "__main__":
    app = SkyHexPanel()
    app.mainloop()
