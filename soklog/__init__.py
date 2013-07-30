import logging
import inspect
from os import path

data = {}


def init(module, log_name):
    data['module'] = module
    data['log'] = logging.getLogger(log_name)


def _get_args_as_string(args):
    args = list(args)
    args = [str(arg) for arg in args]
    return ' '.join(args)


def info(*args, **kwargs):
    msg = _get_args_as_string(args)
    data['log'].info(msg, **kwargs)


def warning(*args, **kwargs):
    msg = _get_args_as_string(args)
    data['log'].warning(msg, **kwargs)


def debug(*args, **kwargs):
    msg = _get_args_as_string(args)
    main_path = path.dirname(data['module'].__file__)
    src_path = inspect.stack()[1][1]
    src_path = '.' + src_path[len(main_path):]
    line = inspect.stack()[1][2]
    msg = '%s:%d %s' % (src_path, line, msg)
    data['log'].debug(msg, **kwargs)


def error(*args, **kwargs):
    data['log'].error(*args, **kwargs)


def start_file_logging(path):
    hdlr = logging.FileHandler(path)
    fmt = logging.Formatter("%(asctime)-10s %(message)s")
    hdlr.setFormatter(fmt)
    data['log'].addHandler(hdlr)
    data['log'].setLevel(logging.DEBUG)


def start_stdout_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-10s %(message)s",
        datefmt="%H:%M:%S"
    )
