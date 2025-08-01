import ttkbootstrap as tb
from tkinter import ttk
import tkinter as tk
import serial
import serial.tools.list_ports
import time
import threading
import math
import random

class AutoBluetoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛰️ LiSat-1 Ground Station")
        self.style = tb.Style("darkly")

        self.serial_port = None
        self.baud_rate = 9600
        self.is_connected = False

        self.build_ui()
        self.monitor_connection_loop()

    def build_ui(self):
        top = tb.Frame(self.root)
        top.pack(fill="both", expand=True)
        icons = [
        "🛰️",  # Satellite
        "🚀",  # Rocket
        "🛸",  # Flying Saucer
        "🌌",  # Milky Way
        "🌍",  # Earth Globe Europe-Africa
        "🌎",  # Earth Globe Americas
        "🌏",  # Earth Globe Asia-Australia
        "👽",  # Alien Face
        "📡",  # Satellite Antenna
        "🔭",  # Telescope
        "🪐",  # Ringed Planet (Saturn)
        "🌠",  # Shooting Star
        "☄️",  # Comet
        "🧭",  # Compass
        "📶",  # Signal Strength
        "🔌",  # Electric Plug
        "⚡",   # High Voltage
        "🔧",  # Wrench (maintenance/tools)
        "🖥️",  # Desktop Computer (monitor)
        "💡",  # Light Bulb (ideas/power)
        "📈",  # Chart Increasing (signal data)
        "📊",  # Bar Chart (monitoring)
        "⚙️",  # Gear (settings/mechanics)
        "🛰️",  # Another Satellite (repeat intentionally for balance)
        ]
        # Satellite icon that changes color
        self.satellite_label = tk.Label(top, text=random.choice(icons), font=("Segoe UI Emoji", 70), fg="white")
        self.satellite_label.pack(pady=(15,5))

        tk.Label(top, text="Solar Panel Angle", font=("Segoe UI", 20, "bold")).pack()

        com_frame = tb.Frame(top)
        com_frame.pack(pady=5)
        tk.Label(com_frame, text="COM Port:", font=("Segoe UI", 12)).pack(side="left", padx=(0,10))
        self.port_combo = ttk.Combobox(com_frame, width=20, state="readonly", font=("Segoe UI",11))
        self.port_combo.pack(side="left", padx=(0,10))
        self.refresh_ports()
        tb.Button(com_frame, text="🔌 Connect", bootstyle="success", command=self.manual_connect).pack(side="left", padx=(0,5))
        tb.Button(com_frame, text="🔍 Auto Connect", bootstyle="primary", command=self.auto_connect).pack(side="left")

        inp = tb.Frame(top)
        inp.pack(pady=10)
        self.angle_entry = tb.Entry(inp, width=5, font=("Segoe UI", 28, "bold"), justify="center")
        self.angle_entry.insert(0,"0")
        self.angle_entry.pack(side="left", padx=(0,15))
        self.send_btn = tb.Button(inp, text="Send 🚀", bootstyle="success",
                                  width=10, command=self.send_angle, state="disabled")
        self.send_btn.pack(side="left")

        self.gauge = tk.Canvas(top, width=240, height=130, bg="#222222", highlightthickness=0)
        self.gauge.pack(pady=20)
        self.draw_gauge_background()

        log_frame = tb.Labelframe(self.root, text="📜 Logs", bootstyle="primary", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0,10))
        self.log_text = tk.Text(log_frame, height=8, font=("Consolas",10),
                                 wrap="word", bg="#222831", fg="#eeeeee",
                                 insertbackground="#eeeeee", relief="flat", borderwidth=10)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")

        self.status_var = tk.StringVar(value="🔌 Select or auto‑connect COM port")
        self.status_lbl = tk.Label(self.root, textvariable=self.status_var,
                                   font=("Segoe UI",12,"bold"), fg="#f1c40f",
                                   bg=self.style.colors.bg)
        self.status_lbl.pack(fill="x", pady=5)

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_combo['values'] = [p.device for p in ports]
        if ports:
            self.port_combo.current(0)

    def manual_connect(self):
        port = self.port_combo.get()
        if not port:
            self.log("⚠️ No COM port selected.", color="orange")
            return
        try:
            ser = serial.Serial(port, self.baud_rate, timeout=1, write_timeout=1)
            self.serial_port = ser
            self.is_connected = True
            self.send_btn.config(state="normal")
            self.update_status(f"✅ Connected to {port}", "lime")
            self.log(f"✅ Manually connected to {port}", color="lime")
            self.set_satellite_color("#00ff00")
        except Exception as e:
            self.log(f"❌ Failed to connect to {port}: {e}", color="red")
            self.update_status("❌ Manual connect failed", "red")
            self.set_satellite_color("white")
            try: ser.close()
            except: pass

    def auto_connect(self):
        self.refresh_ports()
        ports = self.port_combo['values']
        if not ports:
            self.log("⚠️ No COM ports found.", color="orange")
            return

        self.log("🔍 Attempting auto-connect...", color="yellow")
        for p in ports:
            try:
                ser = serial.Serial(p, self.baud_rate, timeout=1, write_timeout=1)
                ser.write(b"0\n")
                time.sleep(0.2)
                self.serial_port = ser
                self.is_connected = True
                self.send_btn.config(state="normal")
                self.update_status(f"✅ Connected to {p}", "lime")
                self.log(f"✅ Auto-connected to {p}", color="lime")
                self.port_combo.set(p)
                self.set_satellite_color("#00ff00")
                return
            except Exception as e:
                self.log(f"❌ {p} failed: {e}", color="red")
                try: ser.close()
                except: pass

        self.update_status("❌ Auto-connect failed", "red")
        self.log("⚠️ None of the ports responded. Use manual option.", color="orange")
        self.set_satellite_color("white")

    def monitor_connection_loop(self):
        def loop():
            while True:
                if self.serial_port:
                    try:
                        self.serial_port.write(b"")
                    except Exception as e:
                        self.handle_disconnect()
                        self.log(f"❌ Disconnected: {e}", color="red")
                        self.send_btn.config(state="disabled")
                time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()

    def handle_disconnect(self):
        if self.is_connected:
            self.is_connected = False
            try:
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.close()
            except:
                pass
            self.serial_port = None
            self.update_status("❌ Disconnected", "red")
            self.log("🔌 Connection lost.", color="red")
            self.send_btn.config(state="disabled")
            self.set_satellite_color("white")

    def send_angle(self):
        def task():
            try:
                angle = int(self.angle_entry.get())
                angle = max(0, min(90, angle))
            except:
                self.log("⚠️ Enter integer 0–90!", color="orange")
                return

            if self.serial_port and self.serial_port.is_open:
                try:
                    self.serial_port.write(f"{angle}\n".encode())
                    self.log(f"📤 Sent angle: {angle}", color="cyan")
                    self.update_gauge(angle)
                except Exception as e:
                    self.log(f"❌ Send error: {e}", color="red")
                    self.handle_disconnect()
            else:
                self.log("⚠️ Not connected!", color="orange")

        threading.Thread(target=task, daemon=True).start()

    def update_status(self, msg, color):
        self.status_var.set(msg)
        self.status_lbl.config(fg={"red":"#e74c3c","lime":"#1abc9c","orange":"#e67e22"}.get(color,color))

    def log(self, msg, color="#eeeeee"):
        self.log_text.config(state="normal")
        tag = f"tag_{color}"
        self.log_text.insert("end", msg+"\n", (tag,))
        self.log_text.tag_config(tag, foreground=color)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def draw_gauge_background(self):
        c = self.gauge
        c.delete("all")
        cx, cy, r = 120,120,90
        c.create_arc(cx-r, cy-r, cx+r, cy+r, start=180, extent=90, style="arc", width=10, outline="#555555")
        for deg in range(0,91,15):
            rad = math.radians(180-deg)
            x1 = cx+(r-10)*math.cos(rad); y1 = cy-(r-10)*math.sin(rad)
            x2 = cx+(r+5)*math.cos(rad); y2 = cy-(r+5)*math.sin(rad)
            c.create_line(x1,y1,x2,y2, fill="#888888", width=1)
            xt = cx+(r+15)*math.cos(rad); yt = cy-(r+15)*math.sin(rad)
            ox, oy = (-7,0) if deg==0 else (0,-7) if deg==90 else (-5,-5) if deg==45 else (0,0)
            c.create_text(xt+ox, yt+oy, text=str(deg), fill="#ccc", font=("Segoe UI",8,"bold"))
        c.create_oval(cx-10, cy-10, cx+10, cy+10, fill="#333333", outline="")

    def update_gauge(self, angle):
        c = self.gauge
        c.delete("needle")
        angle = max(0, min(90, angle))
        rad = math.radians(180-angle)
        x0, y0 = 120, 120
        x1 = x0+75*math.cos(rad); y1 = y0-75*math.sin(rad)
        c.create_line(x0, y0, x1, y1, fill="#00ffff", width=3, tag="needle")
        c.create_oval(x0-5, y0-5, x0+5, y0+5, fill="#00ffff", outline="", tag="needle")
        c.delete("angle_text")
        c.create_text(x0, y0+30, text=f"{angle}°", fill="#00ffff",
                      font=("Segoe UI",18,"bold"), tag="angle_text")

    def set_satellite_color(self, color):
        self.satellite_label.config(fg=color)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    AutoBluetoothApp(root)
    root.mainloop()
