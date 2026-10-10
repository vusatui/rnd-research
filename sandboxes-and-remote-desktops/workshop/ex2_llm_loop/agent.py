"""Exercise 2: LLM tool-call loop; code runs only inside the sandbox."""
import json, sys
from dotenv import load_dotenv
from openai import OpenAI
from e2b_code_interpreter import Sandbox

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"  # any model with tool calling
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
                code = json.loads(tc.function.arguments)["code"]
                print("\n--- code ---\n", code)
                ex = sbx.run_code(code)
                out = {"stdout": ex.logs.stdout, "stderr": ex.logs.stderr,
                       "result": ex.text, "error": str(ex.error) if ex.error else None}
                msgs.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(out)[:8000]})
    return "max steps reached"

if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:]) or "Generate 1000 random numbers from N(5,2), compute the mean and std, and test the hypothesis mean=5"))
