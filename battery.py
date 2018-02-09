# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import subprocess
import plistlib

__author__ = 'ethan'


class BatteryInfo(object):
    def __init__(self, sample_dict):
        self.sample_dict = sample_dict

    def dump_code(self):
        for k in sorted(self.sample_dict.keys()):
            prop_frmt = "    @property\n    def {0}(self):\n" \
                        "        \"\"\":rtype: {1}\"\"\"\n" \
                        "        return self.sample_dict['{0}']\n\n" \
                        "    @{0}.setter\n    def {0}(self, value):\n" \
                        "        \"\"\":type value: {1}\"\"\"\n" \
                        "        self.sample_dict['{0}'] = value\n"
            print(prop_frmt.format(k, type(self.sample_dict[k]).__name__))

    def pretty_print(self):
        for k in sorted(self.sample_dict.keys()):
            v = self.sample_dict[k]
            print("{}:{}{}".format(k, " " * (50 - (len(repr(k)) + len(str(v)))), v))

    @staticmethod
    def take_sample():
        s1 = subprocess.check_output(('-w0', '-r', '-c', 'AppleSmartBattery', '-l', '-a'), executable='/usr/sbin/ioreg')
        d1 = plistlib.readPlistFromString(s1)
        return d1[0]

    @classmethod
    def from_sample(cls):
        return cls(cls.take_sample())

    def update_sample(self):
        self.sample_dict = self.take_sample()

    @property
    def AdapterInfo(self):
        """:rtype: int"""
        return self.sample_dict['AdapterInfo']

    @AdapterInfo.setter
    def AdapterInfo(self, value):
        """:type value: int"""
        self.sample_dict['AdapterInfo'] = value

    @property
    def Amperage(self):
        """:rtype: int"""
        return self.sample_dict['Amperage']

    @Amperage.setter
    def Amperage(self, value):
        """:type value: int"""
        self.sample_dict['Amperage'] = value

    @property
    def AvgTimeToEmpty(self):
        """:rtype: int"""
        return self.sample_dict['AvgTimeToEmpty']

    @AvgTimeToEmpty.setter
    def AvgTimeToEmpty(self, value):
        """:type value: int"""
        self.sample_dict['AvgTimeToEmpty'] = value

    @property
    def AvgTimeToFull(self):
        """:rtype: int"""
        return self.sample_dict['AvgTimeToFull']

    @AvgTimeToFull.setter
    def AvgTimeToFull(self, value):
        """:type value: int"""
        self.sample_dict['AvgTimeToFull'] = value

    @property
    def BatteryInstalled(self):
        """:rtype: bool"""
        return self.sample_dict['BatteryInstalled']

    @BatteryInstalled.setter
    def BatteryInstalled(self, value):
        """:type value: bool"""
        self.sample_dict['BatteryInstalled'] = value

    @property
    def BatteryInvalidWakeSeconds(self):
        """:rtype: int"""
        return self.sample_dict['BatteryInvalidWakeSeconds']

    @BatteryInvalidWakeSeconds.setter
    def BatteryInvalidWakeSeconds(self, value):
        """:type value: int"""
        self.sample_dict['BatteryInvalidWakeSeconds'] = value

    @property
    def BatterySerialNumber(self):
        """:rtype: str"""
        return self.sample_dict['BatterySerialNumber']

    @BatterySerialNumber.setter
    def BatterySerialNumber(self, value):
        """:type value: str"""
        self.sample_dict['BatterySerialNumber'] = value

    @property
    def BootPathUpdated(self):
        """:rtype: int"""
        return self.sample_dict['BootPathUpdated']

    @BootPathUpdated.setter
    def BootPathUpdated(self, value):
        """:type value: int"""
        self.sample_dict['BootPathUpdated'] = value

    @property
    def CellVoltage(self):
        """:rtype: list"""
        return self.sample_dict['CellVoltage']

    @CellVoltage.setter
    def CellVoltage(self, value):
        """:type value: list"""
        self.sample_dict['CellVoltage'] = value

    @property
    def CurrentCapacity(self):
        """:rtype: int"""
        return self.sample_dict['CurrentCapacity']

    @CurrentCapacity.setter
    def CurrentCapacity(self, value):
        """:type value: int"""
        self.sample_dict['CurrentCapacity'] = value

    @property
    def CycleCount(self):
        """:rtype: int"""
        return self.sample_dict['CycleCount']

    @CycleCount.setter
    def CycleCount(self, value):
        """:type value: int"""
        self.sample_dict['CycleCount'] = value

    @property
    def DesignCapacity(self):
        """:rtype: int"""
        return self.sample_dict['DesignCapacity']

    @DesignCapacity.setter
    def DesignCapacity(self, value):
        """:type value: int"""
        self.sample_dict['DesignCapacity'] = value

    @property
    def DesignCycleCount9C(self):
        """:rtype: int"""
        return self.sample_dict['DesignCycleCount9C']

    @DesignCycleCount9C.setter
    def DesignCycleCount9C(self, value):
        """:type value: int"""
        self.sample_dict['DesignCycleCount9C'] = value

    @property
    def DeviceName(self):
        """:rtype: str"""
        return self.sample_dict['DeviceName']

    @DeviceName.setter
    def DeviceName(self, value):
        """:type value: str"""
        self.sample_dict['DeviceName'] = value

    @property
    def ExternalChargeCapable(self):
        """:rtype: bool"""
        return self.sample_dict['ExternalChargeCapable']

    @ExternalChargeCapable.setter
    def ExternalChargeCapable(self, value):
        """:type value: bool"""
        self.sample_dict['ExternalChargeCapable'] = value

    @property
    def ExternalConnected(self):
        """:rtype: bool"""
        return self.sample_dict['ExternalConnected']

    @ExternalConnected.setter
    def ExternalConnected(self, value):
        """:type value: bool"""
        self.sample_dict['ExternalConnected'] = value

    @property
    def FirmwareSerialNumber(self):
        """:rtype: int"""
        return self.sample_dict['FirmwareSerialNumber']

    @FirmwareSerialNumber.setter
    def FirmwareSerialNumber(self, value):
        """:type value: int"""
        self.sample_dict['FirmwareSerialNumber'] = value

    @property
    def FullPathUpdated(self):
        """:rtype: int"""
        return self.sample_dict['FullPathUpdated']

    @FullPathUpdated.setter
    def FullPathUpdated(self, value):
        """:type value: int"""
        self.sample_dict['FullPathUpdated'] = value

    @property
    def FullyCharged(self):
        """:rtype: bool"""
        return self.sample_dict['FullyCharged']

    @FullyCharged.setter
    def FullyCharged(self, value):
        """:type value: bool"""
        self.sample_dict['FullyCharged'] = value

    @property
    def IOGeneralInterest(self):
        """:rtype: str"""
        return self.sample_dict['IOGeneralInterest']

    @IOGeneralInterest.setter
    def IOGeneralInterest(self, value):
        """:type value: str"""
        self.sample_dict['IOGeneralInterest'] = value

    @property
    def IOObjectClass(self):
        """:rtype: str"""
        return self.sample_dict['IOObjectClass']

    @IOObjectClass.setter
    def IOObjectClass(self, value):
        """:type value: str"""
        self.sample_dict['IOObjectClass'] = value

    @property
    def IOObjectRetainCount(self):
        """:rtype: int"""
        return self.sample_dict['IOObjectRetainCount']

    @IOObjectRetainCount.setter
    def IOObjectRetainCount(self, value):
        """:type value: int"""
        self.sample_dict['IOObjectRetainCount'] = value

    @property
    def IORegistryEntryID(self):
        """:rtype: int"""
        return self.sample_dict['IORegistryEntryID']

    @IORegistryEntryID.setter
    def IORegistryEntryID(self, value):
        """:type value: int"""
        self.sample_dict['IORegistryEntryID'] = value

    @property
    def IORegistryEntryName(self):
        """:rtype: str"""
        return self.sample_dict['IORegistryEntryName']

    @IORegistryEntryName.setter
    def IORegistryEntryName(self, value):
        """:type value: str"""
        self.sample_dict['IORegistryEntryName'] = value

    @property
    def IOServiceBusyState(self):
        """:rtype: int"""
        return self.sample_dict['IOServiceBusyState']

    @IOServiceBusyState.setter
    def IOServiceBusyState(self, value):
        """:type value: int"""
        self.sample_dict['IOServiceBusyState'] = value

    @property
    def IOServiceBusyTime(self):
        """:rtype: int"""
        return self.sample_dict['IOServiceBusyTime']

    @IOServiceBusyTime.setter
    def IOServiceBusyTime(self, value):
        """:type value: int"""
        self.sample_dict['IOServiceBusyTime'] = value

    @property
    def IOServiceState(self):
        """:rtype: int"""
        return self.sample_dict['IOServiceState']

    @IOServiceState.setter
    def IOServiceState(self, value):
        """:type value: int"""
        self.sample_dict['IOServiceState'] = value

    @property
    def InstantAmperage(self):
        """:rtype: int"""
        return self.sample_dict['InstantAmperage']

    @InstantAmperage.setter
    def InstantAmperage(self, value):
        """:type value: int"""
        self.sample_dict['InstantAmperage'] = value

    @property
    def InstantTimeToEmpty(self):
        """:rtype: int"""
        return self.sample_dict['InstantTimeToEmpty']

    @InstantTimeToEmpty.setter
    def InstantTimeToEmpty(self, value):
        """:type value: int"""
        self.sample_dict['InstantTimeToEmpty'] = value

    @property
    def IsCharging(self):
        """:rtype: bool"""
        return self.sample_dict['IsCharging']

    @IsCharging.setter
    def IsCharging(self, value):
        """:type value: bool"""
        self.sample_dict['IsCharging'] = value

    @property
    def LegacyBatteryInfo(self):
        """:rtype: _InternalDict"""
        return self.sample_dict['LegacyBatteryInfo']

    @LegacyBatteryInfo.setter
    def LegacyBatteryInfo(self, value):
        """:type value: _InternalDict"""
        self.sample_dict['LegacyBatteryInfo'] = value

    @property
    def Location(self):
        """:rtype: int"""
        return self.sample_dict['Location']

    @Location.setter
    def Location(self, value):
        """:type value: int"""
        self.sample_dict['Location'] = value

    @property
    def ManufactureDate(self):
        """:rtype: int"""
        return self.sample_dict['ManufactureDate']

    @ManufactureDate.setter
    def ManufactureDate(self, value):
        """:type value: int"""
        self.sample_dict['ManufactureDate'] = value

    @property
    def Manufacturer(self):
        """:rtype: str"""
        return self.sample_dict['Manufacturer']

    @Manufacturer.setter
    def Manufacturer(self, value):
        """:type value: str"""
        self.sample_dict['Manufacturer'] = value

    @property
    def ManufacturerData(self):
        """:rtype: instance"""
        return self.sample_dict['ManufacturerData']

    @ManufacturerData.setter
    def ManufacturerData(self, value):
        """:type value: instance"""
        self.sample_dict['ManufacturerData'] = value

    @property
    def MaxCapacity(self):
        """:rtype: int"""
        return self.sample_dict['MaxCapacity']

    @MaxCapacity.setter
    def MaxCapacity(self, value):
        """:type value: int"""
        self.sample_dict['MaxCapacity'] = value

    @property
    def MaxErr(self):
        """:rtype: int"""
        return self.sample_dict['MaxErr']

    @MaxErr.setter
    def MaxErr(self, value):
        """:type value: int"""
        self.sample_dict['MaxErr'] = value

    @property
    def OperationStatus(self):
        """:rtype: int"""
        return self.sample_dict['OperationStatus']

    @OperationStatus.setter
    def OperationStatus(self, value):
        """:type value: int"""
        self.sample_dict['OperationStatus'] = value

    @property
    def PackReserve(self):
        """:rtype: int"""
        return self.sample_dict['PackReserve']

    @PackReserve.setter
    def PackReserve(self, value):
        """:type value: int"""
        self.sample_dict['PackReserve'] = value

    @property
    def PermanentFailureStatus(self):
        """:rtype: int"""
        return self.sample_dict['PermanentFailureStatus']

    @PermanentFailureStatus.setter
    def PermanentFailureStatus(self, value):
        """:type value: int"""
        self.sample_dict['PermanentFailureStatus'] = value

    @property
    def PostChargeWaitSeconds(self):
        """:rtype: int"""
        return self.sample_dict['PostChargeWaitSeconds']

    @PostChargeWaitSeconds.setter
    def PostChargeWaitSeconds(self, value):
        """:type value: int"""
        self.sample_dict['PostChargeWaitSeconds'] = value

    @property
    def PostDischargeWaitSeconds(self):
        """:rtype: int"""
        return self.sample_dict['PostDischargeWaitSeconds']

    @PostDischargeWaitSeconds.setter
    def PostDischargeWaitSeconds(self, value):
        """:type value: int"""
        self.sample_dict['PostDischargeWaitSeconds'] = value

    @property
    def Temperature(self):
        """:rtype: int"""
        return self.sample_dict['Temperature']

    @Temperature.setter
    def Temperature(self, value):
        """:type value: int"""
        self.sample_dict['Temperature'] = value

    @property
    def TimeRemaining(self):
        """:rtype: int"""
        return self.sample_dict['TimeRemaining']

    @TimeRemaining.setter
    def TimeRemaining(self, value):
        """:type value: int"""
        self.sample_dict['TimeRemaining'] = value

    @property
    def UserVisiblePathUpdated(self):
        """:rtype: int"""
        return self.sample_dict['UserVisiblePathUpdated']

    @UserVisiblePathUpdated.setter
    def UserVisiblePathUpdated(self, value):
        """:type value: int"""
        self.sample_dict['UserVisiblePathUpdated'] = value

    @property
    def Voltage(self):
        """:rtype: int"""
        return self.sample_dict['Voltage']

    @Voltage.setter
    def Voltage(self, value):
        """:type value: int"""
        self.sample_dict['Voltage'] = value


class BatteryInfoHandle(object):
    pass

foo = BatteryInfo.from_sample()
print("hey")
#foo.dump_code()
print(foo.AdapterInfo)
foo.pretty_print()
