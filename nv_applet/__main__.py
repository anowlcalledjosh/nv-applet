#!/usr/bin/env python3


import collections
from enum import Enum
from pathlib import Path
import subprocess
import threading

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GLib, Gtk
import indicator_applet


class PowerState(Enum):
    OFF = object()
    ON = object()


class Gpu(Enum):
    INTEL = object()
    NVIDIA = object()


GPU_NAMES = {
    Gpu.INTEL: "Intel",
    Gpu.NVIDIA: "nvidia",
    None: "Unknown",
}


POWER_NAMES = {
    PowerState.ON: "on",
    PowerState.OFF: "off",
    None: "unknown",
}


class NVApplet(indicator_applet.Applet):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.items = collections.OrderedDict(
            status=Gtk.MenuItem("Status:"),
            sep0=Gtk.SeparatorMenuItem(),
            gpu_on=Gtk.MenuItem("Turn GPU on"),
            gpu_off=Gtk.MenuItem("Turn GPU off"),
            sep1=Gtk.SeparatorMenuItem(),
            switch_intel=Gtk.MenuItem("Switch to Intel graphics"),
            switch_nvidia=Gtk.MenuItem("Switch to Nvidia graphics"),
            sep2=Gtk.SeparatorMenuItem(),
            quit=Gtk.MenuItem("Quit"),
        )
        self.items["status"].set_sensitive(False)
        self.current_gpu = None
        self.nvidia_power_state = None
        self.lock = threading.RLock()
        self.update_interval = 10

    def schedule_update(self) -> None:
        with self.lock:
            process = subprocess.run(
                ["nvctl", "gpu", "query", "-q"], stdout=subprocess.PIPE
            )
            stdout = process.stdout.strip()
            if stdout == b"intel":
                gpu = Gpu.INTEL
            elif stdout == b"nvidia":
                gpu = Gpu.NVIDIA
            else:
                gpu = None

            process = subprocess.run(
                ["nvctl", "power", "query", "-q"], stdout=subprocess.PIPE
            )
            stdout = process.stdout.strip()
            if stdout == b"on":
                state = PowerState.ON
            elif stdout == b"off":
                state = PowerState.OFF
            else:
                state = None

            self.current_gpu = gpu
            self.nvidia_power_state = state

            GLib.idle_add(self.do_update, gpu, state)

    def do_update(self, gpu: Gpu, state: PowerState) -> None:
        super().do_update()

        label = f"GPU: {GPU_NAMES[self.current_gpu]}"
        if self.current_gpu is Gpu.NVIDIA:
            label += f" ({POWER_NAMES[self.nvidia_power_state]})"
        self.items["status"].set_label(label)

        self.indicator.icon = (
            "nv-applet-"
            + {
                Gpu.INTEL: "intel",
                Gpu.NVIDIA: "nvidia",
                None: "cpu-frequency-indicator",
            }[self.current_gpu]
            + {PowerState.ON: "", PowerState.OFF: "-symbolic", None: "",}[
                self.nvidia_power_state
            ]
        )

        if self.current_gpu is Gpu.INTEL:
            self.items["switch_intel"].set_sensitive(False)
            self.items["switch_nvidia"].set_sensitive(True)
        elif self.current_gpu is Gpu.NVIDIA:
            self.items["switch_intel"].set_sensitive(True)
            self.items["switch_nvidia"].set_sensitive(False)
        else:
            self.items["switch_intel"].set_sensitive(True)
            self.items["switch_nvidia"].set_sensitive(True)

        if self.nvidia_power_state is PowerState.ON:
            self.items["gpu_on"].set_sensitive(False)
            self.items["gpu_off"].set_sensitive(True)
        elif self.nvidia_power_state is PowerState.OFF:
            self.items["gpu_on"].set_sensitive(True)
            self.items["gpu_off"].set_sensitive(False)
        else:
            self.items["gpu_on"].set_sensitive(True)
            self.items["gpu_off"].set_sensitive(True)

    def handle_gpu_on(self, source) -> None:
        print("turning GPU on...")
        with self.lock:
            assert self.nvidia_power_state is PowerState.OFF, self.nvidia_power_state
            subprocess.run(["nvctl", "power", "on", "-q"], check=True)
            self.schedule_update()

    def handle_gpu_off(self, source) -> None:
        print("turning GPU off...")
        with self.lock:
            assert self.nvidia_power_state is PowerState.ON, self.nvidia_power_state
            subprocess.run(["nvctl", "power", "off", "-q"], check=True)
            self.schedule_update()

    def handle_switch_intel(self, source) -> None:
        print("switching to Intel graphics...")
        with self.lock:
            assert self.current_gpu is Gpu.NVIDIA, self.current_gpu
            subprocess.run(["nvctl", "gpu", "intel", "-q"], check=True)
            self.schedule_update()

    def handle_switch_nvidia(self, source) -> None:
        print("switching to Nvidia graphics...")
        with self.lock:
            assert self.current_gpu is Gpu.INTEL, self.current_gpu
            subprocess.run(["nvctl", "gpu", "nvidia", "-q"], check=True)
            self.schedule_update()


def main():
    NVApplet(
        "nv-applet",
        "cpu-frequency-indicator",
        indicator_applet.Category.HARDWARE,
        Path("/home/ash/src/nv-applet/").resolve().as_posix(),
    ).run()


if __name__ == "__main__":
    main()
