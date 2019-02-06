from libc.stdlib cimport rand, srand
from libc.stdio cimport FILE, fopen, fclose, rewind, fwrite, fflush
from libc.time cimport time
from cpython.mem cimport PyMem_RawMalloc, PyMem_RawFree
cimport cython
from . import errors


srand(time(NULL))


cdef _write_to_file(FILE* file, unsigned long long int number_of_bytes, char* buffer):
    fwrite(buffer, sizeof(char), number_of_bytes, file)
    fflush(file)


cdef _rewrite_file_chunks(FILE* input_file, unsigned long long int file_size, unsigned long long chunk_size,
                          char* buffer):
    cdef unsigned long long int i = 0
    while i < file_size - chunk_size:
        _write_to_file(input_file, chunk_size, buffer)
        i += chunk_size
    _write_to_file(input_file, file_size - i, buffer)


@cython.boundscheck(False)
@cython.wraparound(False)
def shred_file(const char* path, unsigned long long int file_size, unsigned long long int chunk_size):
    cdef:
        FILE* input_file = fopen(path, 'wb+')
        unsigned long long int i = 0, _, counter
        char val[1]
        char *buffer_of_zeros = NULL
        char *buffer_of_ones = NULL
        char *buffer_of_rand = NULL
    if input_file == NULL:
        raise errors.CannotReadFileError(f'Cannot read file {path}')
    buffer_of_zeros = <char*>PyMem_RawMalloc(chunk_size * sizeof(char))
    buffer_of_ones = <char*>PyMem_RawMalloc(chunk_size * sizeof(char))
    if buffer_of_zeros == NULL or buffer_of_ones == NULL:
        raise MemoryError()
    for i in range(chunk_size):
        buffer_of_zeros[i] = 0
        buffer_of_ones[i] = 1
    if file_size <= chunk_size:
        _write_to_file(input_file, file_size, buffer_of_zeros)
        PyMem_RawFree(buffer_of_zeros)
        rewind(input_file)
        _write_to_file(input_file, file_size, buffer_of_ones)
        PyMem_RawFree(buffer_of_ones)
        rewind(input_file)
        buffer_of_rand = <char*>PyMem_RawMalloc(file_size * sizeof(char))
        if buffer_of_rand == NULL:
           raise MemoryError()
        for i in range(file_size):
           buffer_of_rand[i] = rand()
        _write_to_file(input_file, file_size, buffer_of_rand)
        PyMem_RawFree(buffer_of_rand)
    else:
       _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_zeros)
       rewind(input_file)
       PyMem_RawFree(buffer_of_zeros)
       _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_ones)
       rewind(input_file)
       PyMem_RawFree(buffer_of_ones)
       buffer_of_rand = <char*>PyMem_RawMalloc(chunk_size * sizeof(char))
       if buffer_of_rand == NULL:
           raise MemoryError()
       for i in range(chunk_size):
           buffer_of_rand[i] = rand()
       _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_rand)
       PyMem_RawFree(buffer_of_rand)
    fclose(input_file)
