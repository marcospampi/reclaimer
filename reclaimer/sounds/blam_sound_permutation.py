import os

from traceback import format_exc

from reclaimer.sounds import constants, util, blam_sound_samples
from supyr_struct.defs.audio.wav import wav_def


class BlamSoundPermutation:
    # permutation properties
    _source_sample_data = b''
    _source_compression = constants.COMPRESSION_PCM_16_LE
    _source_sample_rate = constants.SAMPLE_RATE_22K
    _source_encoding = constants.ENCODING_MONO

    # processed properties
    _processed_samples = ()

    def __init__(self, sample_data=b'',
                 compression=constants.COMPRESSION_PCM_16_LE,
                 sample_rate=constants.SAMPLE_RATE_22K,
                 encoding=constants.ENCODING_MONO, **kwargs):
        self.load_source_samples(
            sample_data, compression, sample_rate, encoding)

    @property
    def source_sample_data(self):
        return self._source_sample_data
    @property
    def source_compression(self):
        return self._source_compression
    @property
    def source_sample_rate(self):
        return self._source_sample_rate
    @property
    def source_encoding(self):
        return self._source_encoding

    @property
    def processed_samples(self):
        return self._processed_samples
    @property
    def compression(self):
        try:
            return self.processed_samples[0].compression
        except Exception:
            return self._source_compression
    @property
    def sample_rate(self):
        try:
            return self.processed_samples[0].sample_rate
        except Exception:
            return self._source_sample_rate
    @property
    def encoding(self):
        try:
            return self.processed_samples[0].encoding
        except Exception:
            return self._source_encoding

    def load_source_samples(self, sample_data, compression,
                            sample_rate, encoding):
        self._source_sample_data = sample_data
        self._source_compression = compression
        self._source_sample_rate = sample_rate
        self._source_encoding = encoding
        self._processed_samples = []

    def partition_samples(self, compression, sample_rate=None, chunk_size=0,
                          vorbis_bitrate_info=None):
        if (compression == constants.COMPRESSION_OGG and
            not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg encoder not available. Cannot partition.")

        if sample_rate is None:
            sample_rate = self.source_sample_rate

        chunk_size = util.calculate_sample_chunk_size(
            compression, chunk_size, encoding)

        sample_data = self.source_sample_data

        # TODO: Finish this

    def generate_mouth_data(self):
        for samples in self.processed_samples:
            samples.generate_mouth_data()

    def compress_samples(self, compression, sample_rate=None, encoding=None,
                         vorbis_bitrate_info=None):
        for samples in self.processed_samples:
            samples.compress(compression, sample_rate, encoding,
                             vorbis_bitrate_info)

    def get_concatenated_sample_data(self, target_compression=None,
                                     target_encoding=None):
        if target_compression is None:
            target_compression = self.source_compression
        if target_encoding is None:
            target_encoding = self.source_encoding

        assert target_encoding in constants.channel_counts

        if target_compression != self.compression or target_encoding != self.encoding:
            # decompress processed samples to the target compression
            sample_data = b''.join(
                p.get_decompressed(target_compression, target_encoding)
                for p in self.processed_samples)
        else:
            # join samples without decompressing
            compression = self.compression
            # make sure we're able to combine samples without decompressing
            for piece in self.processed_samples:
                if piece.compression != compression:
                    raise ValueError(
                        "Cannot combine differently compressed samples without decompressing.")
                elif piece.compression == constants.COMPRESSION_OGG:
                    raise ValueError(
                        "Cannot combine ogg samples without decompressing.")

            sample_data = b''.join(p.sample_data for p in self.processed_samples)

        return sample_data

    def get_concatenated_mouth_data(self):
        return b''.join(p.mouth_data for p in self.processed_samples)

    def regenerate_source(self):
        '''
        Regenerates an uncompressed, concatenated audio stream
        from the compressed samples. Use when loading a sound tag
        for re-compression, re-sampling, or re-encoding.
        '''
        # always regenerate to constants.DEFAULT_UNCOMPRESSED_FORMAT
        # because, technically speaking, that is highest sample depth
        # we can ever possibly see in Halo CE.
        self._source_sample_data = self.get_concatenated_sample_data(
            constants.DEFAULT_UNCOMPRESSED_FORMAT, self.encoding)
        self._source_compression = constants.DEFAULT_UNCOMPRESSED_FORMAT
        self._source_sample_rate = self.sample_rate
        self._source_encoding = self.encoding

    @staticmethod
    def create_from_file(filepath):
        try:
            new_perm = BlamSoundPermutation()
            new_perm.import_from_file(filepath)
        except Exception:
            print(format_exc())

        if not new_perm.source_sample_data:
            new_perm = None
        return new_perm

    def export_to_file(self, filepath_base, overwrite=False,
                       export_source=True, decompress=True):
        perm_chunks = []
        encoding = self.encoding
        sample_rate = self.sample_rate
        if export_source and self.source_sample_data:
            # export the source data
            perm_chunks.append(
                (self.compression, self.source_encoding, self.source_sample_data)
                )
            sample_rate = self.source_sample_rate
        elif self.processed_samples:
            # concatenate processed samples if source samples don't exist.
            # also, if compression is ogg, we have to decompress
            compression = self.compression
            if decompress or compression == constants.COMPRESSION_OGG:
                compression = constants.COMPRESSION_PCM_16_LE

            try:
                sample_data = self.get_concatenated_sample_data(
                    compression, encoding)
                if sample_data:
                    perm_chunks.append((compression, self.encoding, sample_data))
            except Exception:
                perm_chunks.extend(
                    (piece.compression, piece.encoding, piece.sample_data)
                    for piece in self.processed_samples
                    )

        i = -1
        wav_file = wav_def.build()
        for compression, encoding, sample_data in perm_chunks:
            i += 1
            filepath = util.BAD_PATH_CHAR_REMOVAL.sub("_", filepath_base)

            if len(perm_chunks) > 1:
                filepath += "__%s" % i

            # figure out if the sample data is already encapsulated in a
            # container, or if it'll need to be encapsulated in a wav file.
            is_container_format = True
            if compression == constants.COMPRESSION_OGG:
                ext = ".ogg"
            elif compression == constants.COMPRESSION_WMA:
                ext = ".wma"
            elif compression == constants.COMPRESSION_UNKNOWN:
                ext = ".bin"
            else:
                is_container_format = False
                ext = ".wav"

            if os.path.splitext(filepath)[1].lower() != ext:
                filepath += ext

            if not sample_data or (not overwrite and os.path.isfile(filepath)):
                continue

            if is_container_format:
                try:
                    folderpath = os.path.dirname(filepath)
                    # If the path doesnt exist, create it
                    if not os.path.exists(folderpath):
                        os.makedirs(folderpath)

                    with open(filepath, "wb") as f:
                        f.write(sample_data)
                except Exception:
                    print(format_exc())

                continue

            wav_file.filepath = filepath

            wav_fmt = wav_file.data.format
            wav_fmt.fmt.data = constants.WAV_FORMAT_PCM
            wav_fmt.channels = constants.channel_counts.get(encoding, 1)
            wav_fmt.sample_rate = sample_rate

            samples_len = len(sample_data)
            if compression in constants.PCM_FORMATS:
                # one of the uncompressed pcm formats
                if util.is_big_endian_pcm(compression):
                    sample_data = util.convert_pcm_to_pcm(
                        sample_data, compression,
                        util.change_pcm_endianness(compression))

                sample_width = constants.sample_widths[compression]
                wav_fmt.bits_per_sample = sample_width * 8
                wav_fmt.block_align = sample_width * wav_fmt.channels
                wav_fmt.byte_rate = wav_fmt.sample_rate * wav_fmt.block_align
            elif compression == constants.COMPRESSION_ADPCM:
                # 16bit adpcm
                wav_fmt.fmt.data = constants.WAV_FORMAT_IMA_ADPCM
                wav_fmt.bits_per_sample = 16
                wav_fmt.block_align = constants.ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    (wav_fmt.sample_rate * wav_fmt.block_align /
                     (constants.ADPCM_DECOMPRESSED_BLOCKSIZE // 2))
                    )
            else:
                print("Unknown compression method:", compression)
                continue

            wav_file.data.wav_data.audio_data = sample_data
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)

            #continue
            orig_mouth_data = self.get_concatenated_mouth_data()
            if orig_mouth_data:
                # multiply by 4 so audacity can import it at 120Hz
                orig_mouth_data = b''.join(bytes([b])*4 for b in orig_mouth_data)
                with open(filepath + ".ORIG.mouth", "wb") as f:
                    f.write(orig_mouth_data)

                self.generate_mouth_data()
                gen_mouth_data = self.get_concatenated_mouth_data()
                gen_mouth_data = b''.join(bytes([b])*4 for b in gen_mouth_data)
                with open(filepath + ".MADE.mouth", "wb") as f:
                    f.write(gen_mouth_data)

                with open(filepath + ".DIFF.mouth", "wb") as f:
                    f.write(bytes(abs(gen_mouth_data[i] - orig_mouth_data[i])
                                  for i in range(len(gen_mouth_data))))

    def import_from_file(self, filepath):
        if not os.path.isfile(filepath):
            raise OSError('File "%s" does not exist. Cannot import.' % filepath)

        wav_file = wav_def.build(filepath=filepath)
        wav_header = wav_file.data.wav_header
        wav_format = wav_file.data.format
        wav_data = wav_file.data.wav_data
        if wav_header.riff_sig != wav_header.get_desc("DEFAULT", "riff_sig"):
            raise ValueError(
                "RIFF signature is invalid. Not a valid wav file.")
        elif wav_header.wave_sig != wav_header.get_desc("DEFAULT", "wave_sig"):
            raise ValueError(
                "WAVE signature is invalid. Not a valid wav file.")
        elif wav_format.sig != wav_format.get_desc("DEFAULT", "sig"):
            raise ValueError(
                "Format signature is invalid. Not a valid wav file.")
        elif wav_format.fmt.data not in constants.ALLOWED_WAV_FORMATS:
            raise ValueError(
                'Invalid compression format "%s".' % wav_format.fmt.data)
        elif wav_format.channels not in (1, 2):
            raise ValueError(
                "Invalid number of channels. Must be 1 or 2, not %s." %
                wav_format.channels)
        elif wav_format.sample_rate == 0:
            raise ValueError(
                "Sample rate cannot be zero. Not a valid wav file")
        elif (wav_format.fmt.data == constants.WAV_FORMAT_PCM and
              wav_format.bits_per_sample not in (8, 16, 24, 32)):
            raise ValueError(
                "Pcm sample width must be 8, 16, 24, or 32, not %s." %
                wav_format.bits_per_sample)

        if wav_data.audio_data_size != len(wav_data.audio_data):
            print("Audio sample data length does not match available data "
                  "length. Sample data may be truncated.")

        if wav_format.block_align and (len(wav_data.audio_data) %
                                       wav_format.block_align):
            print("Audio sample data length not a multiple of block_align. "
                  "Sample data may be truncated.")

        sample_width = None
        encoding = constants.ENCODING_MONO
        if wav_format.fmt.data == constants.WAV_FORMAT_PCM:
            sample_width = wav_format.bits_per_sample // 8

        if wav_format.channels == 2:
            encoding = constants.ENCODING_STEREO

        compression = constants.wav_format_mapping.get(
            (wav_format.fmt.data, sample_width))

        self.load_source_samples(
            wav_data.audio_data, compression,
            wav_format.sample_rate, encoding)
