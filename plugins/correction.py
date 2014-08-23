import re

from util import hook

correction_s = r"^[sS]/(.*/.*/([igux]{,4}))\S*$"
correction_re = re.compile(correction_s)


@hook.regex(correction_s)
def correction(match, input=None, conn=None, message=None):
    find, replacement, flags = tuple([b.replace("\/", "/") for b in re.split(r"(?<!\\)/", match.groups()[0])])
    flag_string = flags.replace("g", "")
    flag_string = "(?{})".format(flag_string) if flag_string != "" else ""
    find_re = re.compile("{}{}".format(flag_string, find))

    for item in conn.history[input.chan].__reversed__():
        nick, timestamp, msg = item
        if correction_re.match(msg):
            # don't correct corrections, it gets really confusing
            continue
        if find_re.search(msg):
            if "\x01ACTION" in msg:
                msg = msg.replace("\x01ACTION ", "/me ").replace("\x01", "")
            message("Correction, <{}> {}".format(nick, find_re.sub("\x02" + replacement + "\x02", msg, count=int("g" not in flags))))
            return
        else:
            continue
    return "Did not find {} in any recent messages.".format(to_find)
