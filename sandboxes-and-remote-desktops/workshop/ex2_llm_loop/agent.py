"""Exercise 2: LLM tool-call loop; the model's code runs only inside an E2B sandbox.

LLM: any OpenAI-compatible endpoint, OpenRouter free models by default.
  OPENROUTER_API_KEY  - required
  EX2_MODEL           - optional, default nvidia/nemotron-3-super-120b-a12b:free
  LLM_BASE_URL        - optional, default https://openrouter.ai/api/v1
  SANDBOX_BACKEND     - e2b (default, needs E2B_API_KEY) | docker (local throwaway container)
"""
import json, os, sys
from dotenv import load_dotenv
from openai import OpenAI
import subprocess, uuid

load_dotenv()
client = OpenAI(base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
                api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = os.getenv("EX2_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")  # needs tool calling
TOOLS = [{"type": "function", "function": {
    "name": "run_python", "description": "Execute Python in an isolated sandbox, returns stdout/stderr/result",
    "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}}]

class DockerSandbox:
    """Local fallback: one locked-down container per session (no network, capped CPU/RAM/PIDs)."""
    def __init__(self, image=os.getenv("DOCKER_SANDBOX_IMAGE", "python:3.12-slim")):
        self.name = "ex2-" + uuid.uuid4().hex[:8]
        subprocess.run(["docker", "run", "-d", "--rm", "--name", self.name, "--network", "none",
                        "--memory", "512m", "--cpus", "1", "--pids-limit", "128", "--read-only",
                        "--tmpfs", "/tmp", "--user", "65534:65534", image, "sleep", "600"],
                       check=True, capture_output=True)
    def __enter__(self): return self
    def __exit__(self, *a): subprocess.run(["docker", "rm", "-f", self.name], capture_output=True)
    def run_code(self, code: str) -> dict:
        try:
            p = subprocess.run(["docker", "exec", "-i", self.name, "python", "-"], input=code,
                               capture_output=True, text=True, timeout=60)
            return {"stdout": p.stdout, "stderr": p.stderr, "result": None,
                    "error": None if p.returncode == 0 else f"exit code {p.returncode}"}
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "", "result": None, "error": "timeout after 60s"}

class E2BSandbox:
    def __init__(self):
        from e2b_code_interpreter import Sandbox
        self.sbx = Sandbox.create(timeout=300)
    def __enter__(self): return self
    def __exit__(self, *a): self.sbx.kill()
    def run_code(self, code: str) -> dict:
        ex = self.sbx.run_code(code)
        return {"stdout": ex.logs.stdout, "stderr": ex.logs.stderr,
                "result": ex.text, "error": str(ex.error) if ex.error else None}

def make_sandbox():
    return {"e2b": E2BSandbox, "docker": DockerSandbox}[os.getenv("SANDBOX_BACKEND", "e2b").lower()]()

def run(task: str, max_steps: int = 8):
    msgs = [{"role": "system", "content": "You are a data agent. Use run_python for any computation."},
            {"role": "user", "content": task}]
    with make_sandbox() as sbx:
        for _ in range(max_steps):
            resp = client.chat.completions.create(model=MODEL, messages=msgs, tools=TOOLS)
            m = resp.choices[0].message
            msgs.append(m.model_dump(exclude_none=True))  # a dict, not a pydantic object
            if not m.tool_calls:
                return m.content
            for tc in m.tool_calls:
                try:
                    code = json.loads(tc.function.arguments or "{}")["code"]
                except (json.JSONDecodeError, KeyError) as e:  # small free models sometimes emit bad JSON
                    msgs.append({"role": "tool", "tool_call_id": tc.id, "content": f"bad arguments: {e}"})
                    continue
                print("\n--- code ---\n", code)
                out = sbx.run_code(code)
                msgs.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(out)[:8000]})
    return "max steps reached"

if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:]) or "Generate 1000 random numbers from N(5,2), compute the mean and std, and test the hypothesis mean=5"))
