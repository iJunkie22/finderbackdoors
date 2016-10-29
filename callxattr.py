from __future__ import unicode_literals, print_function
import os.path
import xattr
import struct
import biplist


class TagColorBits(int):
    tag_struct = struct.Struct('9xb22x')

    BLUE = 0x08
    GRAY = 0x02
    GREEN = 0x04
    ORANGE = 0x0E
    PURPLE = 0x06
    RED = 0x0C
    YELLOW = 0x0A

    @property
    def color_name(self):
        return ('Gray', 'Green', 'Purple', 'Blue', 'Yellow', 'Red', 'Orange')[self - 1]

    @property
    def color_int(self):
        return int(self)

    @classmethod
    def from_color_name(cls, code_str):
        return cls(('Gray', 'Green', 'Purple', 'Blue', 'Yellow', 'Red', 'Orange').index(code_str) + 1)

    @classmethod
    def from_finder_xattr(cls, xattr_bin):
        return cls(cls.tag_struct.unpack(xattr_bin)[0] / 2)

    def to_finder_xattr_int(self):
        return self * 2

    def to_tag_meta_int(self):
        return unicode(self.color_int)

    def __str__(self):
        return self.color_name

    def __repr__(self):
        return '<TagColorBits {}:{}>'.format(self.color_int, self.color_name)


class FinderXattr(str, object):
    @property
    def tag_color(self):
        return TagColorBits.from_finder_xattr(self)


class TagsXattr(list, object):
    @property
    def pytags(self):
        return [(k, TagColorBits(int(v))) for k, v in map(lambda x: x.split('\n'), self)]

    def __repr__(self):
        return repr(self.pytags)

    def add_tag(self, tagname, tagcolor):
        self.append(tagname + u'\n' + TagColorBits.from_color_name(tagcolor).to_tag_meta_int())

    def has_tag(self, tagname, tagcolor):
        return tagname + u'\n' + TagColorBits.from_color_name(tagcolor).to_tag_meta_int() in self

    def remove_tag(self, tagname, tagcolor):
        target = tagname + u'\n' + TagColorBits.from_color_name(tagcolor).to_tag_meta_int()
        if target in self:
            self.remove(target)

    def to_bplist(self):
        return biplist.writePlistToString(list(self))


class SmartXattr(xattr.xattr):
    finder_struct = struct.Struct('9xb22x')

    def __init__(self, obj):
        super(SmartXattr, self).__init__(obj)

    @classmethod
    def from_path(cls, fp1):
        return cls(os.path.abspath(os.path.expanduser(fp1)))

    def get_finder_info(self):
        result = self.get('com.apple.FinderInfo')
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

if __name__ == '__main__':
    FP1 = '~/TEMP/tagcolors/purple.txt'
    SCHOOL_TAG = ('School', 'Blue')

    foo = SmartXattr.from_path(FP1)
    print(foo.recent_finder_tag)
    cow = foo.get_tags_meta()
    print(foo.get_tags_meta())

    if foo.has_tag(*SCHOOL_TAG):
        foo.remove_tag(*SCHOOL_TAG)
    else:
        foo.add_tag(*SCHOOL_TAG)

    print(foo.get_tags_meta())
