from os.path import dirname, basename, isfile
import glob

dir_path = dirname(__file__) + "/*.py"

modules = glob.glob(dir_path)

__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]