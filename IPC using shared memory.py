import multiprocessing
import time
from multiprocessing import shared_memory
import numpy as np

def writer(shared_name, shape):
    existing_shm = shared_memory.SharedMemory(name=shared_name)
    shared_array = np.ndarray(shape, dtype=np.int64, buffer=existing_shm.buf)
    for i in range(len(shared_array)):
        shared_array[i] = i * 10
    print("Writer has written data to the shared memory.")
    existing_shm.close()

def reader(shared_name, shape):
    time.sleep(1)
    existing_shm = shared_memory.SharedMemory(name=shared_name)
    shared_array = np.ndarray(shape, dtype=np.int64, buffer=existing_shm.buf)
    print("Reader read data from the shared memory.", shared_array[:])
    existing_shm.close()
    existing_shm.unlink()

if __name__ == '__main__':
    shape = (200,)
    shm = shared_memory.SharedMemory(create=True, size=np.ndarray(shape, dtype=np.int64).nbytes)
    shared_array = np.ndarray(shape, dtype=np.int64,buffer=shm.buf)
    writer_process = multiprocessing.Process(target=writer, args=(shm.name, shape))
    reader_process = multiprocessing.Process(target=reader, args=(shm.name, shape))
    writer_process.start()
    reader_process.start()
    writer_process.join()
    reader_process.join()
    shm.close()
    shm.unlink()
