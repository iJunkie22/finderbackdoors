from __future__ import unicode_literals, print_function
import os.path
import xattr
import struct
import biplist
import os
import lockedfile


class TagColorBits(int):
    tag_struct = struct.Struct('8xbb22x')

    BLUE = 0x08
    GRAY = 0x02
    GREEN = 0x04
    ORANGE = 0x0E
    PURPLE = 0x06
    RED = 0x0C
    YELLOW = 0x0A

    @property
    def color_name(self):
        return ('', 'Gray', 'Green', 'Purple', 'Blue', 'Yellow', 'Red', 'Orange')[self]

    @property
    def color_int(self):
        return int(self)

    @classmethod
    def from_color_name(cls, code_str):
        return cls(('', 'Gray', 'Green', 'Purple', 'Blue', 'Yellow', 'Red', 'Orange').index(code_str))

    @classmethod
    def from_finder_xattr(cls, xattr_bin):
        return cls((cls.tag_struct.unpack(xattr_bin)[1] % 16) / 2)

    def to_finder_xattr_int(self):
        return self * 2

    def to_tag_meta_int(self):
        if self == 0:
            return u''
        else:
            return '\n{}'.format(self.color_int)

    def __str__(self):
        return self.color_name

    def __repr__(self):
        return '<TagColorBits {}:{}>'.format(self.color_int, self.color_name)


class HideFileExtensionBit(int):
    tag_struct = struct.Struct('8xbb22x')

    @classmethod
    def from_finder_xattr(cls, xattr_bin):
        return cls(cls.tag_struct.unpack(xattr_bin)[1] // 16)

    @classmethod
    def from_bool(cls, code_bool):
        return cls(int(code_bool))

    @property
    def is_hidden(self):
        return bool(int(self))


class HideFileSelfBit(int):
    YES = 0x40
    NO = 0x00
    tag_struct = struct.Struct('8xbb22x')

    @classmethod
    def from_finder_xattr(cls, xattr_bin):
        return cls(cls.tag_struct.unpack(xattr_bin)[1])

    @classmethod
    def from_bool(cls, code_bool):
        val = 0x40 if code_bool else 0x00
        return cls(int(val))

    @property
    def is_hidden(self):
        return self == 0x40


class FinderXattr(str, object):
    tag_struct = struct.Struct('8xbb22x')

    @property
    def tag_color(self):
        return TagColorBits.from_finder_xattr(self)

    @property
    def file_ext_hidden(self):
        return HideFileExtensionBit.from_finder_xattr(self)

    @property
    def file_self_hidden(self):
        return HideFileSelfBit.from_finder_xattr(self)

    @classmethod
    def make(cls, tagcolorbits, hidefileextbit, hidefileselfbit):
        merged_bits = (hidefileextbit * 16) + (tagcolorbits * 2)
        return cls(cls.tag_struct.pack(hidefileselfbit, merged_bits))

    def make_modded(self, tagcolorbits=None, hidefileextbit=None, hidefileselfbit=None):
        if tagcolorbits is None:
            tagcolorbits = self.tag_color

        if hidefileextbit is None:
            hidefileextbit = self.file_ext_hidden

        if hidefileselfbit is None:
            hidefileselfbit = self.file_self_hidden

        return self.make(tagcolorbits, hidefileextbit, hidefileselfbit)


class TagsXattr(list, object):
    @property
    def pytags(self):
        return [(k, TagColorBits(int(v))) for k, v in map(lambda x: x.split('\n'), self)]

    def __repr__(self):
        return repr(self.pytags)

    def add_tag(self, tagname, tagcolor):
        self.append(tagname + TagColorBits.from_color_name(tagcolor).to_tag_meta_int())

    def has_tag(self, tagname, tagcolor):
        return tagname + TagColorBits.from_color_name(tagcolor).to_tag_meta_int() in self

    def remove_tag(self, tagname, tagcolor):
        target = tagname + TagColorBits.from_color_name(tagcolor).to_tag_meta_int()
        if target in self:
            self.remove(target)

    def to_bplist(self):
        return biplist.writePlistToString(list(self))


class SmartXattr(xattr.xattr):
    finder_struct = struct.Struct('8xbb22x')

    def __init__(self, obj):
        super(SmartXattr, self).__init__(obj)

    @classmethod
    def from_path(cls, fp1):
        return cls(os.path.abspath(os.path.expanduser(fp1)))

    def get_finder_info(self):
        try:
            result = self.get('com.apple.FinderInfo')
        except IOError:
            result = self.finder_struct.pack(0)
        finder_obj = FinderXattr(result)
        return finder_obj

    def get_tags_meta(self):
        result = self.get('com.apple.metadata:_kMDItemUserTags')
        bplist1 = biplist.readPlistFromString(result)
        return TagsXattr(bplist1)

    def add_tag(self, tagname, tagcolor):
        old_tag_meta = self.get_tags_meta()
        old_tag_meta.add_tag(tagname, tagcolor)
        self.set('com.apple.metadata:_kMDItemUserTags', old_tag_meta.to_bplist())
        return True

    def remove_tag(self, tagname, tagcolor):
        old_tag_meta = self.get_tags_meta()
        old_tag_meta.remove_tag(tagname, tagcolor)
        self.set('com.apple.metadata:_kMDItemUserTags', old_tag_meta.to_bplist())

    def has_tag(self, tagname, tagcolor):
        return self.get_tags_meta().has_tag(tagname, tagcolor)

    @property
    def recent_finder_tag(self):
        return TagColorBits.from_finder_xattr(self.get_finder_info())

    @property
    def hide_file_ext(self):
        return HideFileExtensionBit.from_finder_xattr(self.get_finder_info())

    @property
    def hide_file_self(self):
        return HideFileSelfBit.from_finder_xattr(self.get_finder_info())

    def mod_finder_info(self, tagcolorbits=None, hidefileextbit=None, hidefileselfbit=None):
        modded_bstr = self.get_finder_info().make_modded(tagcolorbits, hidefileextbit, hidefileselfbit)
        self.set('com.apple.FinderInfo', modded_bstr)

    @recent_finder_tag.setter
    def recent_finder_tag(self, value):
        assert isinstance(value, TagColorBits)
        self.mod_finder_info(tagcolorbits=value)

    @hide_file_ext.setter
    def hide_file_ext(self, value):
        val2 = value

        if isinstance(value, bool):
            val2 = HideFileExtensionBit.from_bool(value)
        assert isinstance(val2, HideFileExtensionBit)

        self.mod_finder_info(hidefileextbit=value)

    @hide_file_self.setter
    def hide_file_self(self, value):
        val2 = value

        if isinstance(value, bool):
            val2 = HideFileSelfBit.from_bool(value)
        assert isinstance(val2, HideFileSelfBit)

        self.mod_finder_info(hidefileselfbit=value)

if __name__ == '__main__':
    FP1 = os.path.expanduser('~/TEMP/tagcolors/purple.txt')
    print(os.stat(os.path.expanduser(FP1)).st_flags)
    print(lockedfile.is_file_locked(FP1))

    SCHOOL_TAG = ('School', 'Blue')

    foo = SmartXattr.from_path(FP1)
    print(foo.recent_finder_tag)
    cow = foo.get_tags_meta()
    print(foo.get_tags_meta())

    if foo.has_tag(*SCHOOL_TAG):
        foo.remove_tag(*SCHOOL_TAG)
    else:
        foo.add_tag(*SCHOOL_TAG)

    if not bool(foo.hide_file_ext):
        foo.hide_file_ext = True
    else:
        foo.hide_file_ext = False

    if not bool(foo.hide_file_self):
        foo.hide_file_self = True
    else:
        foo.hide_file_self = False

    print(foo.get_tags_meta())
