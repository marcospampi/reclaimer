from ...hek.defs.coll import *
from ..common_descs import *
from .objs.tag import StubbsTag

shield = dict(shield)
shield[2] = BSEnum16("shield material type", *materials_list)

node = Struct("node",
    ascii_str32("name"),
    dyn_senum16("region",
        DYN_NAME_PATH=".....regions.regions_array[DYN_I].name"),
    dyn_senum16("parent node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("next sibling node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first child node",
        DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    BSInt16("unknown"),
    Pad(2),
    reflexive("bsps", permutation_bsp, 32),
    SIZE=64
    )

permutation = Struct("permutation",
    ascii_str32("name"),
    ascii_str32("unknown"),
    SIZE=128
    )

region = Struct("region",
    ascii_str32("name"),
    BBool32("flags",
        "lives until object dies",
        "forces object to die",
        "dies when object dies",
        "dies when object is damaged",
        "disappears when shield is off",
        "inhibits melee attack",
        "inhibits walking",
        "forces drop weapon",
        "causes head-maimed scream",
        ),
    SInt16("unknown0"),
    UInt16("unknown1"),
    Pad(16),
    QStruct("unknown floats", *[BFloat("float%s" % i) for i in range(12)]),

    dependency("destroyed garbage", "garb"),
    dependency("destroyed weapon", "weap"),
    dependency("destroyed effect", "effe"),
    ascii_str32("unknown2"),
    Pad(28),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH='.name'),
    SIZE=224
    )

material = Struct("material",
    ascii_str32("name"),
    BBool32("flags",
        "head"
        ),
    BSEnum16("material type", *materials_list),
    Pad(2),
    BFloat("shield leak percentage"),
    BFloat("shield damage multiplier"),

    Pad(16+12),
    BFloat("body damage multiplier"),
    SIZE=144
    )

coll_body = Struct("tagdata",
    BBool32("flags",
        "takes shield damage for children",
        "takes body damage for children",
        "always shields friendly damage",
        "passes area damage to children",
        "parent never takes body damage for us",
        "only damaged by explosives",
        "only damaged while occupied",
        ),
    dyn_senum16("indirect damage material",
        DYN_NAME_PATH=".materials.materials_array[DYN_I].name"),
    Pad(2),

    body,
    shield,

    Pad(124),
    reflexive("materials", material, 32, DYN_NAME_PATH='.name'),
    reflexive("regions", region, 8, DYN_NAME_PATH='.name'),
    # this reflexive is literally not allowed to have even a single
    # entry in guerilla, so im just gonna replace it with padding.
    Pad(12),
    #reflexive("modifiers", modifier, 0),

    Pad(16),
    Struct("pathfinding box",
        QStruct("x", INCLUDE=from_to),
        QStruct("y", INCLUDE=from_to),
        QStruct("z", INCLUDE=from_to),
        ),

    reflexive("pathfinding spheres", pathfinding_sphere, 32),
    reflexive("nodes", node, 64, DYN_NAME_PATH='.name'),

    SIZE=664,
    )

fast_coll_body = dict(coll_body)
fast_coll_body[12] = reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name')


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=StubbsTag
    )

fast_coll_def = TagDef("coll",
    blam_header("coll", 10),
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=HekTag,
    )
