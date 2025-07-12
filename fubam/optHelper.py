# cssmin
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import re


__version__ = '0.2.0'


def remove_comments(css):
    """Remove all CSS comment blocks."""

    iemac = False
    preserve = False
    comment_start = css.find("/*")
    while comment_start >= 0:
        preserve = css[comment_start + 2:comment_start + 3] == "!"
        comment_end = css.find("*/", comment_start + 2)
        if comment_end < 0:
            if not preserve:
                css = css[:comment_start]
                break
        elif comment_end >= (comment_start + 2):
            if css[comment_end - 1] == "\\":
                comment_start = comment_end + 2
                iemac = True
            elif iemac:
                comment_start = comment_end + 2
                iemac = False
            elif not preserve:
                css = css[:comment_start] + css[comment_end + 2:]
            else:
                comment_start = comment_end + 2
        comment_start = css.find("/*", comment_start)

    return css


def remove_unnecessary_whitespace(css):
    """Remove unnecessary whitespace characters."""

    def pseudoclasscolon(css):

        """
        Prevents 'p :link' from becoming 'p:link'.

        Translates 'p :link' into 'p ___PSEUDOCLASSCOLON___link'; this is
        translated back again later.
        """

        regex = re.compile(r"(^|\})(([^\{\:])+\:)+([^\{]*\{)")
        match = regex.search(css)
        while match:
            css = ''.join([
                css[:match.start()],
                match.group().replace(":", "___PSEUDOCLASSCOLON___"),
                css[match.end():]])
            match = regex.search(css)
        return css

    css = pseudoclasscolon(css)
    css = re.sub(r"\s+([!{};:>+\(\)\],])", r"\1", css)

    css = re.sub(r"^(.*)(@charset \"[^\"]*\";)", r"\2\1", css)
    css = re.sub(r"^(\s*@charset [^;]+;\s*)+", r"\1", css)

    css = re.sub(r"\band\(", "and (", css)

    css = css.replace('___PSEUDOCLASSCOLON___', ':')
    css = re.sub(r"([!{}:;>+\(\[,])\s+", r"\1", css)

    return css


def remove_unnecessary_semicolons(css):
    return re.sub(r";+\}", "}", css)
def remove_empty_rules(css):
    return re.sub(r"[^\}\{]+\{\}", "", css)
def normalize_rgb_colors_to_hex(css):
    regex = re.compile(r"rgb\s*\(\s*([0-9,\s]+)\s*\)")
    match = regex.search(css)
    while match:
        colors = map(lambda s: s.strip(), match.group(1).split(","))
        hexcolor = '#%.2x%.2x%.2x' % tuple(map(int, colors))
        css = css.replace(match.group(), hexcolor)
        match = regex.search(css)
    return css


def condense_zero_units(css):
    return re.sub(r"([\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)", r"\1\2", css)


def condense_multidimensional_zeros(css):
    css = css.replace(":0 0 0 0;", ":0;")
    css = css.replace(":0 0 0;", ":0;")
    css = css.replace(":0 0;", ":0;")
    css = css.replace("background-position:0;", "background-position:0 0;")
    return css
def condense_floating_points(css):
    return re.sub(r"(:|\s)0+\.(\d+)", r"\1.\2", css)


def condense_hex_colors(css):
    regex = re.compile(r"([^\"'=\s])(\s*)#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])")
    match = regex.search(css)
    while match:
        first = match.group(3) + match.group(5) + match.group(7)
        second = match.group(4) + match.group(6) + match.group(8)
        if first.lower() == second.lower():
            css = css.replace(match.group(), match.group(1) + match.group(2) + '#' + first)
            match = regex.search(css, match.end() - 3)
        else:
            match = regex.search(css, match.end())
    return css


def condense_whitespace(css):
    return re.sub(r"\s+", " ", css)
def condense_semicolons(css):
    return re.sub(r";;+", ";", css)
def wrap_css_lines(css, line_length):
    lines = []
    line_start = 0
    for i, char in enumerate(css):
        if char == '}' and (i - line_start >= line_length):
            lines.append(css[line_start:i + 1])
            line_start = i + 1
    if line_start < len(css):
        lines.append(css[line_start:])
    return '\n'.join(lines)
def cssmin(css, wrap=None):
    css = remove_comments(css)
    css = condense_whitespace(css)
    css = css.replace('"\\"}\\""', "___PSEUDOCLASSBMH___")
    css = remove_unnecessary_whitespace(css)
    css = remove_unnecessary_semicolons(css)
    css = condense_zero_units(css)
    css = condense_multidimensional_zeros(css)
    css = condense_floating_points(css)
    css = normalize_rgb_colors_to_hex(css)
    css = condense_hex_colors(css)
    if wrap is not None:
        css = wrap_css_lines(css, wrap)
    css = css.replace("___PSEUDOCLASSBMH___", '"\\"}\\""')
    css = condense_semicolons(css)
    return css.strip()

#rjsmin

import functools as _ft
import re as _re


def _make_jsmin(python_only=False):
    """
    Generate JS minifier based on `jsmin.c by Douglas Crockford`_

    .. _jsmin.c by Douglas Crockford:
       http://www.crockford.com/javascript/jsmin.c

    Parameters:
      python_only (bool):
        Use only the python variant. If true, the c extension is not even
        tried to be loaded.

    Returns:
      callable: Minifier
    """
    # pylint: disable = unused-variable, possibly-unused-variable
    # pylint: disable = too-many-locals, too-many-statements

    if not python_only:
        try:
            import _rjsmin  # pylint: disable = import-outside-toplevel
        except ImportError:
            pass
        else:
            # Ensure that the C version is in sync
            # https://github.com/ndparker/rjsmin/issues/11
            if getattr(_rjsmin, '__version__', None) == __version__:
                return _rjsmin.jsmin
    try:
        xrange  # pylint: disable = used-before-assignment
    except NameError:
        xrange = range  # pylint: disable = redefined-builtin

    space_chars = r'[\000-\011\013\014\016-\040]'

    line_comment = r'(?://[^\r\n]*)'
    space_comment = r'(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)'
    space_comment_nobang = r'(?:/\*(?!!)[^*]*\*+(?:[^/*][^*]*\*+)*/)'
    bang_comment = r'(?:/\*![^*]*\*+(?:[^/*][^*]*\*+)*/)'

    string1 = r"(?:'[^'\\\r\n]*(?:\\(?:[^\r\n]|\r?\n|\r)[^'\\\r\n]*)*')"
    string1 = string1.replace("'", r'\047')  # portability
    string2 = r'(?:"[^"\\\r\n]*(?:\\(?:[^\r\n]|\r?\n|\r)[^"\\\r\n]*)*")'
    string3 = r'(?:`[^`\\]*(?:\\(?:[^\r\n]|\r?\n|\r)[^`\\]*)*`)'
    string3 = string3.replace('`', r'\140')  # portability
    strings = r'(?:%s|%s|%s)' % (string1, string2, string3)

    charclass = r'(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^\\\]\r\n]*)*\])'
    nospecial = r'[^/\\\[\r\n]'
    regex = r'(?:/(?![\r\n/*])%s*(?:(?:\\[^\r\n]|%s)%s*)*/[a-z]*)' % (
        nospecial, charclass, nospecial
    )
    space = r'(?:%s|%s)' % (space_chars, space_comment)
    newline = r'(?:%s?[\r\n])' % line_comment

    def fix_charclass(result):
        """ Fixup string of chars to fit into a regex char class """
        pos = result.find('-')
        if pos >= 0:
            result = r'%s%s-' % (result[:pos], result[pos + 1:])

        def sequentize(string):
            """
            Notate consecutive characters as sequence

            (1-4 instead of 1234)
            """
            first, last, result = None, None, []
            for char in map(ord, string):
                if last is None:
                    first = last = char
                elif last + 1 == char:
                    last = char
                else:
                    result.append((first, last))
                    first = last = char
            if last is not None:
                result.append((first, last))
            return ''.join(['%s%s%s' % (
                chr(first),
                last > first + 1 and '-' or '',
                last != first and chr(last) or ''
            ) for first, last in result])  # noqa

        return _re.sub(
            r"([\000-\040'`])",  # ' and ` for better portability
            lambda m: '\\%03o' % ord(m.group(1)), (
                sequentize(result)
                .replace('\\', '\\\\')
                .replace('[', '\\[')
                .replace(']', '\\]')
            )
        )

    def id_literal_(what):
        """ Make id_literal like char class """
        match = _re.compile(what).match
        result = ''.join([
            chr(c) for c in xrange(127) if not match(chr(c))
        ])
        return '[^%s]' % fix_charclass(result)

    def not_id_literal_(keep):
        """ Make negated id_literal like char class """
        match = _re.compile(id_literal_(keep)).match
        result = ''.join([
            chr(c) for c in xrange(127) if not match(chr(c))
        ])
        return r'[%s]' % fix_charclass(result)

    not_id_literal = not_id_literal_(r'[a-zA-Z0-9_$]')
    preregex1 = r'[(,=:\[!&|?{};\r\n+*-]'
    preregex2 = r'%(not_id_literal)sreturn' % locals()

    id_literal = id_literal_(r'[a-zA-Z0-9_$]')
    id_literal_open = id_literal_(r'[a-zA-Z0-9_${\[(!+-]')
    id_literal_close = id_literal_(r'[a-zA-Z0-9_$}\])"\047\140+-]')
    post_regex_off = id_literal_(r'[^\000-\040}\])?:|,;.&=+-]')

    dull = r'[^\047"\140/\000-\040]'

    space_sub_simple = _re.compile((
        # noqa pylint: disable = bad-option-value, bad-continuation

        r'(%(dull)s+)'                                         # 0
        r'|(%(strings)s%(dull)s*)'                             # 1
        r'|(?<=[)])'
            r'%(space)s*(?:%(newline)s%(space)s*)*'
            r'(%(regex)s)'                                     # 2
            r'(?=%(space)s*(?:%(newline)s%(space)s*)*'
                r'\.'
                r'%(space)s*(?:%(newline)s%(space)s*)*[a-z])'
        r'|(?<=%(preregex1)s)'
            r'%(space)s*(?:%(newline)s%(space)s*)*'
            r'(%(regex)s)'                                     # 3
            r'(%(space)s*(?:%(newline)s%(space)s*)+'           # 4
                r'(?=%(post_regex_off)s))?'
        r'|(?<=%(preregex2)s)'
            r'%(space)s*(?:(%(newline)s)%(space)s*)*'          # 5
            r'(%(regex)s)'                                     # 6
            r'(%(space)s*(?:%(newline)s%(space)s*)+'           # 7
                r'(?=%(post_regex_off)s))?'
        r'|(?<=%(id_literal_close)s)'
            r'%(space)s*(?:(%(newline)s)%(space)s*)+'          # 8
            r'(?=%(id_literal_open)s)'
        r'|(?<=%(id_literal)s)(%(space)s)+(?=%(id_literal)s)'  # 9
        r'|(?<=\+)(%(space)s)+(?=\+)'                          # 10
        r'|(?<=-)(%(space)s)+(?=-)'                            # 11
        r'|%(space)s+'
        r'|(?:%(newline)s%(space)s*)+'
    ) % locals()).sub

    # print(space_sub_simple.__self__.pattern)

    def space_subber_simple(match):
        """ Substitution callback """
        # pylint: disable = too-many-return-statements

        groups = match.groups()
        if groups[0]:
            return groups[0]
        elif groups[1]:
            return groups[1]
        elif groups[2]:
            return groups[2]
        elif groups[3]:
            if groups[4]:
                return groups[3] + '\n'
            return groups[3]
        elif groups[6]:
            return "%s%s%s" % (
                groups[5] and '\n' or '',
                groups[6],
                groups[7] and '\n' or '',
            )
        elif groups[8]:
            return '\n'
        elif groups[9] or groups[10] or groups[11]:
            return ' '
        else:
            return ''

    space_sub_banged = _re.compile((
        # noqa pylint: disable = bad-option-value, bad-continuation

        r'(%(dull)s+)'                                         # 0
        r'|(%(strings)s%(dull)s*)'                             # 1
        r'|(?<=[)])'
            r'(%(space)s*(?:%(newline)s%(space)s*)*)'          # 2
            r'(%(regex)s)'                                     # 3
            r'(?=%(space)s*(?:%(newline)s%(space)s*)*'
                r'\.'
                r'%(space)s*(?:%(newline)s%(space)s*)*[a-z])'
        r'|(?<=%(preregex1)s)'
            r'(%(space)s*(?:%(newline)s%(space)s*)*)'          # 4
            r'(%(regex)s)'                                     # 5
            r'(%(space)s*(?:%(newline)s%(space)s*)+'           # 6
                r'(?=%(post_regex_off)s))?'
        r'|(?<=%(preregex2)s)'
            r'(%(space)s*(?:(%(newline)s)%(space)s*)*)'        # 7, 8
            r'(%(regex)s)'                                     # 9
            r'(%(space)s*(?:%(newline)s%(space)s*)+'           # 10
                r'(?=%(post_regex_off)s))?'
        r'|(?<=%(id_literal_close)s)'
            r'(%(space)s*(?:%(newline)s%(space)s*)+)'          # 11
            r'(?=%(id_literal_open)s)'
        r'|(?<=%(id_literal)s)(%(space)s+)(?=%(id_literal)s)'  # 12
        r'|(?<=\+)(%(space)s+)(?=\+)'                          # 13
        r'|(?<=-)(%(space)s+)(?=-)'                            # 14
        r'|(%(space)s+)'                                       # 15
        r'|((?:%(newline)s%(space)s*)+)'                       # 16
    ) % locals()).sub

    # print(space_sub_banged.__self__.pattern)

    keep = _re.compile((
        r'%(space_chars)s+|%(space_comment_nobang)s+|%(newline)s+'
        r'|(%(bang_comment)s+)'
    ) % locals()).sub
    keeper = lambda m: m.groups()[0] or ''

    # print(keep.__self__.pattern)

    def space_subber_banged(match):
        """ Substitution callback """
        # pylint: disable = too-many-return-statements

        groups = match.groups()
        if groups[0]:
            return groups[0]
        elif groups[1]:
            return groups[1]
        elif groups[3]:
            return "%s%s" % (
                keep(keeper, groups[2]),
                groups[3],
            )
        elif groups[5]:
            return "%s%s%s%s" % (
                keep(keeper, groups[4]),
                groups[5],
                keep(keeper, groups[6] or ''),
                groups[6] and '\n' or '',
            )
        elif groups[9]:
            return "%s%s%s%s%s" % (
                keep(keeper, groups[7]),
                groups[8] and '\n' or '',
                groups[9],
                keep(keeper, groups[10] or ''),
                groups[10] and '\n' or '',
            )
        elif groups[11]:
            return keep(keeper, groups[11]) + '\n'
        elif groups[12] or groups[13] or groups[14]:
            return keep(keeper, groups[12] or groups[13] or groups[14]) or ' '
        else:
            return keep(keeper, groups[15] or groups[16])

    banged = _ft.partial(space_sub_banged, space_subber_banged)
    simple = _ft.partial(space_sub_simple, space_subber_simple)

    def jsmin(script, keep_bang_comments=False):
        r"""
        Minify javascript based on `jsmin.c by Douglas Crockford`_\.

        Instead of parsing the stream char by char, it uses a regular
        expression approach which minifies the whole script with one big
        substitution regex.

        .. _jsmin.c by Douglas Crockford:
           http://www.crockford.com/javascript/jsmin.c

        Parameters:
          script (str):
            Script to minify

          keep_bang_comments (bool):
            Keep comments starting with an exclamation mark? (``/*!...*/``)

        Returns:
          str: Minified script
        """
        # pylint: disable = redefined-outer-name

        is_bytes, script = _as_str(script)
        script = (banged if keep_bang_comments else simple)(
            '\n%s\n' % script
        ).strip()
        if is_bytes:
            script = script.encode('latin-1')
            if is_bytes == 2:
                script = bytearray(script)
        return script

    return jsmin

jsmin = _make_jsmin()


def _as_str(script):
    """ Make sure the script is a text string """
    is_bytes = False
    if str is bytes:
        if not isinstance(script, basestring):  # noqa pylint: disable = undefined-variable
            raise TypeError("Unexpected type")
    elif isinstance(script, bytes):
        is_bytes = True
        script = script.decode('latin-1')
    elif isinstance(script, bytearray):
        is_bytes = 2
        script = script.decode('latin-1')
    elif not isinstance(script, str):
        raise TypeError("Unexpected type")

    return is_bytes, script


def jsmin_for_posers(script, keep_bang_comments=False):
    r"""
    Minify javascript based on `jsmin.c by Douglas Crockford`_\.

    Instead of parsing the stream char by char, it uses a regular
    expression approach which minifies the whole script with one big
    substitution regex.

    .. _jsmin.c by Douglas Crockford:
       http://www.crockford.com/javascript/jsmin.c

    :Warning: This function is the digest of a _make_jsmin() call. It just
              utilizes the resulting regexes. It's here for fun and may
              vanish any time. Use the `jsmin` function instead.

    Parameters:
      script (str):
        Script to minify

      keep_bang_comments (bool):
        Keep comments starting with an exclamation mark? (``/*!...*/``)

    Returns:
      str: Minified script
    """
    if not keep_bang_comments:
        rex = (
            r'([^\047"\140/\000-\040]+)|((?:(?:\047[^\047\\\r\n]*(?:\\(?:[^'
            r'\r\n]|\r?\n|\r)[^\047\\\r\n]*)*\047)|(?:"[^"\\\r\n]*(?:\\(?:[^'
            r'\r\n]|\r?\n|\r)[^"\\\r\n]*)*")|(?:\140[^\140\\]*(?:\\(?:[^\r\n'
            r']|\r?\n|\r)[^\140\\]*)*\140))[^\047"\140/\000-\040]*)|(?<=[)])'
            r'(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+'
            r')*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-\0'
            r'40]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)*((?:/(?![\r\n/*])[^/'
            r'\\\[\r\n]*(?:(?:\\[^\r\n]|(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^\\\]'
            r'\r\n]*)*\]))[^/\\\[\r\n]*)*/[a-z]*))(?=(?:[\000-\011\013\014\0'
            r'16-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n'
            r']*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^'
            r'/*][^*]*\*+)*/))*)*\.(?:[\000-\011\013\014\016-\040]|(?:/\*[^*'
            r']*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?:[\00'
            r'0-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)'
            r'*[a-z])|(?<=[(,=:\[!&|?{};\r\n+*-])(?:[\000-\011\013\014\016-'
            r'\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)'
            r'?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*]'
            r'[^*]*\*+)*/))*)*((?:/(?![\r\n/*])[^/\\\[\r\n]*(?:(?:\\[^\r\n]|'
            r'(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^\\\]\r\n]*)*\]))[^/\\\[\r\n]*)*'
            r'/[a-z]*))((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/'
            r'*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?:[\000-\011\013'
            r'\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)+(?=[^\000'
            r'-\040&)+,.:;=?\]|}-]))?|(?<=[\000-#%-,./:-@\[-^\140{-~-]return'
            r')(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*'
            r'+)*/))*(?:((?:(?://[^\r\n]*)?[\r\n]))(?:[\000-\011\013\014\016'
            r'-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)*((?:/(?![\r\n/*])'
            r'[^/\\\[\r\n]*(?:(?:\\[^\r\n]|(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^'
            r'\\\]\r\n]*)*\]))[^/\\\[\r\n]*)*/[a-z]*))((?:[\000-\011\013\014'
            r'\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r'
            r'\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:'
            r'[^/*][^*]*\*+)*/))*)+(?=[^\000-\040&)+,.:;=?\]|}-]))?|(?<=[^\0'
            r'00-!#%&(*,./:-@\[\\^{|~])(?:[\000-\011\013\014\016-\040]|(?:/'
            r'\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:((?:(?://[^\r\n]*)?[\r\n]))'
            r'(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+'
            r')*/))*)+(?=[^\000-\040"#%-\047)*,./:-@\\-^\140|-~])|(?<=[^\000'
            r'-#%-,./:-@\[-^\140{-~-])((?:[\000-\011\013\014\016-\040]|(?:/'
            r'\*[^*]*\*+(?:[^/*][^*]*\*+)*/)))+(?=[^\000-#%-,./:-@\[-^\140{-'
            r'~-])|(?<=\+)((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:'
            r'[^/*][^*]*\*+)*/)))+(?=\+)|(?<=-)((?:[\000-\011\013\014\016-\0'
            r'40]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)))+(?=-)|(?:[\000-\011\0'
            r'13\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))+|(?:(?:(?'
            r'://[^\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]'
            r'*\*+(?:[^/*][^*]*\*+)*/))*)+'
        )

        def subber(match):
            """ Substitution callback """
            groups = match.groups()
            return (
                groups[0] or
                groups[1] or
                groups[2] or
                (groups[4] and (groups[3] + '\n')) or
                groups[3] or
                (groups[6] and "%s%s%s" % (
                    groups[5] and '\n' or '',
                    groups[6],
                    groups[7] and '\n' or '',
                )) or
                (groups[8] and '\n') or
                (groups[9] and ' ') or
                (groups[10] and ' ') or
                (groups[11] and ' ') or
                ''
            )
    else:
        rex = (
            r'([^\047"\140/\000-\040]+)|((?:(?:\047[^\047\\\r\n]*(?:\\(?:[^'
            r'\r\n]|\r?\n|\r)[^\047\\\r\n]*)*\047)|(?:"[^"\\\r\n]*(?:\\(?:[^'
            r'\r\n]|\r?\n|\r)[^"\\\r\n]*)*")|(?:\140[^\140\\]*(?:\\(?:[^\r\n'
            r']|\r?\n|\r)[^\140\\]*)*\140))[^\047"\140/\000-\040]*)|(?<=[)])'
            r'((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*'
            r'+)*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-'
            r'\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)*)((?:/(?![\r\n/*])'
            r'[^/\\\[\r\n]*(?:(?:\\[^\r\n]|(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^'
            r'\\\]\r\n]*)*\]))[^/\\\[\r\n]*)*/[a-z]*))(?=(?:[\000-\011\013\0'
            r'14\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^'
            r'\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+('
            r'?:[^/*][^*]*\*+)*/))*)*\.(?:[\000-\011\013\014\016-\040]|(?:/'
            r'\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?'
            r':[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*'
            r'/))*)*[a-z])|(?<=[(,=:\[!&|?{};\r\n+*-])((?:[\000-\011\013\014'
            r'\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r'
            r'\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:'
            r'[^/*][^*]*\*+)*/))*)*)((?:/(?![\r\n/*])[^/\\\[\r\n]*(?:(?:\\[^'
            r'\r\n]|(?:\[[^\\\]\r\n]*(?:\\[^\r\n][^\\\]\r\n]*)*\]))[^/\\\[\r'
            r'\n]*)*/[a-z]*))((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+'
            r'(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)?[\r\n])(?:[\000-\01'
            r'1\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)+(?=['
            r'^\000-\040&)+,.:;=?\]|}-]))?|(?<=[\000-#%-,./:-@\[-^\140{-~-]r'
            r'eturn)((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*]['
            r'^*]*\*+)*/))*(?:((?:(?://[^\r\n]*)?[\r\n]))(?:[\000-\011\013\0'
            r'14\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)*)((?:/(?!['
            r'\r\n/*])[^/\\\[\r\n]*(?:(?:\\[^\r\n]|(?:\[[^\\\]\r\n]*(?:\\[^'
            r'\r\n][^\\\]\r\n]*)*\]))[^/\\\[\r\n]*)*/[a-z]*))((?:[\000-\011'
            r'\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:('
            r'?://[^\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*'
            r']*\*+(?:[^/*][^*]*\*+)*/))*)+(?=[^\000-\040&)+,.:;=?\]|}-]))?|'
            r'(?<=[^\000-!#%&(*,./:-@\[\\^{|~])((?:[\000-\011\013\014\016-\0'
            r'40]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*(?:(?:(?://[^\r\n]*)?['
            r'\r\n])(?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^'
            r'*]*\*+)*/))*)+)(?=[^\000-\040"#%-\047)*,./:-@\\-^\140|-~])|(?<'
            r'=[^\000-#%-,./:-@\[-^\140{-~-])((?:[\000-\011\013\014\016-\040'
            r']|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))+)(?=[^\000-#%-,./:-@\[-^'
            r'\140{-~-])|(?<=\+)((?:[\000-\011\013\014\016-\040]|(?:/\*[^*]*'
            r'\*+(?:[^/*][^*]*\*+)*/))+)(?=\+)|(?<=-)((?:[\000-\011\013\014'
            r'\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))+)(?=-)|((?:[\00'
            r'0-\011\013\014\016-\040]|(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))+)'
            r'|((?:(?:(?://[^\r\n]*)?[\r\n])(?:[\000-\011\013\014\016-\040]|'
            r'(?:/\*[^*]*\*+(?:[^/*][^*]*\*+)*/))*)+)'
        )

        keep = _re.compile(
            r'[\000-\011\013\014\016-\040]+|(?:/\*(?!!)[^*]*\*+(?:[^/*][^*]*'
            r'\*+)*/)+|(?:(?://[^\r\n]*)?[\r\n])+|((?:/\*![^*]*\*+(?:[^/*][^'
            r'*]*\*+)*/)+)'
        ).sub
        keeper = lambda m: m.groups()[0] or ''

        def subber(match):
            """ Substitution callback """
            groups = match.groups()
            return (
                groups[0] or
                groups[1] or
                groups[3] and "%s%s" % (
                    keep(keeper, groups[2]),
                    groups[3],
                ) or
                groups[5] and "%s%s%s%s" % (
                    keep(keeper, groups[4]),
                    groups[5],
                    keep(keeper, groups[6] or ''),
                    groups[6] and '\n' or '',
                ) or
                groups[9] and "%s%s%s%s%s" % (
                    keep(keeper, groups[7]),
                    groups[8] and '\n' or '',
                    groups[9],
                    keep(keeper, groups[10] or ''),
                    groups[10] and '\n' or '',
                ) or
                groups[11] and (keep(keeper, groups[11]) + '\n') or
                groups[12] and (keep(keeper, groups[12]) or ' ') or
                groups[13] and (keep(keeper, groups[13]) or ' ') or
                groups[14] and (keep(keeper, groups[14]) or ' ') or
                keep(keeper, groups[15] or groups[16])
            )

    is_bytes, script = _as_str(script)
    script = _re.sub(rex, subber, '\n%s\n' % script).strip()
    if is_bytes:
        script = script.encode('latin-1')
        if is_bytes == 2:
            script = bytearray(script)
    return script


# Custom codes


def passc():
        pass


def recieveContent(file,callback=passc):
    print(open(file).read())
    callback()


class iterationSkipper:
    def __init__(self):
        self.function = "skipping iteration"


# class iterationSucker:
#     def __init__(self,x):
#         img

class codeInjector:
    def __init__(self,filename,MinifyBool = True):
        self.filename = filename
        self.MinifyBool = MinifyBool
        open(filename,"w").close()
    def injectContent(self,filetoappend):
        print("appending  "+filetoappend+" to: " + self.filename)
        with open(self.filename,"a") as ultima:
            ultima.write((cssmin(open(filetoappend).read()) if self.MinifyBool else open(filetoappend).read())+"\n")
            ultima.close()
