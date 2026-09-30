alphabet = "abcdefghijklmnopqrstuvwxyz"

with open("PartB/cipher3b.txt", "r") as text_file:
    cipher_text = text_file.read()

# I saw fpw at the start of the cipher. It repeats a couple of times in the text.
# We can use it to maybe find the key length.

# Let's make a script to find the distance between the repeating sequences of letters.

# Keep the original formatting of the file (line breaks and spaces) while searching.


def find_distances(sequence, text):
    sequence = sequence.lower()
    normalized_text = "".join(ch.lower() for ch in text if ch.isalpha())
    positions = []

    start = 0
    while True:
        index = normalized_text.find(sequence, start)
        if index == -1:
            break
        positions.append(index)
        start = index + 1

    if len(positions) < 2:
        print(f"Sequence '{sequence}' appears {len(positions)} time(s).")
        return []

    distances = []
    for i in range(1, len(positions)):
        distances.append(positions[i] - positions[i - 1])

    print(f"Sequence: {sequence}")
    print(f"Positions: {positions}")
    print(f"Distances: {distances}")
    return distances


find_distances("fpw", cipher_text)

# Since we can see it appears a few times. We can try to find keys so it makes words.

key = "mister" # Started with "mis" to change 'fpw' to 'the'
# Since we saw 'the zydne who' after putting mis we can assume
# that the start is defenitely of the key is 'mis'
# By using common words divisable by 3(because of the distance between real words), 
# I found mister worked first try.

def vigenere_decrypt(cipher_text, key):
    decrypted_text = []
    key_length = len(key)
    key_indices = [ord(k) - ord('a') for k in key.lower()]
    key_position = 0

    for char in cipher_text:
        if char.isalpha():
            shift = key_indices[key_position % key_length]
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            decrypted_text.append(decrypted_char.upper() if char.isupper() else decrypted_char)
            key_position += 1
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


decoded_text = vigenere_decrypt(cipher_text, key)

with open("PartB/cipher3b_decoded.txt", "w") as output_file:
    output_file.write(decoded_text)

# Our decoded text has fewer repetitions of the sequence "fpw" 
# means the key is probably longer. 


