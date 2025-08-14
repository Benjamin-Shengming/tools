import typing
# Abstract base class and enum for token types
from abc import ABC
from enum import Enum

_VT = typing.TypeVar("_VT")

class TT(Enum):
    COM = 1  # Comment
    SEC = 2  # Section
    STR = 3  # String/whitespace
    KVP = 4  # Key-value pair
    DIR = 5  # Directive

class Token(ABC):
    """Base class for all token types."""
    def __init__(self, tt: TT):
        self.tt = tt

    def __repr__(self):
        return f'<{self.tt}> {str(self)}'

class Comment(Token):
    """Represents a comment line."""
    def __init__(self, comment):
        self.comment = comment
        super().__init__(TT.COM)

    def __str__(self):
        return '#' + self.comment

class KVP(Token):
    """Represents a key-value pair."""
    def __init__(self, key, key_post, value_pre, value):
        self.key = key
        self.key_post = key_post
        self.value_pre = value_pre
        self.value = value
        super().__init__(TT.KVP)

    def __str__(self):
        return f'{self.key}{self.key_post}={self.value_pre}{self.value}'

class Directive(Token):
    """Represents a directive line starting with a dot."""
    def __init__(self, directive, spacer, args):
        self.directive = directive
        self.spacer = spacer
        self.args = args
        super().__init__(TT.DIR)

    def __str__(self):
        return f'.{self.directive}{self.spacer}{self.args}'

class Str(Token):
    """Represents a string or whitespace token."""
    def __init__(self, value: str):
        self.value = value
        super().__init__(TT.STR)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'<{self.tt}> {str(self).replace("\r", r"\r").replace("\n", r"\n")}'

class Section(Token):
    """Represents a section, which can contain other tokens."""
    def __init__(self, value_pre, value, value_post):
        self.value_pre = value_pre
        self.value = value
        self.value_post = value_post
        self.nodes:list[Token] = []  # Child tokens in this section
        super().__init__(TT.SEC)

    def append(self, t):
        self.nodes.append(t)

    def prepend(self, t):
        self.nodes.insert(0, t)

    def get_kvp(self, name, default: _VT = None) -> KVP | _VT:
        """Get a key-value pair by name."""
        return next((s for s in self.nodes if s.tt == TT.KVP and typing.cast(KVP, s).key == name), default)

    @property
    def kvp(self) -> typing.Iterable[KVP]:
        """Iterate over all key-value pairs in this section."""
        return filter(lambda x: x.tt == TT.KVP, self.nodes)

    def __str__(self):
        return f'[{self.value_pre}{self.value}{self.value_post}]' + ''.join(map(lambda n: str(n), self.nodes))

    def __repr__(self):
        return f'<{self.tt}> [{self.value_pre}{self.value}{self.value_post}]\n' + '\n'.join(map(lambda n: n.__repr__(), self.nodes)) + '\n'

class OpensslCnf:
    def print_ast_tree(self, indent: int = 0):
        """Print the config AST as a tree to stdout, only showing sections and key-value pairs."""
        for node in self.nodes:
            self._print_node_tree(node, indent)

    def _print_node_tree(self, node, indent):
        # Print Section, KVP, and Directive nodes, show only their own info
        if getattr(node, 'tt', None) == TT.SEC:
            print(' ' * indent + f'Section: [{node.value_pre}{node.value}{node.value_post}]')
        elif getattr(node, 'tt', None) == TT.KVP:
            print(' ' * indent + f'KVP: {node.key}{node.key_post}={node.value_pre}{node.value}')
        elif getattr(node, 'tt', None) == TT.DIR:
            print(' ' * indent + f'Directive: .{node.directive}{node.spacer}{node.args}')
        if hasattr(node, 'nodes'):
            for subnode in node.nodes:
                self._print_node_tree(subnode, indent + 2)
    """Represents the root of the OpenSSL config AST."""
    def __init__(self):
        self.nodes:list[Token] = []  # Top-level tokens

    def prepend(self, t):
        """Insert a token at the beginning."""
        self.nodes.insert(0, t)

    def append(self, t):
        """Append a token at the end."""
        self.nodes.append(t)

    def get_section(self, name, default: _VT = None) -> Section | _VT:
        """Get a section by name."""
        return next((s for s in self.nodes if s.tt == TT.SEC and typing.cast(Section, s).value == name), default)

    def get_kvp(self, name, default: _VT = None) -> KVP | _VT:
        return next((s for s in self.nodes if s.tt == TT.KVP and typing.cast(KVP, s).key == name), default)

    def __str__(self):
        return ''.join(map(lambda n: str(n), self.nodes))

    def __repr__(self):
        return '\n'.join(map(lambda n: n.__repr__(), self.nodes))

    class parser():
        """Parser for OpenSSL config files."""
        def __init__(self, fd):
            self.fd = fd  # File descriptor
            self.read1()

        def read1(self):
            """Read one character from file."""
            self.c = self.fd.read(1)
            return self.c

        def eat_comment(self):
            """Parse a comment line."""
            if self.c == '#':
                v = ''
                while True:
                    self.read1()
                    if not self.c or self.c == '\n' or self.c == '\r':
                        return Comment(v)
                    v += self.c

        def eat_str(self):
            """Parse whitespace as a string token."""
            if self.c.isspace():
                v = self.c
                while True:
                    self.read1()
                    if not self.c or not self.c.isspace():
                        return Str(v)
                    v += self.c

        def eat_sec(self):
            """Parse a section header."""
            if self.c == '[':
                pre = v = post = ''

                # Parse leading whitespace
                while True:
                    self.read1()
                    if not self.c:
                        raise SystemError("invalid section")
                    if not self.c.isspace():
                        break
                    pre += self.c

                # Parse section name
                while True:
                    if not self.c:
                        raise SystemError("invalid section")
                    if self.c.isspace() or self.c == ']':
                        break
                    v += self.c
                    self.read1()

                # Parse trailing whitespace before closing bracket
                while True:
                    if not self.c:
                        raise SystemError("invalid section")
                    if self.c == ']':
                        self.read1()
                        break
                    post += self.c
                    self.read1()

                return Section(pre, v, post)

        def eat_kv(self):
            """Parse a key-value pair."""
            if self.c.isalnum():
                key = key_post = value_pre = value = ''

                # Parse key
                while True:
                    if self.c.isspace() or self.c == '=':
                        break
                    key += self.c
                    self.read1()
                    if not self.c or self.c == '\n' or self.c == '\r':
                        raise SystemError("invalid key")

                # Parse whitespace after key
                while True:
                    if self.c == '=':
                        break
                    key_post += self.c
                    self.read1()
                    if not self.c or self.c == '\n' or self.c == '\r':
                        raise SystemError("invalid key_after")

                # Parse whitespace before value
                while True:
                    self.read1()
                    if not self.c.isspace():
                        break
                    value_pre += self.c
                    if not self.c or self.c == '\n' or self.c == '\r':
                        raise SystemError("invalid value_pre")

                # Parse value
                while True:
                    value += self.c
                    self.read1()
                    if not self.c or self.c == '#' or self.c == '\n' or self.c == '\r':
                        break

                return KVP(key, key_post, value_pre, value)

        def eat_directive(self):
            """Parse a directive line starting with a dot."""
            if self.c == '.':
                directive = spacer = args = ''
                # Parse directive name
                while True:
                    self.read1()
                    if not self.c or self.c == '#' or self.c == '\n' or self.c == '\r':
                        return Directive(directive, spacer, args)
                    if self.c.isspace():
                        break
                    directive += self.c

                # Parse whitespace after directive
                while True:
                    spacer += self.c
                    self.read1()
                    if not self.c or self.c == '#' or self.c == '\n' or self.c == '\r':
                        return Directive(directive, spacer, args)
                    if not self.c.isspace():
                        break

                # Parse arguments
                while True:
                    args += self.c
                    self.read1()
                    if not self.c or self.c == '#' or self.c == '\n' or self.c == '\r':
                        return Directive(directive, spacer, args)

    def dump(self, filename):
        """Write the config AST to a file."""
        with open(filename, 'wt', encoding='utf-8') as new:
            s = str(self)
            new.write(s)

    def ensure_last_new_line(self, nl='\n'):
        """Ensure the AST ends with a newline string token."""
        if len(self.nodes) == 0:
            self.append(Str(nl))
        else:
            lastAstNode = self.nodes[-1]
            if lastAstNode.tt == TT.STR:
                if not typing.cast(Str, lastAstNode).value.endswith(nl):
                    self.append(Str(nl))
            elif lastAstNode.tt == TT.SEC:
                lastSection = typing.cast(Section, lastAstNode)
                if len(lastSection.nodes) == 0:
                    lastSection.append(Str(nl))
                else:
                    lastSectionNode = lastSection.nodes[-1]
                    if lastSectionNode.tt == TT.STR:
                        if not typing.cast(Str, lastSectionNode).value.endswith(nl):
                            lastSectionNode.append(Str(nl))
                    else:
                        lastSection.append(Str(nl))
            else:
                self.append(Str(nl))

    @staticmethod
    def load(filename):
        """Load and parse an OpenSSL config file into an AST."""
        rv = OpensslCnf()

        with open(filename, 'rt', encoding='utf-8') as fd:
            ps = OpensslCnf.parser(fd)
            cur_section = rv
            while True:
                # Try to parse each token type in order
                t = ps.eat_str() or \
                    ps.eat_comment() or \
                    ps.eat_sec() or \
                    ps.eat_kv() or \
                    ps.eat_directive() or \
                    None

                if not t:
                    break

                if t.tt == TT.SEC:
                    rv.append(t)
                    cur_section = t
                else:
                    cur_section.append(t)

                # Uncomment for debug: print(f'<{t.tt}>' + str(t))
        return rv