# -*- coding: utf-8 -*-
import os
import sqlite3

if __name__ == '__main__':
    command_list = []
    with sqlite3.connect(os.path.expanduser('~/Library/Application Support/iTerm2/ShellHistory.sqlite')) as db:
        for row in db.execute("select ZCOMMAND from ZCOMMANDHISTORYCOMMANDUSE order  by Z_PK desc limit 50"):
            command_list.append(row[0])