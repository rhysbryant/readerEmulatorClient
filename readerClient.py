__author__ = 'rhys'
'''
 * @License LGPL
 * @Auther Rhys Bryant
 * @Copyright Rhys Bryant 2017
 *
 *	This file is part of readerEmulatorClient
 *
 *   readerEmulatorClient is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   any later version.
 *
 *   readerEmulatorClient is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with readerEmulatorClient.  If not, see <http://www.gnu.org/licenses/>.
'''
import readerSerialConnection
import argparse
import sys
class ReaderEmulator:
    TAG_CMD = 64
    TAG_UART_CMD_WRITE_PAGE = TAG_CMD + 1
    TAG_UART_CMD_READ_PAGE = TAG_CMD + 2
    TAG_UART_CMD_GET_LAST_AUTH_KEY_SENT = TAG_CMD + 3
    TAG_UART_CMD_GET_LAST_PAGE_READ = TAG_CMD + 4
    TAG_UART_CMD_GET_LAST_PAGE_WRITE = TAG_CMD + 5
    TAG_PAGE_SIZE = 4
    TAG_NUM_PAGES_RETURNED = 4
    READER_CMD = 128
    READER_CMD_DISABLE_TAG = READER_CMD + 1
    READER_CMD_ENABLE_TAG = READER_CMD + 2

    WRITE_SUCCESS = 1
    WRITE_ERROR = 0

    def __init__(cls, conn):
        cls._conn = conn

    def writePage(self, index, data):
        """writes 4 bytes for the given page index"""
        d = bytearray()
        d.append(self.TAG_UART_CMD_WRITE_PAGE)
        d.append(index)
        d.extend(data)
        self._conn.write(d)

        data = self._conn.read(1)
        if data[0] != self.WRITE_SUCCESS:
            raise ValueError("writePage failed")

    def readPages(self, startingPageIndex):
        """:returns the page bytes for 4 pages starting from the index provided.
        this will wrap round like the NTAG read command"""
        # 0 pad to work round microchip USB bug
        header = bytearray()
        header.append(self.TAG_UART_CMD_READ_PAGE)
        header.append(startingPageIndex)
        header.append(0)
        self._conn.write(header)
        return self._conn.read(self.TAG_PAGE_SIZE * self.TAG_NUM_PAGES_RETURNED)

    def writeAndVerify(self, index, pageData):
        """sends the write then reads the page back to Verify it was written"""
        self.writePage(index, pageData)
        dataRead = self.readPages(index)
        for i in xrange(4):
            if dataRead[i] != pageData[i]:
                raise ValueError("write Verify check failed")

    def writePagesFromFile(self, filename):
        """writes the contents of the file to the tag
        the format is one page per line in hex"""
        fl = open(filename, 'rb')
        pageByteIndex = 0
        pageIndex = 0
        for line in fl:
            line2 = line.rstrip('\n')
            pageBytes = bytearray()
            for i in range(1, 8, 2):
                print line2[i - 1:i + 1]
                pageBytes.append(int("0x" + line2[i - 1:i + 1], 16))
                pageByteIndex += 1
            self.writeAndVerify(pageIndex, pageBytes)
            pageIndex += 1
        fl.close()

    def writePagesToFile(self, filename):
        """reads all the pages from the tag and writes them to the given file"""
        fl = open(filename, 'wb')
        for page in range(0, 45, self.TAG_PAGE_SIZE):
            data = self.readPages(page)

            length = len(data)
            if page == 44:
                length = 4

            if page > 0:
                fl.write('\n')
            for b in range(0, length):
                if (b > 0 and b % 4 == 0):
                    fl.write('\n')
                fl.write(format(data[b], '02x'))
        fl.close()

    def disableTag(self):
        """disables the tag, the emulated reader will flush the buffer and won't process tag commands"""
        header = {self.READER_CMD_DISABLE_TAG}
        self._conn.write(header)

    def enableTag(self):
        """enables the tag, emulated will response to commands sent by the reader"""
        header = {self.READER_CMD_ENABLE_TAG}
        self._conn.write(header)

    @property
    def lastAuthUsed(self):
        """:returns the 4 bytes of the auth key that was last sent by the I2c master to the emulator"""
        header = {self.TAG_UART_CMD_GET_LAST_AUTH_KEY_SENT}
        self._conn.write(header)
        return self._conn.read(4)

    @property
    def lastPageRead(self):
        """:returns the index of the last page that was read from the emulated tag by the I2c master"""
        header = {self.TAG_UART_CMD_GET_LAST_PAGE_READ}
        self._conn.write(header)
        return self._conn.read(1)

    @property
    def lastPageWrite(self):
        """:returns the index and the 4 bytes of the last page written by the I2c master to the emulated tag"""
        header = {self.TAG_UART_CMD_GET_LAST_PAGE_WRITE}
        self._conn.write(header)
        return self._conn.read(5)  # page index,page bytes


def main():
    parser = argparse.ArgumentParser(description='interface for PNS512 Emulator')
    parser.add_argument('--readerPath',help='the path to the serial/uart port',required=True)
    parser.add_argument('--cmd',help='the command to execute',choices=['writeToFile','readFromFile'],required=True)
    parser.add_argument('--file',help='the local file to read or write to/from when using the file commands')
    args = parser.parse_args()

    c = readerSerialConnection.Connection()
    c.connect(args.readerPath)
    reader = ReaderEmulator(c)
    if args.cmd == 'writeToFile':
        reader.writePagesToFile(args.file)
    elif args.cmd == 'readFromFile':
        reader.writePagesFromFile(args.file)

if __name__ == '__main__':
    main()