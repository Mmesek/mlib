def import_from(dirname: str):
    """Recursively imports modules from specified directory"""
    import importlib, time, pkgutil, sys, os
    from platform import python_version_tuple as ver
    from .logger import log

    t = time.time()
    all_dirnames = [dirname] + [
        os.path.join(dirname, o)
        for o in os.listdir(dirname)
        if os.path.isdir(os.path.join(dirname, o)) and "__" not in o
    ]
    times = set()
    path = os.getcwd().replace("\\", "/")
    for importer, package_name, _ in pkgutil.iter_modules(all_dirnames):
        _t = time.time_ns()
        full_package_name = ".".join(
            [importer.path.replace("\\", "/").replace(path + "/", "").replace("/", "."), package_name]
        )
        if full_package_name not in sys.modules:
            try:
                importlib.import_module(full_package_name)
                log.debug("Imported %s", full_package_name)
            except ImportError as ex:
                log.exception(ex, exc_info=ex)
        times.add((package_name, time.time_ns() - _t))
    f = time.time()
    if times:
        longest = len(max(times, key=lambda x: len(x[0]))[0])
        times = sorted(times, key=lambda x: x[1], reverse=True)
        log.log(
            1, "Times in ns:\n%s", "\n".join("{:-<{longest}}-{}".format(i[0], i[1], longest=longest) for i in times)
        )
    log.info("%s Loaded in %s", dirname, f - t)


def import_modules(dirname: str):
    """Imports modules/packages from specified directory"""
    import importlib, time, pkgutil, sys, os
    from .logger import log

    t = time.time()
    if not os.path.exists(dirname):
        log.debug("Couldn't find %s. Not importing anything", dirname)
        return
    times = set()
    for _, package_name, _ in pkgutil.iter_modules([dirname]):
        _t = time.time_ns()
        full_package_name = ".".join([dirname.replace("\\", ".").replace("/", "."), package_name])
        if full_package_name not in sys.modules:
            try:
                importlib.import_module(full_package_name)
                log.debug("Imported %s", full_package_name)
            except ImportError as ex:
                log.exception(ex, exc_info=ex)
        times.add((package_name, time.time_ns() - _t))
    f = time.time()
    if times:
        longest = len(max(times, key=lambda x: len(x[0]))[0])
        times = sorted(times, key=lambda x: x[1], reverse=True)
        log.log(
            1, "Times in ns:\n%s", "\n".join("{:-<{longest}}-{}".format(i[0], i[1], longest=longest) for i in times)
        )
    log.info("%s Loaded in %s", dirname, f - t)
