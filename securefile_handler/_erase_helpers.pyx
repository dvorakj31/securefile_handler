from libc.stdlib cimport rand, srand
from libc.stdio cimport FILE, fopen, fclose, fseek, ftell, rewind, fwrite, fflush, SEEK_END, SEEK_SET
from libc.time cimport time
from pathlib import Path
import errors


srand(time(NULL))


def shred_file(const char* path, unsigned long long int file_size, int cycle_counter=3):
    cdef:
        FILE* input_file = fopen(path, 'wb+')
        unsigned long long int i, _
        char val[1]
    if input_file == NULL:
        raise errors.CannotReadFileError(f'Cannot read file {path}')
    for i in range(cycle_counter):
        rewind(input_file)
        for _ in range(file_size):
            val[0] = i if i < 2 else rand()
            fwrite(val, sizeof(val), 1, input_file)
        fflush(input_file)
    fclose(input_file)
