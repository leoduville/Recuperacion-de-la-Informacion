import struct
import time

def encode_vbyte(number):
    bytes_list = []
    while True:
        bytes_list.insert(0, number & 0x7F)
        number >>= 7
        if number == 0:
            break
    bytes_list[-1] |= 0x80  # Set the most significant bit of the last byte
    return bytes_list

def decompress_docId(docIds_filename):

    with open(docIds_filename, 'rb') as binary_file:
        byte_data = binary_file.read()

    format_string = f">{len(byte_data)}B"
    unpacked_data = struct.unpack(format_string, byte_data)
    result = []
    docId = 0
    n = 1
    for data in unpacked_data:
        if data >=128:
            docId +=  data - 128 
            result.append(docId)
            docId = 0
            n = 1
        else:
            docId+= data * 128 * n 
            n +=1
    return result
    
def encode_elias_gamma(number):
    if number == 0:
        return [0]
    
    # Encuentra el número de bits necesarios para representar number
    bit_length = number.bit_length()
    
    # Crea el código de prefijo con longitud igual a bit_length - 1
    prefix = [0] * (bit_length - 1)
    
    # Crea el código de sufijo con los bits de la representación binaria de number
    suffix = [int(bit) for bit in bin(number)[2:]]
    
    # Combina el prefijo y el sufijo
    return prefix + suffix

def decode_elias_gamma(encoded_number):
    if encoded_number == '0':
        return 0
    length = 0
    while encoded_number[length] == '0':
        length += 1
    binary_representation = '1' + encoded_number[length+1:length*2+1]
    return int(binary_representation, 2)

def compress_index(index_filename, dgaps):
    compressed_doc_ids_filename = "compressed_docIds.bin"
    compressed_freqs_filename = "compressed_frequencies.bin"

    doc_ids = []
    freqs = []

    doc_id_anterior = 0
    with open(index_filename, 'rb') as index_file:
        while True:
            data = index_file.read(8)
            if not data:
                break
            doc_id, freq = struct.unpack('>II', data)
            if dgaps: 
                if doc_id > doc_id_anterior:
                    doc_id_aux = doc_id
                    doc_id = doc_id - doc_id_anterior
                    doc_id_anterior = doc_id_aux
                else:
                    doc_id_anterior = doc_id
            doc_ids.append(doc_id)
            freqs.append(freq)

    with open(compressed_doc_ids_filename, 'wb') as doc_ids_file:
        for doc_id in doc_ids:
            array_data= encode_vbyte(doc_id)
            byte_data = struct.pack(f">{len(array_data)}B", *array_data)
            doc_ids_file.write(byte_data)

    with open(compressed_freqs_filename, 'wb') as freqs_file:
        for freq in freqs:
            encoded_freq = encode_elias_gamma(freq)
            for bit in encoded_freq:
                bit_data = struct.pack('b', bit)
                freqs_file.write(bit_data)

    print("Índice comprimido y almacenado en archivos separados.")

def read_bits_from_file(file):
    with open(file, 'rb') as binary_file:
        bit_data = binary_file.read()

    format_string = f">{len(bit_data)}b"
    unpacked_data = struct.unpack(format_string, bit_data)
    return unpacked_data

def concatenate_bits(bits):
    result = 0
    for bit in bits:
        result = (result << 1) | bit
    return result

def binary_list_to_decimal(binary_list):
    pos = len(binary_list)
    num = 0
    for binary in binary_list:
        num += binary * 2 ** pos
        pos -= 1
    return num

def decode_elias_gamma(bits):
    decoded_numbers = []
    count_zeros = 0    
    bandera = False
    num = []
    for bit in bits:
        if bandera and count_zeros != 0:
            num.append(bit)
            count_zeros -= 1
        if not bandera:
            if bit == 0:
                count_zeros += 1
            if bit == 1:
                count = count_zeros
                bandera = True
        if bandera and count_zeros == 0:
            num_final = 2 ** count + binary_list_to_decimal(num)
            decoded_numbers.append(num_final)
            count = 0
            bandera = False
            num = []
    return decoded_numbers

def decompress_freqs(compressed_freqs_filename):
    compressed_bits = read_bits_from_file(compressed_freqs_filename)
    return decode_elias_gamma(compressed_bits)

start_time = time.time()
compress_index('final_index.bin', True)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo Compresión: {elapsed_time}")

start_time = time.time()
decompress_docId('compressed_docIds.bin')
decompressed_freqs = decompress_freqs("compressed_frequencies.bin")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo Descompresión: {elapsed_time}")