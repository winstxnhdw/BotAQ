warn = lambda *args, **kwargs : [print(f"\x1b[33;20m{object}\x1b[0m", **kwargs) for object in args]

def log(object, **kwargs):

    if "end" in kwargs:
        del kwargs["end"]

    print(f"{object}{' '*100}", **kwargs, end='\r')