

def after_exec(res, text):
    if res == 0:
        print(">> [SUCCESS] ", end='')
    else:
        print(">> [FAIL] ", end='')
    print(text)

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()