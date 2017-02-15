from array import array
from .tag import *

import arbytmap as ab

ab.FORMAT_P8 = "P8-BUMP"

"""ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
ab.define_format(
    format_id=ab.FORMAT_P8, raw_format=True, channel_count=4,
    depths=(8,8,8,8), offsets=(24,16,8,0),
    masks=(4278190080, 16711680, 65280, 255))

#in a bitmap tag this number designates the type
TYPE_2D = 0
TYPE_3D = 1
TYPE_CUBEMAP = 2
TYPE_WHITE = 3

#in a bitmap tag this number designates the format
FORMAT_NONE = -1#this value is used ONLY in the conversion process

FORMAT_A8 = 0
FORMAT_Y8 = 1
FORMAT_AY8 = 2
FORMAT_A8Y8 = 3
FORMAT_R5G6B5 = 6
FORMAT_A1R5G5B5 = 8
FORMAT_A4R4G4B4 = 9
FORMAT_X8R8G8B8 = 10
FORMAT_A8R8G8B8 = 11
FORMAT_DXT1 = 14
FORMAT_DXT3 = 15
FORMAT_DXT5 = 16
FORMAT_P8 = 17

DXT_FORMATS = [FORMAT_DXT1,FORMAT_DXT3,FORMAT_DXT5]

PALLETIZED_FORMATS = [FORMAT_P8]

TYPE_NAME_MAP = ["2D", "3D", "CUBE"]

FORMAT_NAME_MAP = [
    "A8", "Y8", "AY8", "A8Y8",
    "UNUSED1", "UNUSED2",
    "R5G6B5",  "UNUSED3", "A1R5G5B5", "A4R4G4B4",
    "X8R8G8B8", "A8R8G8B8",
    "UNUSED4", "UNUSED5",
    "DXT1", "DXT3", "DXT5", "P8-BUMP", None]

#each bitmap's number of bytes must be a multiple of 512
BITMAP_PADDING = 512
#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128


class BitmTag(HekTag):

    tex_infos = ()
    
    def bitmap_count(self, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.size
        self.data.tagdata.bitmaps.size = new_value
        
    def bitmap_width(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].width
        self.data.tagdata.bitmaps.bitmaps_array[b_index].width = new_value

    def bitmap_height(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].height
        self.data.tagdata.bitmaps.bitmaps_array[b_index].height = new_value

    def bitmap_depth(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].depth
        self.data.tagdata.bitmaps.bitmaps_array[b_index].depth = new_value

    def bitmap_mipmaps_count(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].mipmaps
        self.data.tagdata.bitmaps.bitmaps_array[b_index].mipmaps = new_value

    def bitmap_type(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].type.data
        self.data.tagdata.bitmaps.bitmaps_array[b_index].type.data = new_value

    def bitmap_format(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].format.data
        self.data.tagdata.bitmaps.bitmaps_array[b_index].format.data = new_value


    def bitmap_width_height_depth(self, b_index=0, new_value=None):
        bitmap = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitmap.width, bitmap.height, bitmap.depth)
        bitmap.width, bitmap.height, bitmap.depth = (
            new_value[0], new_value[1], new_value[2])

    def bitmap_flags(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].flags
        self.data.tagdata.bitmaps.bitmaps_array[b_index].flags = new_value
        
    def bitmap_base_address(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.base_address)
        bitm.base_address=new_value

    def bitmap_data_offset(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.pixels_offset)
        bitm.pixels_offset=new_value

    def registration_point_x(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return bitm.registration_point_x
        bitm.registration_point_x = new_value

    def registration_point_y(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return bitm.registration_point_y
        bitm.registration_point_y = new_value

    def registration_point_xy(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.registration_point_x,
                   bitm.registration_point_y)
        bitm.registration_point_x, bitm.registration_point_y = new_value[0],\
                                                               new_value[1]

    @property
    def is_xbox_bitmap(self):
        #we only need to check the first bitmap
        return self.bitmap_base_address() == 1073751810
        
    def processed_by_reclaimer(self, new_flag=None):
        if new_flag is None:
            return self.data.tagdata.flags.processed_by_reclaimer
        self.data.tagdata.flags.processed_by_reclaimer = new_flag

    def is_power_of_2_bitmap(self, b_index=0):
        return self.bitmap_flags(b_index).power_of_2_dim
            
    def is_compressed_bitmap(self, b_index=0):
        return self.bitmap_flags(b_index).compressed
        
    def swizzled(self, new_flag=None, b_index = 0):
        if new_flag is None:
            return self.bitmap_flags(b_index).swizzled
        self.bitmap_flags(b_index).swizzled = new_flag

    def color_plate_data_bytes_size(self, new_value=None):
        if new_value is None:
            return(self.data.tagdata.compressed_color_plate_data.size)
        self.data.tagdata.compressed_color_plate_data.size = new_value

    def pixel_data_bytes_size(self, new_value=None):
        if new_value is None:
            return self.data.tagdata.processed_pixel_data.size
        self.data.tagdata.processed_pixel_data.size = new_value

    def set_platform(self, saveasxbox):
        '''changes different things to set the platform to either PC or Xbox'''
        #Read each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            bitmap = self.data.tagdata.bitmaps.bitmaps_array[b_index]
            
            bitmap.flags.set_to('xbox_bitmap', saveasxbox)

            '''base_address is the ONLY discernable difference
            between a bitmap made by arsenic from a PC map, and
            a bitmap made by arsenic from an original XBOX map'''
            if saveasxbox:
                #change some miscellaneous variables               
                bitmap.pixels = 4608
                bitmap.bitmap_data_pointer = -1
                bitmap.base_address = 1073751810
            else:
                bitmap.base_address = 0

        if not saveasxbox:
            return

        #if Xbox, reset these structure variable's all to 0
        #since xbox doesn't like them being non-zero
        tagdata = self.data.tagdata
        for i in (1,2,3):
            tagdata.compressed_color_plate_data[i] = 0
            tagdata.processed_pixel_data[i] = 0

        for i in (1,2):
            tagdata.sequences[i] = 0
            tagdata.bitmaps[i] = 0
                
        #swap the order of the cubemap faces
        #and mipmaps if saving to xbox format
        self.change_sub_bitmap_ordering(saveasxbox)

    def change_sub_bitmap_ordering(self, saveasxbox):
        '''Used to change the mipmap and cube face ordering.
        On pc all highest resolution faces are first, then
        the next highest resolution mipmap set. On xbox it's
        all of a face's mipmaps before any of the other faces.
        
        DO NOT UNDER ANY CIRCUMSTANCES CALL THIS FUNCTION
        IF PADDING HAS ALREADY BEEN ADDED TO A BITMAP'''

        raw_bitmap_data = self.data.tagdata.processed_pixel_data.data

        #Loop over each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            
            if self.bitmap_type(b_index) == TYPE_CUBEMAP:
                mipmap_count = self.bitmap_mipmaps_count(b_index) + 1
                tex_block = raw_bitmap_data[b_index]

                #this will be used to copy values from
                template = tex_block.__copy__()

                #this is used to keep track of which index
                #we're placing the new pixel array into
                i = 0
                
                '''since we also want to swap the second and third
                cubemap faces we can do that easily like this xbox
                has the second and third cubemap faces transposed
                with each other compared to pc. IDFKY'''
                for face in (0, 2, 1, 3, 4, 5):
                    for mip in range(0, mipmap_count*6, 6):
                        '''get the block we want from the original
                        layout and place it in its new position'''
                        if saveasxbox:
                            tex_block[i] = template[mip + face]
                        else:
                            tex_block[mip + face] = template[i]
                        i += 1

    def add_bitmap_padding(self, save_as_xbox):
        '''This function will create and apply padding to each of the
        bitmaps in the tag to make it XBOX compatible. This function will
        also add the number of bytes of padding to the internal offsets'''

        """The offset of each bitmap's pixel data needs to be increased by
        the padding of all the bitmaps before it. This variable will be
        used for knowing the total amount of padding before each bitmap.

        DO NOT RUN IF A BITMAP ALREADY HAS PADDING."""
        total_data_size = 0

        for i in range(self.bitmap_count()):
            sub_bitmap_count = 1
            if self.bitmap_type(i) == TYPE_CUBEMAP:
                sub_bitmap_count = 6
                
            pixel_data_block = self.data.tagdata.processed_pixel_data.data[i]

            """BECAUSE THESE OFFSETS ARE THE BEGINNING OF THE PIXEL
            DATA WE ADD THE NUMBER OF BYTES OF PIXEL DATA BEFORE
            WE CALCULATE THE NUMBER OF BYTES OF THIS ONE"""
            #apply the offset to the tag
            self.bitmap_data_offset(i, total_data_size)

            """ONLY ADD PADDING IF THE BITMAP IS P8 FORMAT OR GOING ON XBOX"""
            if save_as_xbox or self.bitmap_format(i) == ab.FORMAT_P8:
                #calculate how much padding to add to the xbox bitmaps
                bitmap_pad, cubemap_pad = self.get_padding_size(i)
                
                #add the number of bytes of padding to the total
                total_data_size += bitmap_pad + cubemap_pad*sub_bitmap_count

                #if this bitmap has padding on each of the sub-bitmaps
                if cubemap_pad:
                    mipmap_count = self.bitmap_mipmaps_count(i) + 1
                    for j in range(0, 6*(mipmap_count + 1), mipmap_count + 1):
                        pad = bytearray(cubemap_pad)
                        if isinstance(pixel_data_block[0], array):
                            pad = array('B', pad)
                        pixel_data_block.insert(j + mipmap_count, pad)
                        
                #add the main padding to the end of the bitmap block
                pad = bytearray(bitmap_pad)
                if isinstance(pixel_data_block[0], array):
                    pad = array('B', pad)
                pixel_data_block.append(pad)

            #add the number of bytes this bitmap is to the
            #total bytes so far(multiple by sub-bitmap count)
            total_data_size += self.get_bitmap_size(i)*sub_bitmap_count

        #update the total number of bytes of pixel data
        #in the tag by all the padding that was added
        self.pixel_data_bytes_size(total_data_size)

    def get_bitmap_size(self, b_index):
        '''Given a bitmap index, this function will
        calculate how many bytes the data takes up.
        THIS FUNCTION WILL NOT TAKE INTO ACCOUNT THE NUMBER OF SUB-BITMAPS'''

        #since we need this information to read the bitmap we extract it
        mw, mh, md, = self.bitmap_width_height_depth(b_index)
        format = FORMAT_NAME_MAP[self.bitmap_format(b_index)]

        #this is used to hold how many pixels in
        #total all this bitmaps mipmaps add up to
        pixel_count = 0
        
        for mipmap in range(self.bitmap_mipmaps_count(b_index) + 1):
            w, h, d = ab.get_mipmap_dimensions(mw, mh, md, mipmap, format)
            pixel_count += w*h*d

        bytes_count = pixel_count
        #based on the format, each pixel takes up a different amount of bytes
        if format != ab.FORMAT_P8:
            bytes_count = (bytes_count * ab.BITS_PER_PIXEL[format])//8

        return bytes_count

    def get_padding_size(self, b_index):
        '''Calculates how many bytes of padding need to be added
        to a bitmap to properly align it in the texture cache'''

        #first we need to know how many bytes the bitmap data takes up
        bytes_count = self.get_bitmap_size(b_index)
        cubemap_pad = 0

        #if there are sub-bitmaps we calculate the amount of padding for them
        if self.bitmap_type(b_index) == TYPE_CUBEMAP:
            cubemap_pad = ((CUBEMAP_PADDING - (bytes_count % CUBEMAP_PADDING))
                           % CUBEMAP_PADDING)
            bytes_count = (bytes_count + cubemap_pad) * 6

        bitmap_pad = (BITMAP_PADDING -
                      (bytes_count%BITMAP_PADDING))%BITMAP_PADDING
        
        return(bitmap_pad, cubemap_pad)

    def sanitize_mipmap_counts(self):
        '''Some original xbox bitmaps have fudged up mipmap counts
        and cause issues. This function will scan through all a
        bitmap's bitmaps and check that they fit within their
        calculated pixel data bounds. This is done by checking if a
        bitmap's calculated size is both within the side of the total
        pixel data and less than the next bitmap's pixel data start'''
        
        bad_bitmap_index_list = []
        bitmap_count = self.bitmap_count()
        
        for i in range(bitmap_count):

            #if this is the last bitmap
            if i + 1 == bitmap_count:
                #this is how many bytes of texture data there is total
                max_size = self.pixel_data_bytes_size()
            else:
                #this is the start of the next bitmap's pixel data
                max_size = self.bitmap_data_offset(i+1)
            
            while True:
                mipmap_count = self.bitmap_mipmaps_count(i)
                curr_size = self.get_bitmap_size(i) + self.bitmap_data_offset(i)

                if curr_size <= max_size:
                    break

                self.bitmap_mipmaps_count(i, mipmap_count - 1)

                #the mipmap count is zero and the bitmap still will
                #not fit within the space provided. Something's wrong
                if mipmap_count == 0:
                    bad_bitmap_index_list.append(i)
                    break

        return bad_bitmap_index_list

    def sanitize_bitmaps(self):
        tex_infos = self.tex_infos
        #after we've edited with the bitmap in whatever ways we did this will
        #tie up all the loose ends and recalculate all the offsets and stuff

        #Read the pixel data blocks for each bitmap
        for i in range(self.bitmap_count()):
            format = FORMAT_NAME_MAP[self.bitmap_format(i)]
            flags = self.bitmap_flags(i)
            old_w, old_h, _ = self.bitmap_width_height_depth(i)
            
            reg_point_x, reg_point_y = self.registration_point_xy(i)
            texinfo = tex_infos[i]
            
            #set the flags to the new value
            flags.palletized = (format == ab.FORMAT_P8)
            flags.compressed = (format in ab.COMPRESSED_FORMATS)
            
            self.bitmap_width_height_depth(
                i, (texinfo["width"], texinfo["height"], texinfo["depth"]))
            self.bitmap_mipmaps_count(i, texinfo["mipmap_count"])
            self.registration_point_xy(i, (texinfo["width"]*reg_point_x//old_w,
                                          texinfo["height"]*reg_point_y//old_h))
