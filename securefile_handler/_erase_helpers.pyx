"""
This module defines functions for safe file erasing.
Algorithm for erasing is defined by British HMG Infosec Standard 5, Enhanced Standard.
Algorithm pseudocode:
    Open file

    In first round rewrite all bytes to zeros

    In second round rewrite all bytes to ones

    In third round rewrite all bytes to random values

Algorithm is defined in shred_file function.
"""


from libc.stdlib cimport rand, srand
from libc.stdio cimport FILE, fopen, fclose, rewind, fwrite, fflush
from libc.time cimport time
from cpython.mem cimport PyMem_Malloc, PyMem_Free
cimport cython
from . import errors


srand(time(NULL))


cdef _write_to_file(FILE* file, unsigned long long int number_of_bytes, char* buffer):
    """
    Function that writes bytes from buffer to file.
    
    :param file: Output file
    :param number_of_bytes: buffer size
    :param buffer: byte-string that will be written to file

    """
    fwrite(buffer, sizeof(char), number_of_bytes, file)


cdef _rewrite_file_chunks(FILE* input_file, unsigned long long int file_size, unsigned long long chunk_size,
                          char* buffer):
    """
    Function that writes bytes chunk by chunk to input_file
    
    :param input_file: File where buffer will be written. 
    :param file_size: Size of file in bytes
    :param chunk_size: Size of chunk in bytes
    :param buffer: Buffer that will be written to file
    """
    cdef unsigned long long int i = 0
    while i < file_size - chunk_size and file_size > chunk_size:
        _write_to_file(input_file, chunk_size, buffer)
        i += chunk_size
    _write_to_file(input_file, file_size - i, buffer)
    fflush(input_file)
    rewind(input_file)
    PyMem_Free(buffer)


@cython.boundscheck(False)
@cython.wraparound(False)
def shred_file(const char* path, unsigned long long int file_size, unsigned long long int chunk_size):
    """
    Cythonized function for shredding file.

    :param path: String path to file
    :param file_size: Size of file in bytes
    :param chunk_size: Size of chunk in bytes

    """
    cdef:
        FILE* input_file = fopen(path, 'wb+')
        unsigned long long int i = 0, _, counter
        char val[1]
        char *buffer_of_zeros = NULL
        char *buffer_of_ones = NULL
        char *buffer_of_rand = NULL
    if input_file == NULL:
        raise errors.CannotReadFileError(f'Cannot read file {path}')
    buffer_of_zeros = <char*>PyMem_Malloc(chunk_size * sizeof(char))
    buffer_of_ones = <char*>PyMem_Malloc(chunk_size * sizeof(char))
    if buffer_of_zeros == NULL or buffer_of_ones == NULL:
        PyMem_Free(buffer_of_zeros)
        PyMem_Free(buffer_of_ones)
        fclose(input_file)
        raise MemoryError()
    for i in range(chunk_size):
        buffer_of_zeros[i] = 0
        buffer_of_ones[i] = -1
    _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_zeros)
    _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_ones)
    buffer_of_rand = <char*>PyMem_Malloc(chunk_size * sizeof(char))
    if buffer_of_rand == NULL:
        fclose(input_file)
        raise MemoryError()
    for i in range(chunk_size):
        buffer_of_rand[i] = rand()
    _rewrite_file_chunks(input_file, file_size, chunk_size, buffer_of_rand)
    fclose(input_file)
