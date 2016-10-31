from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

vertex = Struct("vertex",
    BFloat("spring strength coefficient"),

    Pad(24),
    QStruct("angles", INCLUDE=yp_float),  # measured in radians
    BFloat("length"),
    BSInt16("sequence index"),

    Pad(2),
    QStruct("color", INCLUDE=argb_float),
    QStruct("lod color", INCLUDE=argb_float),
    SIZE=128
    )

ant__body = Struct("tagdata",
    StrLatin1("attachment marker name", SIZE=32),
    dependency("bitmaps", valid_bitmaps),
    dependency("physics", valid_point_physics),

    Pad(80),
    BFloat("spring strength coefficient"),
    BFloat("falloff pixels"),
    BFloat("cutoff pixels"),

    Pad(40),
    reflexive("vertices", vertex, 20),
    SIZE=208
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    blam_header('"ant!'),
    ant__body,

    ext=".antenna", endian=">"
    )