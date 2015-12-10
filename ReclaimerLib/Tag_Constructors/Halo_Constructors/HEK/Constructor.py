from supyr_struct.Constructor import Constructor as TC
from ....Tag_Descriptors.Halo_Descriptors.HEK.Objs.Tag_Obj import Halo_Tag_Obj
from .Field_Types import *


class Constructor(TC):
    Default_Defs_Path = "ReclaimerLib\\Tag_Descriptors\\Halo_Descriptors\\HEK\\"
    Default_Tag_Obj   = Halo_Tag_Obj

    #used whenever we need to know the extension of a tag based
    #on it's FourCC all 83 Halo 1 tag types are defined below
    ID_Ext_Mapping = {b"\x00\x00\x00\x00":".unknown_tag",
                      "":".unknown_tag",
                      'actr':".actor",                              #NEED
                      'actv':".actor_varient",                      #NEED
                      'ant!':".antenna",                            #NEED
                      'bipd':".biped",                              #NEED
                      'bitm':".bitmap",
                      'trak':".camera_track",                       #NEED
                      'colo':".color_table",                        #NEED
                      'cdmg':".continuous_damage_effect",           #NEED
                      'cont':".contrail",                           #NEED
                      'deca':".decal",                              #NEED
                      'udlg':".dialogue",                           #NEED
                      'dobc':".detail_object_collection",           #NEED
                      'devi':".device",                             #----
                      'ctrl':".device_control",                     #NEED
                      'lifi':".device_light_fixture",               #NEED
                      'mach':".device_machine",                     #NEED
                      'jpt!':".damage_effect",                      #NEED
                      'effe':".effect",                             #NEED
                      'eqip':".equipment",                          #NEED
                      'flag':".flag",                               #NEED
                      'fog ':".fog",                                #NEED
                      'font':".font",                               #NEED
                      'garb':".garbage",                            #NEED
                      'mod2':".gbxmodel",                           #NEED
                      'matg':".globals",                            #NEED
                      'glw!':".glow",                               #NEED
                      'grhi':".grenade_hud_interface",              #NEED
                      'hudg':".hud_globals",                        #NEED
                      'hmt ':".hud_message_text",
                      'hud#':".hud_number",                         #NEED
                      'devc':".input_device_defaults",              #NEED
                      'item':".item",                               #----
                      'itmc':".item_collection",                    #NEED
                      'lens':".lens_flare",                         #NEED
                      'ligh':".light",                              #NEED
                      'mgs2':".light_volume",                       #NEED
                      'elec':".lightning",                          #NEED
                      'foot':".material_effects",                   #NEED
                      'metr':".meter",
                      'mode':".model",                              #NEED
                      'antr':".model_animations",                   #NEED
                      'coll':".model_collision_geometry",           #NEED
                      'mply':".multiplayer_scenario_description",   #NEED
                      'obje':".object",                             #----
                      'part':".particle",                           #NEED
                      'pctl':".particle_system",                    #NEED
                      'phys':".physics",                            #NEED
                      'plac':".placeholder",                        #----
                      'pphy':".point_physics",
                      'ngpr':".preferences_network_game",           #NEED
                      'proj':".projectile",                         #NEED
                      'scnr':".scenario",                           #NEED
                      'sbsp':".scenario_structure_bsp",             #NEED
                      'scen':".scenery",                            #NEED
                      'snd!':".sound",                              #NEED
                      'snde':".sound_environment",                  #NEED
                      'lsnd':".sound_looping",                      #NEED
                      'ssce':".sound_scenery",                      #NEED
                      'boom':".spheroid",
                      'shdr':".shader",                             #----
                      'schi':".shader_transparent_chicago",
                      'scex':".shader_transparent_chicago_extended",
                      'sotr':".shader_transparent_generic",
                      'senv':".shader_environment",
                      'sgla':".shader_transparent_glass",           #NEED
                      'smet':".shader_transparent_meter",           #NEED
                      'soso':".shader_model",
                      'spla':".shader_transparent_plasma",          #NEED
                      'swat':".shader_transparent_water",           #NEED
                      'sky ':".sky",                                #NEED
                      'str#':".string_list",
                      'tagc':".tag_collection",
                      'Soul':".ui_widget_collection",               #NEED
                      'DeLa':".ui_widget_definition",               #NEED
                      'ustr':".unicode_string_list",
                      'unit':".unit",                               #NEED
                      'unhi':".unit_hud_interface",                 #NEED
                      'vehi':".vehicle",                            #NEED
                      'vcky':".virtual_keyboard",                   #NEED
                      'weap':".weapon",                             #NEED
                      'wphi':".weapon_hud_interface",               #NEED
                      'rain':".weather_particle_system",            #NEED
                      'wind':".wind"                                #NEED
                      }

    Ext_ID_Mapping = {}

    for key in ID_Ext_Mapping.keys():
        Ext_ID_Mapping[ID_Ext_Mapping[key]] = key

    def __init__(self, *args, **kwargs):
        TC.__init__(self, *args, **kwargs)

        #remove the autogenerated ID_Ext_Mapping to use the above one
        del self.__dict__['ID_Ext_Mapping']
        

    def Get_Cls_ID(self, Filepath):
        '''It is more reliable to determine a Halo tag
        based on its 4CC Cls_ID than by file extension'''
        try:            
            with open(Filepath, 'r+b') as Tag_File:
                Tag_File.seek(36)
                Cls_ID = str(Tag_File.read(4), 'latin-1')
                
            if Cls_ID in self.Definitions:
                return Cls_ID
        except:
            return None