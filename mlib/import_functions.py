def import_from(dirname: str):
    import importlib, time, pkgutil, sys, os
    t = time.time()
    dirname = [dirname]+[os.path.join(dirname,o) for o in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, o)) and '__' not in o]
    times = set()
    for importer, package_name, _ in pkgutil.iter_modules(dirname):
        _t = time.time_ns()
        full_package_name = '.'.join([importer.path.replace('\\','.').replace('/','.'), package_name])
        if full_package_name not in sys.modules:
            importlib.import_module(full_package_name)
        times.add((package_name, time.time_ns()-_t))
    f = time.time()
    from .logger import log
    longest = len(max(times, key=lambda x: len(x[0]))[0])
    times = sorted(times, key=lambda x: x[1], reverse=True)
    log.log(1, "Times in ns:\n%s", "\n".join("{:-<{longest}}-{}".format(i[0], i[1], longest=longest) for i in times))
    log.info("%s Loaded in %s", dirname, f-t)
