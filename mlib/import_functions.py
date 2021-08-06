def import_from(dirname: str):
    import importlib, time, pkgutil, sys, os
    t = time.time()
    dirname = [dirname]+[os.path.join(dirname,o) for o in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, o)) and '__' not in o]
    for importer, package_name, _ in pkgutil.iter_modules(dirname):
        full_package_name = '.'.join([importer.path.replace('\\','.').replace('/','.'), package_name])
        if full_package_name not in sys.modules:
            importlib.import_module(full_package_name)
    f = time.time()
    from .logger import log
    log.info("%s Loaded in %s", dirname, f-t)
