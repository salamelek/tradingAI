def progressBar(progress, iterLen, msg="", length=30, fill='█', prefix=''):
    ratio = iterLen / length
    barProg = int(progress / ratio)
    bar = fill * barProg + '-' * int(length - barProg)
    print(f'\r{msg}{prefix} |{bar}| {round(((progress / iterLen) * 100), 1)}% Complete', end="", flush=True)
