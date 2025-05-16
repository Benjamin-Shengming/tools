from loguru import logger

class FuncAsCmd:
    def __init__(self, log=logger):
        self.map_funcs = {}
        self.default = ""
        self.hidden = set()
        self.log = log

    def as_cmd(self, default=False, hidden=False):
        def inner(func):
            if default:
                self.default = func.__name__
            self.map_funcs[func.__name__] = func
            if hidden:
                self.hidden.add(func.__name__)
            return func

        return inner

    def debug(self, msg): 
        if self.log is None:
            return  
        self.log.debug(msg)
      
    def call_func_by_name(self, funcname, *args, **kargs):
        self.debug(f"Try to run {funcname}")
        return self.map_funcs[funcname](*args, **kargs)

    def add_funcs_as_cmds(self, parser, long_cmd_str="--command", short_cmd_str="-c"):
        all_cmds = set([k for k in self.map_funcs])
        all_cmds = list(all_cmds - self.hidden)
        all_cmds.sort()
        dft_cmd = self.default
        parser.add_argument(
            long_cmd_str,
            short_cmd_str,
            help="commands need to run" + str(all_cmds),
            default=dft_cmd,
        )
        return parser
