from ...hek.defs.actr import *
from ..common_descs import *
from .objs.tag import StubbsTag

actr_body = dict(actr_body)
actr_body[3] = BSEnum16("type", *actor_types)
actr_body[12] = dict(actr_body[12])
actr_body[12][2] = BSEnum16("leader type", *actor_types)

actr_body[14] = dict(actr_body[14])
actr_body[14][6] = BSEnum16("defensive crouch type",
    "never",
    "danger",
    "low shields",
    "hide behind shield",
    "any target",
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header('actr'),
    actr_body,

    ext=".actor", endian=">", tag_cls=StubbsTag
    )
