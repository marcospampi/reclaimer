from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def object_reference(name, *args, **kwargs):
    "Macro to cut down on a lot of code"
    block_name = kwargs.pop('block_name', name + 's').replace(' ', '_')

    dyn_type_path = "tagdata.%s_palette.STEPTREE[DYN_I].name.filepath" % block_name
    return Struct(name,
        dyn_senum16('type', DYN_NAME_PATH=dyn_type_path),
        dyn_senum16('name',
            DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
        BBool16('not placed',
            "automatically",
            "on easy",
            "on normal",
            "on hard",
            ),
        BSInt16('desired permutation'),
        QStruct("position", INCLUDE=xyz_float),
        ypr_float_rad("rotation"),
        *args,
        **kwargs
        )

def object_palette(name, def_id, size=48):
    "Macro to cut down on a lot of code"
    return Struct(name,
        dependency("name", def_id),
        SIZE=size
        )

fl_float_xyz = QStruct("",
    FlFloat("x"),
    FlFloat("y"),
    FlFloat("z"),
    ORIENT="h"
    )

stance_flags = FlBool16("stance",
    "walk",
    "look only",
    "primary fire",
    "secondary fire",
    "jump",
    "crouch",
    "melee",
    "flashlight",
    "action1",
    "action2",
    "action hold",
    )

unit_control_packet = Struct("unit control packet",
    
    )

r_a_stream_header = Struct("r a stream header",
    UInt8("move index", DEFAULT=3, MAX=6),
    UInt8("bool index"),
    stance_flags,
    FlSInt16("weapon", DEFAULT=-1),
    QStruct("speed", FlFloat("x"), FlFloat("y"), ORIENT="h"),
    QStruct("feet", INCLUDE=fl_float_xyz),
    QStruct("body", INCLUDE=fl_float_xyz),
    QStruct("head", INCLUDE=fl_float_xyz),
    QStruct("change", INCLUDE=fl_float_xyz),
    FlUInt32("unknown1"),
    FlUInt32("unknown2", DEFAULT=0xFFFFFFFF),
    SIZE=60
    )

script_syntax_data_block = QStruct("script_syntax_data_block",
    UInt16("unknown0"),
    UInt16("unknown1"),
    UInt16("unknown2"),
    UInt16("unknown3"),
    UInt32("unknown4"),
    UInt32("unknown5"),
    UInt32("unknown6"),
    SIZE=20
    )

script_syntax_data_header = Container("script syntax data header",
    ascii_str32('name', DEFAULT="script node"),
    UInt16("data array length", DEFAULT=19001),  # this is 1 more than it should be
    UInt16("data block size", DEFAULT=20),
    UInt8("unknown0", DEFAULT=1),
    UInt8("unknown1"),   # zero?
    UInt16("unknown2"),  # zero?
    UInt32("data sig", DEFAULT="d@t@"),
    UInt16("unknown3"),  # zero?
    UInt16("unknown4"),
    UInt16("unknown5"),
    UInt16("unknown6"),
    UInt32("unknown7"),
    SIZE=56
    )

script_syntax_data_header_os = dict(script_syntax_data_header)
script_syntax_data_header_os[1] = UInt16("data array length", DEFAULT=28501)

device_flags = (
    "initially open",  # value of 1.0
    "initially off",  # value of 0.0
    "can change only once",
    "position reversed",
    "not usable from any side"
    )

location_types = (
    "none",
    "ctf",
    "slayer",
    "oddball",
    "king",
    "race",
    "terminator",
    "stub",
    "ignored1",
    "ignored2",
    "ignored3",
    "ignored4",
    "all games",
    "all games except ctf",
    "all games except ctf and race"
    )

group_indices = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

squad_states = (
    "none",
    "sleeping",
    "alert",
    "moving - repeat same position",
    "moving - loop",
    "moving - loop back and forth",
    "moving - loop randomly",
    "moving - randomly",
    "guarding",
    "guarding at position",
    "searching",
    "fleeing"
    )

maneuver_when_states = (
    "never",
    {NAME: "strength at 75 percent", GUI_NAME: "< 75% strength"},
    {NAME: "strength at 50 percent", GUI_NAME: "< 50% strength"},
    {NAME: "strength at 25 percent", GUI_NAME: "< 25% strength"},
    "anybody dead",
    {NAME: "dead at 25 percent", GUI_NAME: "25% dead"},
    {NAME: "dead at 50 percent", GUI_NAME: "50% dead"},
    {NAME: "dead at 75 percent", GUI_NAME: "75% dead"},
    "all but one dead",
    "all dead"
    )

atom_types = (
    "pause",
    "goto",
    "goto and face",
    "move in direction",
    "look",
    "animation mode",
    "crouch",
    "shoot",
    "grenade",
    "vehicle",
    "running jump",
    "targeted jump",
    "script",
    "animate",
    "recording",
    "action",
    "vocalize",
    "targeting",
    "initiative",
    "wait",
    "loop",
    "die",
    "move immediate",
    "look random",
    "look player",
    "look object",
    "set radius",
    "teleport"
    )


sky = Struct("sky",
    dependency("sky", "sky "),
    SIZE=16
    )

child_scenario = Struct("child scenario",
    dependency("child scenario", "scnr"),
    SIZE=32
    )

function = Struct('function',
    BBool32('flags',
        'scripted',
        'invert',
        'additive',
        'always active',
        ),
    ascii_str32('name'),
    float_sec('period'),  # seconds
    dyn_senum16('scale period by', DYN_NAME_PATH="..[DYN_I].name"),
    BSEnum16('function', *animation_functions),
    dyn_senum16('scale function by', DYN_NAME_PATH="..[DYN_I].name"),
    BSEnum16('wobble function', *animation_functions),
    float_sec('wobble period'),  # seconds
    BFloat('wobble magnitude', SIDETIP="%"),  # percent
    BFloat('square wave threshold'),
    BSInt16('step count'),
    BSEnum16('map to', *fade_functions),
    BSInt16('sawtooth count'),

    Pad(2),
    dyn_senum16('scale result by', DYN_NAME_PATH="..[DYN_I].name"),
    BSEnum16('bounds mode',
        'clip',
        'clip and normalize',
        'scale to fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn off with', DYN_NAME_PATH="..[DYN_I].name"),

    SIZE=120
    )

comment = Struct("comment",
    QStruct("position", INCLUDE=xyz_float),
    Pad(16),
    rawtext_ref("comment data", StrLatin1, max_size=16384),
    SIZE=48
    )

object_name = Struct("object name",
    ascii_str32("name"),
    SIZE=36
    )

# Object references
scenery = object_reference("scenery", SIZE=72, block_name="sceneries")

biped = object_reference("biped",
    Pad(40),
    float_zero_to_one("body vitality"),
    BBool32("flags",
        "dead",
        ),
    SIZE=120
    )

vehicle = object_reference("vehicle",
    Pad(40),
    float_zero_to_one("body vitality"),
    BBool32("flags",
        "dead",
        ),

    Pad(8),
    SInt8("multiplayer team index"),
    Pad(1),
    BBool16("multiplayer spawn flags",
        "slayer default",
        "ctf default",
        "king default",
        "oddball default",
        #"unused1",
        #"unused2",
        #"unused3",
        #"unused4",
        ("slayer allowed", 1<<8),
        ("ctf allowed", 1<<9),
        ("king allowed", 1<<10),
        ("oddball allowed", 1<<11),
        #"unused5",
        #"unused6",
        #"unused7",
        #"unused8",
        ),
    SIZE=120
    )

equipment = object_reference("equipment",
    BBool32("misc flags",
        "initially at rest",
        # "obsolete",
        {NAME: "can accelerate", VALUE: 1<<2,
         GUI_NAME:"moves due to explosions"},
        ),
    SIZE=40
    )

weapon = object_reference("weapon",
    Pad(40),
    BSInt16("rounds left"),
    BSInt16("rounds loaded"),
    BBool16("flags",
        "initially at rest",
        # "obsolete",
        {NAME: "can accelerate", VALUE: 1<<2,
         GUI_NAME:"moves due to explosions"},
        ),
    SIZE=92
    )

device_group = Struct("device group",
    ascii_str32("name"),
    float_zero_to_one("initial value"),
    BBool32("flags",
        "can change only once"
        ),
    SIZE=52
    )

machine = object_reference("machine",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    BBool32("flags", *device_flags),
    BBool32("more flags",
        "does not operate automatically",
        "one-sided",
        "never appears locked",
        "opened by melee attack",
        ),
    SIZE=64
    )

control = object_reference("control",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    BBool32("flags", *device_flags),
    BBool32("more flags",
        "usable from both sides",
        ),
    BSInt16("DONT TOUCH THIS"),  # why?
    SIZE=64
    )

light_fixture = object_reference("light fixture",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH="tagdata.device_groups.STEPTREE[DYN_I].name"),
    BBool32("flags", *device_flags),
    QStruct("color", INCLUDE=rgb_float),
    BFloat("intensity"),
    BFloat("falloff angle"),  # radians
    BFloat("cutoff angle"),  # radians
    SIZE=88
    )

sound_scenery = object_reference("sound scenery", SIZE=40, block_name="sound_sceneries")

# Object palettes
scenery_palette = object_palette("scenery palette", "scen")
biped_palette = object_palette("biped palette", "bipd")
vehicle_palette = object_palette("vehicle palette", "vehi")
equipment_palette = object_palette("equipment palette", "eqip")
weapon_palette = object_palette("weapon palette", "weap")
machine_palette = object_palette("machine palette", "mach")
control_palette = object_palette("control palette", "ctrl")
light_fixture_palette = object_palette("light fixture palette", "lifi")
sound_scenery_palette = object_palette("sound scenery palette", "ssce")

player_starting_profile = Struct("player starting profile",
    ascii_str32("name"),
    float_zero_to_one("starting health modifier"),
    float_zero_to_one("starting shield modifier"),
    dependency("primary weapon", "weap"),
    BSInt16("primary rounds loaded"),
    BSInt16("primary rounds total"),
    dependency("secondary weapon", "weap"),
    BSInt16("secondary rounds loaded"),
    BSInt16("secondary rounds total"),
    SInt8("starting frag grenade count", MIN=0),
    SInt8("starting plasma grenade count", MIN=0),
    SIZE=104
    )

player_starting_location = Struct("player starting location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    BSInt16("team index"),
    BSInt16("bsp index"),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),
    SIZE=52
    )

trigger_volume = Struct("trigger volume",
    LUInt32("unknown", ENDIAN='<', DEFAULT=1, EDITABLE=False),
    ascii_str32("name"),
    # find out what if these fields actually what i'm calling them
    QStruct("normal",   INCLUDE=ijk_float),
    QStruct("binormal", INCLUDE=ijk_float),
    QStruct("tangent",  INCLUDE=ijk_float),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("sides",
        BFloat("w"), BFloat("l"), BFloat("h"),
        ORIENT='h'
        ),
    SIZE=96,
    COMMENT="I'm not sure if these are the actual names, but they seem to fit."
    )

recorded_animation = Struct("recorded animation",
    ascii_str32("name"),
    SInt8("version"),
    SInt8("raw animation data"),
    SInt8("unit control data version"),
    Pad(1),
    BSInt16("length of animation", SIDETIP="ticks"),  # ticks
    Pad(6),
    rawdata_ref("recorded animation event stream", max_size=2097152),
    SIZE=64
    )

netgame_flag = Struct("netgame flag",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    BSEnum16("type",
        "ctf - flag",
        "ctf - vehicle",
        "oddball - ball spawn",
        "race - track",
        "race - vehicle",
        "vegas - bank",
        "teleport - from",
        "teleport - to",
        "hill - flag",
        ),
    BSInt16("team index"),
    dependency("weapon group", "itmc"),
    SIZE=148
    )

netgame_equipment = Struct("netgame equipment",
    BBool32("type",
        "levitate"
        ),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),
    BSInt16("team index"),
    BSInt16("spawn time", SIDETIP="seconds(0 = default)",
            UNIT_SCALE=sec_unit_scale),  # seconds

    Pad(48),
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    dependency("item collection", "itmc"),
    SIZE=144
    )

starting_equipment = Struct("starting equipment",
    BBool32("type",
        "no grenades",
        "plasma grenades",
        ),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),

    Pad(48),
    dependency("item collection 1", "itmc"),
    dependency("item collection 2", "itmc"),
    dependency("item collection 3", "itmc"),
    dependency("item collection 4", "itmc"),
    dependency("item collection 5", "itmc"),
    dependency("item collection 6", "itmc"),
    SIZE=204
    )

bsp_switch_trigger_volume = Struct("bsp switch trigger volume",
    dyn_senum16("trigger volume",
        DYN_NAME_PATH="tagdata.trigger_volumes.STEPTREE[DYN_I].name"),
    BSInt16("source"),
    BSInt16("destination"),
    SIZE=8
    )

decal = Struct("decal",
    dyn_senum16("decal type",
        DYN_NAME_PATH="tagdata.decals_palette.STEPTREE[DYN_I].name.filepath"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=16
    )

decal_palette = object_palette("decal palette", "deca", 16)
detail_object_collection_palette = object_palette(
    "detail object collection palette", "dobc")
actor_palette = object_palette("actor palette", "actv", 16)

ai_anim_reference = Struct("ai animation reference",
    ascii_str32("animation name"),
    dependency("animation graph", "antr"),
    SIZE=60
    )

ai_script_reference = Struct("ai script reference",
    ascii_str32("script name"),
    SIZE=40
    )

ai_recording_reference = Struct("ai recording reference",
    ascii_str32("recording name"),
    SIZE=40
    )

script = Struct("script",
    ascii_str32("script name"),
    BSEnum16("script type", *script_types),
    BSEnum16("return type", *script_object_types),
    BSInt32("root expression index"),
    SIZE=92
    )

halo_global = Struct("halo global",
    ascii_str32("global name"),
    BSEnum16("type", *script_object_types),
    Pad(6),
    BSInt32("initialization expression index"),
    SIZE=92
    )

reference = Struct("tag reference",
    Pad(24),
    dependency("reference"),
    SIZE=40
    )

source_file = Struct("source_file",
    ascii_str32("source name"),
    rawdata_ref("source", max_size=262144, widget=HaloScriptSourceFrame),
    SIZE=52
    )

cutscene_flag = Struct("cutscene flag",
    Pad(4),
    ascii_str32("name"),
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("facing"),  # radians
    SIZE=92
    )

cutscene_camera_point = Struct("cutscene camera point",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("orientation"),  # radians
    float_rad("field of view"),  # radians
    SIZE=104
    )

cutscene_title = Struct("cutscene title",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("text bounds",
        BSInt16("t"), BSInt16("l"), BSInt16("b"), BSInt16("r"),
        ORIENT='h',
        ),
    BSInt16("string index"),
    BSEnum16("text style",
        "plain",
        "bold",
        "italic",
        "condense",
        "underline",
        ),
    BSEnum16("justification",
        "left",
        "right",
        "center",
        ),

    Pad(6),
    #QStruct("text color", INCLUDE=argb_byte),
    #QStruct("shadow color", INCLUDE=argb_byte),
    UInt32("text color", INCLUDE=argb_uint32),
    UInt32("shadow color", INCLUDE=argb_uint32),
    float_sec("fade in time"),  # seconds
    float_sec("up time"),  # seconds
    float_sec("fade out time"),  # seconds
    SIZE=96
    )

structure_bsp = Struct("structure bsp",
    FlUInt32("bsp pointer", VISIBLE=False),
    FlUInt32("bsp size", VISIBLE=False),
    FlUInt32("bsp magic", VISIBLE=False),
    Pad(4),
    dependency("structure bsp", "sbsp"),
    SIZE=32
    )


move_position = Struct("move position",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    BFloat("weight"),
    from_to_sec("time"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    SInt8("sequence id"),

    Pad(45),
    BSInt32("surface index"),
    SIZE=80
    )

actor_starting_location = Struct("starting location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    Pad(2),
    SInt8("sequence id"),
    Bool8("flags",
        "required",
        ),
    BSEnum16("return state", *squad_states),
    BSEnum16("initial state", *squad_states),
    dyn_senum16("actor type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("command list",
        DYN_NAME_PATH="tagdata.command_lists.STEPTREE[DYN_I].name"),
    SIZE=28
    )

squad = Struct("squad",
    ascii_str32("name"),
    dyn_senum16("actor type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("platoon",
        DYN_NAME_PATH=".....platoons.STEPTREE[DYN_I].name"),
    BSEnum16("initial state", *squad_states),
    BSEnum16("return state", *squad_states),
    BBool32("flags",
        "unused",
        "never search",
        "start timer immediately",
        "no timer, delay forever",
        "magic sight after timer",
        "automatic migration",
        ),
    BSEnum16("unique leader type",
        "normal",
        "none",
        "random",
        "sgt johnson",
        "sgt lehto",
        ),

    Pad(30),
    dyn_senum16("maneuver to squad", DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),
    float_sec("squad delay time"),  # seconds
    BBool32("attacking", *group_indices),
    BBool32("attacking search", *group_indices),
    BBool32("attacking guard", *group_indices),
    BBool32("defending", *group_indices),
    BBool32("defending search", *group_indices),
    BBool32("defending guard", *group_indices),
    BBool32("pursuing", *group_indices),

    Pad(12),
    BSInt16("normal diff count"),
    BSInt16("insane diff count"),
    BSEnum16("major upgrade",
        "normal",
        "few",
        "many",
        "none",
        "all",
        ),

    Pad(2),
    BSInt16("respawn min actors"),
    BSInt16("respawn max actors"),
    BSInt16("respawn total"),

    Pad(2),
    from_to_sec("respawn delay"),

    Pad(48),
    reflexive("move positions", move_position, 31),
    reflexive("starting locations", actor_starting_location, 31),
    SIZE=232
    )

platoon = Struct("platoon",
    ascii_str32("name"),
    BBool32("flags",
        "flee when maneuvering",
        "say advancing when maneuvering",
        "start in defending state",
        ),

    Pad(12),
    BSEnum16("change attacking/defending state", *maneuver_when_states),
    dyn_senum16("change happens to", DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    BSEnum16("maneuver when", *maneuver_when_states),
    dyn_senum16("maneuver happens to", DYN_NAME_PATH="..[DYN_I].name"),
    SIZE=172
    )

firing_position = Struct("firing position",
    QStruct("position", INCLUDE=xyz_float),
    BSEnum16("group index", *group_indices),
    SIZE=24
    )

encounter = Struct("encounter",
    ascii_str32("name"),
    BBool32("flags",
        "not initially created",
        "respawn enabled",
        "initially blind",
        "initially deaf",
        "initially braindead",
        "firing positions are 3d",
        "manual bsp index specified",
        ),
    BSEnum16("team index",
        "0 / default by unit",
        "1 / player",
        "2 / human",
        "3 / covenant",
        "4 / flood",
        "5 / sentinel",
        "6 / unused6",
        "7 / unused7",
        "8 / unused8",
        "9 / unused9"
        ),
    BSInt16('unknown'),
    BSEnum16("search behavior",
        "normal",
        "never",
        "tenacious"
        ),
    BSInt16("manual bsp index"),
    from_to_sec("respawn delay"),

    Pad(76),
    reflexive("squads", squad, 64),
    reflexive("platoons", platoon, 32, DYN_NAME_PATH='.name'),
    reflexive("firing positions", firing_position, 512),
    reflexive("player starting locations", player_starting_location, 256),
    
    SIZE=176
    )

command = Struct("command",
    BSEnum16("atom type", *atom_types),
    BSInt16("atom modifier"),
    BFloat("parameter 1"),
    BFloat("parameter 2"),
    dyn_senum16("point 1", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("point 2", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    dyn_senum16("script",
        DYN_NAME_PATH="tagdata.scripts.STEPTREE[DYN_I].script_name"),
    dyn_senum16("recording",
        DYN_NAME_PATH="tagdata.ai_recording_references.STEPTREE[DYN_I].recording_name"),
    dyn_senum16("command", DYN_NAME_PATH="..[DYN_I].atom_type.enum_name"),
    dyn_senum16("object name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    SIZE=32
    )

point = Struct("point",
    QStruct("position", INCLUDE=xyz_float),
    SIZE=20
    )

command_list = Struct("command list",
    ascii_str32("name"),
    BBool32("flags",
        "allow initiative",
        "allow targeting",
        "disable looking",
        "disable communication",
        "disable falling damage",
        "manual bsp index",
        ),

    Pad(8),
    BSInt16("manual bsp index"),

    Pad(2),
    reflexive("commands", command, 64),
    reflexive("points", point, 64),
    SIZE=96
    )

participant = Struct("participant",
    Pad(3),
    Bool8("flags",
        "optional",
        "has alternate",
        "is alternate",
        ),
    BSEnum16("selection type",
        "friendly actor",
        "disembodied",
        "in players vehicle",
        "not in a vehicle",
        "prefer sergeant",
        "any actor",
        "radio unit",
        "radio sergeant",
        ),
    BSEnum16("actor type", *actor_types),
    dyn_senum16("use this object", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    dyn_senum16("set new name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),

    Pad(12),
    BytesRaw("unknown", DEFAULT=b"\xFF"*12, SIZE=12),
    ascii_str32("encounter name"),
    SIZE=84
    )

line = Struct("line",
    BBool16("flags",
        "addressee look at speaker",
        "everyone look at speaker",
        "everyone look at addressee",
        "wait until told to advance",
        "wait until speaker nearby",
        "wait until everyone nearby",
        ),
    dyn_senum16("participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),
    BSEnum16("addressee",
        "none",
        "player",
        "participant",
        ),
    dyn_senum16("addressee participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),

    Pad(4),
    BFloat("line delay time"),

    Pad(12),
    dependency("variant 1", "snd!"),
    dependency("variant 2", "snd!"),
    dependency("variant 3", "snd!"),
    dependency("variant 4", "snd!"),
    dependency("variant 5", "snd!"),
    dependency("variant 6", "snd!"),
    SIZE=124
    )

ai_conversation = Struct("ai conversation",
    ascii_str32("name"),
    BBool16("flags",
        "stop if death",
        "stop if damaged",
        "stop if visible enemy",
        "stop if alerted to enemy",
        "player must be visible",
        "stop other actions",
        "keep trying to play",
        "player must be looking",
        ),

    Pad(2),
    float_wu("trigger distance"),
    float_wu("run-to-player distance"),

    Pad(36),
    reflexive("participants", participant, 8,
        DYN_NAME_PATH='.encounter_name'),
    reflexive("lines", line, 32),
    SIZE=116
    )

scnr_body = Struct("tagdata",
    dependency("DONT USE", 'sbsp'),
    dependency("WONT USE", 'sbsp'),
    dependency("CANT USE", 'sky '),
    reflexive("skies", sky, 8, DYN_NAME_PATH='.sky.filepath'),
    BSEnum16("type",
        "singleplayer",
        "multiplayer",
        "main menu"
        ),
    BBool16("flags",
        "cortana hack",
        "use demo ui"
        ),
    reflexive("child scenarios", child_scenario, 16,
        DYN_NAME_PATH='.child_scenario.filepath'),
    float_rad("local north"),  # radians

    Pad(156),
    reflexive("predicted resources", predicted_resource, 1024),
    reflexive("functions", function, 32,
        DYN_NAME_PATH='.name'),
    rawdata_ref("scenario editor data", max_size=65536),
    reflexive("comments", comment, 1024),

    Pad(224),
    reflexive("object names", object_name, 512,
        DYN_NAME_PATH='.name'),
    reflexive("sceneries", scenery, 2000),
    reflexive("sceneries palette", scenery_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("bipeds", biped, 128),
    reflexive("bipeds palette", biped_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("vehicles", vehicle, 80),
    reflexive("vehicles palette", vehicle_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("equipments", equipment, 256),
    reflexive("equipments palette", equipment_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("weapons", weapon, 128),
    reflexive("weapons palette", weapon_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("device groups", device_group, 128,
        DYN_NAME_PATH='.name'),
    reflexive("machines", machine, 400),
    reflexive("machines palette", machine_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("controls", control, 100),
    reflexive("controls palette", control_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("light fixtures", light_fixture, 500),
    reflexive("light fixtures palette", light_fixture_palette, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("sound sceneries", sound_scenery, 256),
    reflexive("sound sceneries palette", sound_scenery_palette, 100,
        DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("player starting profiles", player_starting_profile, 256,
        DYN_NAME_PATH='.name'),
    reflexive("player starting locations", player_starting_location, 256),
    reflexive("trigger volumes", trigger_volume, 256,
        DYN_NAME_PATH='.name'),
    reflexive("recorded animations", recorded_animation, 1024,
        DYN_NAME_PATH='.name'),
    reflexive("netgame flags", netgame_flag, 200,
        DYN_NAME_PATH='.type.enum_name'),
    reflexive("netgame equipments", netgame_equipment, 200,
        DYN_NAME_PATH='.item_collection.filepath'),
    reflexive("starting equipments", starting_equipment, 200),
    reflexive("bsp switch trigger volumes", bsp_switch_trigger_volume, 256),
    reflexive("decals", decal, 65535),
    reflexive("decals palette", decal_palette, 128,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("detail object collection palette",
        detail_object_collection_palette, 32, DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("actors palette", actor_palette, 64,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("encounters", encounter, 128, DYN_NAME_PATH='.name'),
    reflexive("command lists", command_list, 256, DYN_NAME_PATH='.name'),
    reflexive("ai animation references", ai_anim_reference, 128,
        DYN_NAME_PATH='.animation_name'),
    reflexive("ai script references", ai_script_reference, 128,
        DYN_NAME_PATH='.script_name'),
    reflexive("ai recording references", ai_recording_reference, 128,
        DYN_NAME_PATH='.recording_name'),
    reflexive("ai conversations", ai_conversation, 128,
        DYN_NAME_PATH='.name'),
    rawdata_ref("script syntax data", max_size=380076),
    rawdata_ref("script string data", max_size=262144),
    reflexive("scripts", script, 512, DYN_NAME_PATH='.script_name'),
    reflexive("globals", halo_global, 128, DYN_NAME_PATH='.global_name'),
    reflexive("references", reference, 256,
              DYN_NAME_PATH='.reference.filepath'),
    reflexive("source files", source_file, 8, DYN_NAME_PATH='.source_name'),

    Pad(24),
    reflexive("cutscene flags", cutscene_flag, 512, DYN_NAME_PATH='.name'),
    reflexive("cutscene camera points", cutscene_camera_point, 512,
        DYN_NAME_PATH='.name'),
    reflexive("cutscene titles", cutscene_title, 64, DYN_NAME_PATH='.name'),
    Pad(12), # unknown reflexive

    Pad(96),
    dependency("custom object names", 'ustr'),
    dependency("ingame help text", 'ustr'),
    dependency("hud messages", 'hmt '),
    reflexive("structure bsps", structure_bsp, 16,
        DYN_NAME_PATH='.structure_bsp.filepath'),
    SIZE=1456,
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )