def warn(*args, **kwards):
    
    for object in args:
        print(f"\x1b[33;20m{object}\x1b[0m", **kwargs)
        

def log(object, **kwargs):

    if "end" in kwargs:
        del kwargs["end"]

    print(f"{object}{' '*100}", **kwargs, end='\r')
 
