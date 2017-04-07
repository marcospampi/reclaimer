from ..hek.handler import HaloHandler

class Halo2XboxHandler(HaloHandler):
    default_defs_path = "reclaimer.h2x.defs"

    def get_def_id(self, filepath):
        if not filepath.startswith('.') and '.' in filepath:
            ext = splitext(filepath)[-1].lower()
        else:
            ext = filepath.lower()

        if ext in self.ext_id_map:
            return self.ext_id_map[ext]

        '''It is more reliable to determine a Halo tag
        based on its 4CC def_id than by file extension'''
        try:
            with open(filepath, 'r+b') as tagfile:
                tagfile.seek(36)
                def_id = str(tagfile.read(4), 'latin-1')
            tagfile.seek(60);
            engine_id = tagfile.read(4)
            if def_id in self.defs and engine_id == b'!MLB':
                return def_id
        except:
            return None
