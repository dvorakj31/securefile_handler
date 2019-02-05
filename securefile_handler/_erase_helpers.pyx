from libc.stdlib cimport rand, srand
from libc.stdio cimport FILE, fopen, fclose, fseek, ftell, rewind, fwrite, fflush, SEEK_END, SEEK_SET
from libc.time cimport time
from pathlib import Path
import errors


srand(time(NULL))

cdef:
    unsigned long long int CHUNK_SIZE = 16 * 1024 * 1024
    char buffer_of_zeros[16 * 1024 * 1024]
    char buffer_of_ones[16 * 1024 * 1024]
    char buffer_of_rand[16 * 1024 * 1024]


cdef _write_to_file(FILE* file, unsigned long long int number_of_bytes, char byte=-1):
    if byte == 0:
        fwrite(buffer_of_zeros, sizeof(char), number_of_bytes, file)
    elif byte == 1:
        fwrite(buffer_of_zeros, sizeof(char), number_of_bytes, file)
    elif byte == -1:
        for i in range(number_of_bytes):
            buffer_of_rand[i] = rand()
        fwrite(buffer_of_rand, sizeof(char), number_of_bytes, file)
    fflush(file)


cdef _rewrite_file_chunks(FILE* input_file, unsigned long long int file_size, char byte=-1):
    cdef unsigned long long int i = 0
    while i < file_size - CHUNK_SIZE:
        _write_to_file(input_file, CHUNK_SIZE, byte)
        i += CHUNK_SIZE
    _write_to_file(input_file, file_size - i, byte)

def shred_file(const char* path, unsigned long long int file_size, unsigned long long int chunk_size,
               int cycle_counter=3):
    cdef:
        FILE* input_file = fopen(path, 'wb+')
        unsigned long long int i = 0, _, counter
        char val[1]
    CHUNK_SIZE = chunk_size
    if input_file == NULL:
        raise errors.CannotReadFileError(f'Cannot read file {path}')
    for i in range(CHUNK_SIZE):
        buffer_of_zeros[i] = 0
        buffer_of_ones[i] = 1
    if file_size <= CHUNK_SIZE:
       _write_to_file(input_file, file_size, 0)
       rewind(input_file)
       _write_to_file(input_file, file_size, 1)
       rewind(input_file)
       _write_to_file(input_file, file_size)
    else:
       for i in range(2):
           _rewrite_file_chunks(input_file, file_size, i)
           rewind(input_file)
       _rewrite_file_chunks(input_file, file_size)
    fclose(input_file)
