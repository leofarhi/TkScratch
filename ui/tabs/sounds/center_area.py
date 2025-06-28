import customtkinter as ctk
import tkinter as tk
import os
import time
import simpleaudio as sa
import wave
import numpy as np
from engine.Sound import Sound, test_sound

class SoundsArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.sound = test_sound

        self.is_playing = False
        self.wave_obj = None
        self.play_obj = None

        self.zoom_factor = 1.0
        self.min_zoom = 1.0

        self.play_position = 0.0
        self.volume = 1.0  # Volume par défaut à 100%

        self.waveform_id = None 

        top_bar = ctk.CTkFrame(self)
        top_bar.pack(fill="x", pady=10, padx=10)

        self.name_label = ctk.CTkLabel(top_bar, text="Sound")
        self.name_label.pack(side="left", padx=(5, 2), pady=5)
        self.name_entry = ctk.CTkEntry(top_bar, placeholder_text="Sound name")
        self.name_entry.insert(0, self.sound.name)
        self.name_entry.pack(side="left", padx=5, pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=800, height=220, orientation="horizontal")
        self.scrollable_frame.pack(fill="x", padx=10, pady=10)

        self.canvas = tk.Canvas(self.scrollable_frame, width=800, height=200, border=0, highlightthickness=0)
        self.canvas.pack(anchor="w")

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=10)

        self.play_btn = ctk.CTkButton(controls, text="▶", width=40, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=(5, 5), pady=5)

        #Barre de volume
        self.volume_slider = ctk.CTkSlider(controls, from_=0, to=1, number_of_steps=100, command=self.change_volume)
        self.volume_slider.set(1.0)  # 100% par défaut
        self.volume_slider.pack(side="left", padx=10, pady=5)

        self.zoom_out_btn = ctk.CTkButton(controls, text="➖", width=50, command=self.zoom_out)
        self.zoom_out_btn.pack(side="right", padx=5, pady=5)

        self.zoom_in_btn = ctk.CTkButton(controls, text="➕", width=50, command=self.zoom_in)
        self.zoom_in_btn.pack(side="right", padx=5, pady=5)

        self.canvas.bind("<Button-1>", self.seek_audio)
        self.samples = self.sound.get_waveform_data(5000)

        self.bind("<Configure>", self.on_resize)
        self._calc_min_zoom()
        self.zoom_factor = self.min_zoom
        self.draw_waveform()

        self.app.add_refresh(self.refresh)

    def change_volume(self, value):
        self.volume = float(value)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self._calc_min_zoom()
        if self.zoom_factor < self.min_zoom:
            self.zoom_factor = self.min_zoom
        self.draw_waveform()

    def refresh(self):
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][self.app._get_appearance_mode() == "dark"]
        self.canvas.configure(bg=bg_color)
        ###################
        self.name_label.configure(text=self.app.language_manager.get("sound.name"))
        self.name_entry.configure(placeholder_text=self.app.language_manager.get("sound.name_placeholder"))

    def _calc_min_zoom(self):
        self.scrollable_frame.update_idletasks()
        width = self.scrollable_frame._parent_canvas.winfo_width()
        raw_len = len(self.samples)
        self.min_zoom = (width / raw_len) - 0.001

    def on_resize(self, event):
        self._calc_min_zoom()
        if self.zoom_factor < self.min_zoom:
            self.zoom_factor = self.min_zoom
        self.draw_waveform()

    def toggle_play(self):
        if self.is_playing:
            self.stop_playback()
        else:
            self.start_playback()

    def start_playback(self):
        if not os.path.exists(self.sound.filepath):
            return
        try:
            wave_read = wave.open(self.sound.filepath, 'rb')
            frames = wave_read.readframes(wave_read.getnframes())
            samples = np.frombuffer(frames, dtype=np.int16)

            samples = (samples * self.volume).astype(np.int16)
            data = samples.tobytes()

            self.wave_obj = sa.WaveObject(data, wave_read.getnchannels(), wave_read.getsampwidth(),
                                          wave_read.getframerate())

            if self.play_position > 0.0:
                start_frame = int(self.play_position * wave_read.getnframes())
                wave_read.setpos(start_frame)
                frames = wave_read.readframes(wave_read.getnframes() - start_frame)
                samples = np.frombuffer(frames, dtype=np.int16)
                samples = (samples * self.volume).astype(np.int16)
                data = samples.tobytes()
                self.wave_obj = sa.WaveObject(data, wave_read.getnchannels(), wave_read.getsampwidth(),
                                              wave_read.getframerate())

            self.playback_start_time = time.time() - (self.play_position * self.sound.duration)
            self.play_obj = self.wave_obj.play()
            self.is_playing = True
            self.play_btn.configure(text="⏹")

            self.update_cursor()
            self.check_playing()

        except Exception as e:
            print(e)

    def stop_playback(self):
        if self.play_obj:
            self.play_obj.stop()
        self.is_playing = False
        self.play_btn.configure(text="▶")
        self.play_position = 0.0
        self.draw_waveform()

    def check_playing(self):
        if self.play_obj and self.play_obj.is_playing():
            self.after(100, self.check_playing)
        else:
            self.is_playing = False
            self.play_btn.configure(text="▶")
            self.play_position = 0.0
            self.draw_waveform()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.draw_waveform()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        if self.zoom_factor < self.min_zoom:
            self.zoom_factor = self.min_zoom
        self.draw_waveform()

    def draw_waveform(self):
        viewport_width = self.scrollable_frame._parent_canvas.winfo_width()
        raw_len = len(self.samples)
        self.min_zoom = (viewport_width / raw_len) - 0.001

        if self.zoom_factor < self.min_zoom:
            self.zoom_factor = self.min_zoom

        self._draw_waveform_base()
        self._draw_cursor()

    def _draw_waveform_base(self):
        total_samples = len(self.samples)
        h = int(self.canvas["height"])
        mid_y = h // 2

        max_amp = max(abs(self.samples)) or 1
        scaled = [s / max_amp for s in self.samples]

        zoomed_len_px = int(total_samples * self.zoom_factor)

        viewport_height = self.scrollable_frame._parent_canvas.winfo_height()
        self.canvas.config(width=zoomed_len_px, height=viewport_height)

        self.scrollable_frame.update_idletasks()

        points = []
        for i, s in enumerate(scaled):
            x = i * self.zoom_factor
            y = mid_y - s * (h // 2) * 0.9
            points.append((x, y))
        full_points = [(0, mid_y)] + points + [(zoomed_len_px, mid_y)]
        flat_points = [coord for point in full_points for coord in point]

        if self.waveform_id is None:
            self.waveform_id = self.canvas.create_polygon(flat_points, fill="#d28eff", outline="#a46ff2")
        else:
            self.canvas.coords(self.waveform_id, *flat_points)

    def _draw_cursor(self):
        total_samples = len(self.samples)
        zoomed_len_px = total_samples * self.zoom_factor
        cursor_x = self.play_position * zoomed_len_px
        h = int(self.canvas["height"])
        self.canvas.delete("cursor")
        self.canvas.create_line(cursor_x, 0, cursor_x, h, fill="red", width=2, tags="cursor")

    def update_cursor(self):
        if self.is_playing:
            elapsed = time.time() - self.playback_start_time
            self.play_position = min(elapsed / self.sound.duration, 1.0)
            self._draw_cursor()
            if self.play_position < 1.0:
                self.after(50, self.update_cursor)
            else:
                self.is_playing = False
                self.play_btn.configure(text="▶")
                self.play_position = 0.0
                self._draw_cursor()

    def seek_audio(self, event):
        click_x = self.canvas.canvasx(event.x)
        total_len_px = len(self.samples) * self.zoom_factor

        if self.is_playing:
            self.stop_playback()
            self.play_position = max(0.0, min(click_x / total_len_px, 1.0))
            self.start_playback()
        else:
            self.play_position = max(0.0, min(click_x / total_len_px, 1.0))
            self._draw_cursor()
