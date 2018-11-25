from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

bmp3_blend_method = (
    "standard",
    "unknown",
    "unknown_1",
    "alpha",
    "overlay",
    "unknown_2",
    "lighter_color",
    "unknown_3",
    "unknown_4",
    "unknown_5",
    "inverted_alpha",
    "unknown_6",
    "unknown_7",
    "unknown_8",
    )


bmp3_meta_def = BlockDef("bmp3",
    Bool32("flags",
        ("scale_to_bounds", 1 << 3),
        "replace_with_blur",
        ("replace_with_white", 1 << 10),
        "replace_with_black",
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    dependency("animation"),
    dependency("bitmap"),
    dependency("unknown_1"),
    SEnum16("blend_method", *bmp3_blend_method),
    SInt16("unknown_2"),
    SInt16("sprite_index"),
    SInt16("unknown_3"),
    string_id_meta("data_source_name"),
    string_id_meta("sprite_data_source_name"),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )