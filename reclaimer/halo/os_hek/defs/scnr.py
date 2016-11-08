from ...hek.defs.scnr import *

player_starting_profile = Struct("player starting profile",
    ascii_str32("name"),
    BFloat("starting health modifier"),
    BFloat("starting shield modifier"),
    dependency("primary weapon", "weap"),
    BSInt16("primary rounds loaded"),
    BSInt16("primary rounds total"),
    dependency("secondary weapon", "weap"),
    BSInt16("secondary rounds loaded"),
    BSInt16("secondary rounds total"),
    SInt8("starting frag grenade count"),
    SInt8("starting plasma grenade count"),
    SInt8("starting custom 2 grenade count"),
    SInt8("starting custom 3 grenade count"),
    SIZE=104
    )

ai_anim_reference = Struct("ai animation reference",
    ascii_str32("animation name"),
    dependency_os("animation graph", ("antr", "magy")),
    SIZE=60
    )

reference = Struct("tag reference",
    Pad(24),
    dependency_os("reference"),
    SIZE=40
    )

# copy the scnr_body and replace the descriptors for certain fields
# with ones that are tweaked for use with open sauce
scnr_body = dict(scnr_body)
scnr_body[0] = dependency_os("project yellow definitions", 'yelo')
scnr_body[35] = reflexive("player starting profiles",
    player_starting_profile, 128)
scnr_body[50] = reflexive("ai animation references", ai_anim_reference, 128)
scnr_body[54] = rawdata_ref("script syntax data", max_size=570076)
scnr_body[55] = rawdata_ref("script string data", max_size=393216)
scnr_body[58] = reflexive("references", reference, 256)
scnr_body[68] = reflexive("structure bsps", structure_bsp, 32)

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">"
    )
