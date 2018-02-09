# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import datetime
import plistlib
import subprocess
import re


__author__ = 'ethan'


class MetaDataResult(object):
    def __init__(self, root_dict):
        self.root_dict = root_dict

    @classmethod
    def from_file(cls, fp_to_inspect):
        s1 = subprocess.check_output((b'/usr/bin/mdls -plist - \"{}\"'.format(fp_to_inspect)), shell=True)
        print(s1)
        bad_lines = "\t<key>kMDLabel_.*?</key>\n\t<date>0000-12-30T00:00:00Z</date>\n"
        s1_filtered = re.sub(bad_lines, "", s1)
        # Add a filter for kMDLabel_kqde5prblvaibjifrcn4saxjwi followed by a datetime of 0000-12-30T00:00:00Z
        d1 = plistlib.readPlistFromString(s1_filtered)
        return cls(d1)

    def to_plist_string(self):
        return plistlib.writePlistToString(self.root_dict)

    @property
    def kMDItemContentCreationDate(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemContentCreationDate")

    @property
    def kMDItemContentModificationDate(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemContentModificationDate")

    @property
    def kMDItemContentType(self):
        """:rtype: str"""
        return self.root_dict.get("kMDItemContentType")

    @property
    def kMDItemContentTypeTree(self):
        """
        (self: MetaDataResult) -> List[str]
        :rtype: list of str"""
        return self.root_dict.get("kMDItemContentTypeTree")

    @property
    def kMDItemDateAdded(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemDateAdded")

    @property
    def kMDItemDisplayName(self):
        """:rtype: str"""
        return self.root_dict.get("kMDItemDisplayName")

    @property
    def kMDItemFSContentChangeDate(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemFSContentChangeDate")

    @property
    def kMDItemFSCreationDate(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemFSCreationDate")

    @property
    def kMDItemFSCreatorCode(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSCreatorCode")

    @property
    def kMDItemFSFinderFlags(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSFinderFlags")

    @property
    def kMDItemFSInvisible(self):
        """:rtype: bool"""
        return self.root_dict.get("kMDItemFSInvisible")

    @property
    def kMDItemFSIsExtensionHidden(self):
        """:rtype: bool"""
        return self.root_dict.get("kMDItemFSIsExtensionHidden")

    @property
    def kMDItemFSLabel(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSLabel")

    @property
    def kMDItemFSName(self):
        """:rtype: str"""
        return self.root_dict.get("kMDItemFSName")

    @property
    def kMDItemFSOwnerGroupID(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSOwnerGroupID")

    @property
    def kMDItemFSOwnerUserID(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSOwnerUserID")

    @property
    def kMDItemFSSize(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSSize")

    @property
    def kMDItemFSTypeCode(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemFSTypeCode")

    @property
    def kMDItemKind(self):
        """:rtype: str"""
        return self.root_dict.get("kMDItemKind")

    @property
    def kMDItemLastUsedDate(self):
        """:rtype: datetime.datetime"""
        return self.root_dict.get("kMDItemLastUsedDate")

    @property
    def kMDItemLogicalSize(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemLogicalSize")

    @property
    def kMDItemPhysicalSize(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemPhysicalSize")

    @property
    def kMDItemUseCount(self):
        """:rtype: int"""
        return self.root_dict.get("kMDItemUseCount")

    @property
    def kMDItemUsedDates(self):
        """:rtype: list"""
        return self.root_dict.get("kMDItemUsedDates")

    @property
    def kMDItemUserTags(self):
        """:rtype: list or None"""
        return self.root_dict.get("kMDItemUserTags")

if __name__ == '__main__':
    mdResult = MetaDataResult.from_file("/Users/ethan/Developer/Bash/xterm_color_test.sh")
    print(mdResult.to_plist_string())

