# encoding: utf-8

import sys
import time
from workflow import Workflow, ICON_CLOCK

args = ''

def main(wf):
    t = str(int(time.time()))
    if args:
        if str.isdigit(args):
            timeArray = time.localtime(float(args))
            t = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
        else:
            timeArray = time.strptime(args, "%Y-%m-%d %H:%M:%S")
            t = str(int(time.mktime(timeArray)))
    wf.add_item(title='time',
                subtitle=t,
                copytext=t,
                icon=ICON_CLOCK)

    wf.send_feedback()


if __name__ == u"__main__":
    args = "{query}"
    wf = Workflow()
    sys.exit(wf.run(main))
