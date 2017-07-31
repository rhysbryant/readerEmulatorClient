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
import serial

class Connection:

    def connect(self, comport):
        self.serial = serial.Serial(comport)
        self.serial.timeout = 100000

    def write(self, data):
        self.serial.write(data)

    def read(self, numBytes):
        data=self.serial.read(numBytes)
        if len(data) < numBytes:
            raise ValueError("timeout reading response")
        d=bytearray()
        d.extend(data)

        return d
    def disconnect(self):
        self.serial.close()