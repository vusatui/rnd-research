"""Exercise 1: E2B sandbox lifecycle."""
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()
with Sandbox.create(timeout=120) as sbx:  # Firecracker microVM, dies after TTL
    ex = sbx.run_code("import platform, os; print(platform.uname()); print(os.getcwd())")
    print("stdout:", ex.logs.stdout)
    sbx.files.write("/home/user/data.csv", "x,y\n1,2\n3,4\n")
    ex = sbx.run_code("import pandas as pd; df=pd.read_csv('/home/user/data.csv'); df.sum()")
    print("result:", ex.text)
    r = sbx.commands.run("rm -rf /tmp/* && echo 'break whatever we want - the host is fine'")
    print(r.stdout)
