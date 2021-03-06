#!/usr/bin/python
#    This file is part of LfLe.
#
#   Copyright 2012, 2013 Willi Ballenthin <william.ballenthin@mandiant.com>
#                    while at Mandiant <http://www.mandiant.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   Version v.0.1
import sys
import mmap
import contextlib

from Evt.Evt import Record
from Evt.BinaryParser import OverrunBufferException


def main():
    with open(sys.argv[1], 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                          access=mmap.ACCESS_READ)) as buf:
            offset = 0x8
            offset = buf.find("LfLe", offset)  # skip header
            while offset != -1:
                try:
                    record = Record(buf, offset - 0x4)
                except OverrunBufferException:
                    break
                try:
                    print('%s, %d, "%s", "%s"' % (record.time_generated().isoformat("T") + "Z",
                                                  record.event_id(), record.source(),
                                                  str(record.strings())))
                except UnicodeDecodeError:
                    pass
                except UnicodeEncodeError:
                    pass
                except OverrunBufferException:
                    pass
                if record.length() > 0x100:
                    offset = buf.find("LfLe", offset + 1)
                else:
                    offset = buf.find("LfLe", offset + record.length())

if __name__ == "__main__":
    main()
