"""Adapter: computer-use interface on top of a self-hosted container."""
import subprocess

class DockerDesktop:
    def __init__(self, name="desk"):
        self.name = name
    def _x(self, cmd: str) -> bytes:
        return subprocess.run(["docker", "exec", "-e", "DISPLAY=:1", self.name, "bash", "-lc", cmd],
                              capture_output=True, check=True).stdout
    def screenshot(self) -> bytes:
        return self._x("scrot -o /tmp/s.png && cat /tmp/s.png")
    def left_click(self, x, y): self._x(f"xdotool mousemove {x} {y} click 1")
    def right_click(self, x, y): self._x(f"xdotool mousemove {x} {y} click 3")
    def move_mouse(self, x, y): self._x(f"xdotool mousemove {x} {y}")
    def double_click(self, x, y): self._x(f"xdotool mousemove {x} {y} click --repeat 2 1")
    def write(self, text): subprocess.run(["docker", "exec", "-e", "DISPLAY=:1", self.name, "xdotool", "type", "--delay", "20", text], check=True)
    def press(self, key):
        if isinstance(key, list): key = "+".join(key)
        self._x(f"xdotool key {key}")
    def wait(self, ms): import time; time.sleep(ms / 1000)
    def scroll(self, direction, amount=3): self._x(f"xdotool click --repeat {amount} {4 if direction=='up' else 5}")
    def launch(self, app): self._x(f"nohup {app} >/dev/null 2>&1 &")
