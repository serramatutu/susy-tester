from termcolor import cprint

class PrettyLogger:
    @staticmethod
    def _normalize_args(args):
        return ' '.join(map(str, args))

    def success(self, *args, **kwargs):
        cprint(PrettyLogger._normalize_args(args), color='green', **kwargs)

    def warn(self, *args, **kwargs):
        cprint(PrettyLogger._normalize_args(args), color='yellow', **kwargs)

    def info(self, *args, **kwargs):
        cprint(PrettyLogger._normalize_args(args), color='cyan', **kwargs)

    def error(self, *args, **kwargs):
        cprint(PrettyLogger._normalize_args(args), color='red', **kwargs)

    def log(self, *args, **kwargs):
        cprint(PrettyLogger._normalize_args(args), **kwargs)