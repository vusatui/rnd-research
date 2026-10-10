"""Exercise 2: LLM tool-call loop; the model's code runs only inside an E2B sandbox.

LLM: any OpenAI-compatible endpoint, OpenRouter free models by default.
  OPENROUTER_API_KEY  - required
  EX2_MODEL           - optional, default nvidia/nemotron-3-super-120b-a12b:free
  LLM_BASE_URL        - optional, default https://openrouter.ai/api/v1
"""
import json, os, sys
from dotenv import load_dotenv
from openai import OpenAI
from e2b_code_interpreter import Sandbox

load_dotenv()
client = OpenAI(base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
                api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = os.getenv("EX2_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")  # needs tool calling
TOOLS = [{"type": "function", "function": {
    "name": "run_python", "description": "Execute Python in an isolated sandbox, returns stdout/stderr/result",
    "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}}]

def run(task: str, max_steps: int = 8):
    msgs = [{"role": "system", "content": "You are a data agent. Use run_python for any computation."},
            {"role": "user", "content": task}]
    with Sandbox.create(timeout=300) as sbx:
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
                ex = sbx.run_code(code)
                out = {"stdout": ex.logs.stdout, "stderr": ex.logs.stderr,
                       "result": ex.text, "error": str(ex.error) if ex.error else None}
                msgs.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(out)[:8000]})
    return "max steps reached"

if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:]) or "Generate 1000 random numbers from N(5,2), compute the mean and std, and test the hypothesis mean=5"))
