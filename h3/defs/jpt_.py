from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

jpt_category = (
    "none",
    "falling",
    "bullet",
    "grenade",
    "high_explosive",
    "sniper",
    "melee",
    "flame",
    "mounted_weapon",
    "vehicle",
    "plasma",
    "needle",
    "shotgun",
    )

jpt_player_response_fade_function = (
    "linear",
    "late",
    "very_late",
    "early",
    "very_early",
    "cosine",
    "zero",
    "one",
    )

jpt_player_response_priority = (
    "low",
    "medium",
    "high",
    )

jpt_player_response_response_type = (
    "shielded",
    "unshielded",
    "all",
    )

jpt_player_response_type = (
    "none",
    "lighten",
    "darken",
    "max",
    "min",
    "invert",
    "tint",
    )

jpt_side_effect = (
    "none",
    "harmless",
    "lethal_to_the_unsuspecting",
    "emp",
    )

jpt_wobble_function = (
    "one",
    "zero",
    "cosine",
    "cosine_variable_period",
    "diagonal_wave",
    "diagonal_wave_variable_period",
    "slide",
    "slide_variable_period",
    "noise",
    "jitter",
    "wander",
    "spark",
    )


jpt_player_response = Struct("player_responses",
    SEnum16("response_type", *jpt_player_response_response_type),
    SInt16("unknown"),
    SEnum16("type", *jpt_player_response_type),
    SEnum16("priority", *jpt_player_response_priority),
    Float("duration"),
    SEnum16("fade_function", *jpt_player_response_fade_function),
    SInt16("unknown_1"),
    Float("maximum_intensity"),
    Float("color_alpha"),
    Float("color_red"),
    Float("color_green"),
    Float("color_blue"),
    Float("low_frequency_vibration_duration"),
    rawdata_ref("low_frequency_vibration_function"),
    Float("high_frequency_vibration_duration"),
    rawdata_ref("high_frequency_vibration_function"),
    string_id_meta("effect_name"),
    Float("duration_1"),
    rawdata_ref("effect_scale_function"),
    ENDIAN=">", SIZE=112
    )


jpt__meta_def = BlockDef("jpt!",
    Float("radius_min"),
    Float("radius_max"),
    Float("cutoff_scale"),
    Bool32("flags",
        "don_t_scale_damage_by_distance",
        "area_damage_players_only",
        ),
    SEnum16("side_effect", *jpt_side_effect),
    SEnum16("category", *jpt_category),
    Bool32("flags_1",
        "does_not_hurt_owner",
        "can_cause_headshots",
        "pings_resistant_units",
        "does_not_hurt_friends",
        "does_not_ping_units",
        "detonates_explosives",
        "only_hurts_shields",
        "causes_flaming_death",
        "damage_indicators_always_point_down",
        "skips_shields",
        "only_hurts_one_infection_form",
        ("infection_form_pop", 1 << 12),
        "ignore_seat_scale_for_direct_damage",
        "forces_hard_ping",
        "does_not_hurt_players",
        ),
    Float("area_of_effect_core_radius"),
    Float("damage_lower_bound"),
    Float("damage_upper_bound_min"),
    Float("damage_upper_bound_max"),
    float_rad("damage_inner_cone_angle"),
    float_rad("damage_outer_cone_angle"),
    Float("active_camoflage_damage"),
    Float("stun"),
    Float("max_stun"),
    Float("stun_time"),
    Float("instantaneous_acceleration"),
    Float("rider_direct_damage_scale"),
    Float("rider_max_transfer_damage_scale"),
    Float("rider_min_transfer_damage_scale"),
    string_id_meta("general_damage"),
    string_id_meta("specific_damage"),
    string_id_meta("special_damage"),
    Float("ai_stun_radius"),
    Float("ai_stun_bounds_min"),
    Float("ai_stun_bounds_max"),
    Float("shake_radius"),
    Float("emp_radius"),
    Float("unknown"),
    Float("unknown_1"),
    reflexive("player_responses", jpt_player_response),
    dependency("damage_response"),
    Float("duration"),
    SEnum16("fade_function", *jpt_player_response_fade_function),
    SInt16("unknown_2"),
    float_rad("rotation"),
    Float("pushback"),
    Float("jitter_min"),
    Float("jitter_max"),
    Float("duration_1"),
    SEnum16("falloff_function", *jpt_player_response_fade_function),
    SInt16("unknown_3"),
    Float("random_translation"),
    float_rad("random_rotation"),
    SEnum16("wobble_function", *jpt_wobble_function),
    SInt16("unknown_4"),
    Float("wobble_function_period"),
    Float("wobble_weight"),
    dependency("sound"),
    Float("forward_velocity"),
    Float("forward_radius"),
    Float("forward_exponent"),
    Float("outward_velocity"),
    Float("outward_radius"),
    Float("outward_exponent"),
    TYPE=Struct, ENDIAN=">", SIZE=240
    )
