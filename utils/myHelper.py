def after_exec(res, text):
    if res == 0:
        print(">> [SUCCESS] ", end='')
    else:
        print(">> [FAIL] ", end='')
    print(text)

def check_dir(dir):
    if not dir.exists():
        dir.mkdir()

def check_num(num):
    if num is not None:
        return 1
    else:
        return 0