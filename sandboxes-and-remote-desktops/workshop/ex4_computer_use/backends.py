"""Desktop backends with one interface: screenshot() -> PNG bytes, click/type/key/scroll/move.
Select with DESKTOP_BACKEND=docker|e2b."""
import os, sys, time

class DockerBackend:
    """The ex3 container (agent-desktop). Start it first:
    docker run --rm -d --name desk -p 127.0.0.1:6080:6080 --shm-size=1g agent-desktop"""
    def __init__(self, name=None):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ex3_docker_desktop"))
        from desktop_tools import DockerDesktop
        self.d = DockerDesktop(name or os.getenv("DOCKER_DESKTOP_NAME", "desk"))
        self.live_url = "http://localhost:6080/vnc.html"
    def screenshot(self): return self.d.screenshot()
    def click(self, x, y, button="left", double=False):
        if double: self.d.double_click(x, y)
        elif button == "right": self.d.right_click(x, y)
        else: self.d.left_click(x, y)
    def move(self, x, y): self.d.move_mouse(x, y)
    def type(self, text): self.d.write(text)
    def key(self, combo): self.d.press(combo)          # xdotool syntax: "ctrl+l", "Return"
    def scroll(self, direction, amount): self.d.scroll(direction, amount)
    def close(self): pass                              # container lifecycle is yours

class E2BBackend:
    """E2B Desktop cloud sandbox (needs E2B_API_KEY)."""
    def __init__(self, resolution=(1280, 800)):
        from e2b_desktop import Sandbox
        self.d = Sandbox.create(resolution=resolution, timeout=900)
        self.d.stream.start()
        self.live_url = self.d.stream.get_url()
    def screenshot(self): return bytes(self.d.screenshot())
    def click(self, x, y, button="left", double=False):
        if double: self.d.double_click(x, y)
        elif button == "right": self.d.right_click(x, y)
        else: self.d.left_click(x, y)
    def move(self, x, y): self.d.move_mouse(x, y)
    def type(self, text): self.d.write(text)
    def key(self, combo):
        keys = combo.split("+"); self.d.press(keys if len(keys) > 1 else keys[0])
    def scroll(self, direction, amount): self.d.scroll(direction, amount)
    def close(self): self.d.kill()

def make_backend(name=None):
    name = (name or os.getenv("DESKTOP_BACKEND", "docker")).lower()
    return {"docker": DockerBackend, "e2b": E2BBackend}[name]()

def wait(seconds): time.sleep(min(float(seconds), 10))
