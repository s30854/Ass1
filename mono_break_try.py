alphabet = "abcdefghijklmnopqrstuvwxyz"

text_file = open("cipher3a.txt", "r")

cipher_text = text_file.read()

text_file.close()

# Frequency analysis

freq_in_cipher = {alphabet[i]: 0 for i in range(len(alphabet))}
total_letters = 0

for letter in cipher_text:
    if letter in freq_in_cipher:
        freq_in_cipher[letter] += 1
        total_letters += 1

#print([f"{letter}: {freq_in_cipher[letter]}" for letter in freq_in_cipher])
#print(f"Total letters: {total_letters}")

for letter in freq_in_cipher:
    freq_in_cipher[letter] /= total_letters/100 

#print([f"{letter}: {freq_in_cipher[letter]}" for letter in freq_in_cipher])

# h has highest frequency so we can set it to e.

mapping = {'j':'t', 's':'h', 'h':'e'}

# Change each h to e and print it out into a new filemapping = {'h': 'e'}

decoded_text_manual = ''.join(mapping.get(letter, letter) for letter in cipher_text)

with open("cipher3a_decoded.txt", "w") as output_file:
    output_file.write(decoded_text_manual)

# Could make a dict with the "known" frequencies and compare them to what we have. Then we could auto associate the letters with the similar frequencies.

letterFrequency = {
    'E' : 12.0,
    'T' : 9.10,
    'A' : 8.12,
    'O' : 7.68,
    'I' : 7.31,
    'N' : 6.95,
    'S' : 6.28,
    'R' : 6.02,
    'H' : 5.92,
    'D' : 4.32,
    'L' : 3.98,
    'U' : 2.88,
    'C' : 2.71,
    'M' : 2.61,
    'F' : 2.30,
    'Y' : 2.11,
    'W' : 2.09,
    'G' : 2.03,
    'P' : 1.82,
    'B' : 1.49,
    'V' : 1.11,
    'K' : 0.69,
    'X' : 0.17,
    'Q' : 0.11,
    'J' : 0.10,
    'Z' : 0.07 } #https://gist.github.com/pozhidaevak/0dca594d6f0de367f232909fe21cdb2f
    # Didn't feel like writing it myself. :)

# The frequency from cipher text closest to the known frequency of letters in English is likely to be that letter. So we can map them together.

best_mapping = {}

for cipher_letter, cipher_freq in freq_in_cipher.items():
    best_letter = min(
        letterFrequency,
        key=lambda plain_letter: abs(cipher_freq - letterFrequency[plain_letter])
    )
    #print(f"\'{cipher_letter}\':\'{best_letter}\',")
    best_mapping[cipher_letter] = best_letter


# Now we can use this to decode the text.

mapping2 = {
    'a':'T',
    'b':'P',
    'c':'D',
    'd':'Z',
    'e':'G',
    'f':'H',
    'g':'H',
    'h':'E',
    'i':'P',
    'j':'T',
    'k':'O',
    'l':'M',
    'm':'K',
    'n':'C',
    'o':'M',
    'p':'Q',
    'q':'P',
    'r':'X',
    's':'H',
    't':'P',
    'u':'S',
    'v':'K',
    'w':'V',
    'x':'L',
    'y':'C',
    'z':'I',
}
decoded_text = ''.join(mapping2.get(letter, letter) for letter in cipher_text)

with open("cipher3a_decoded2.txt", "w") as output_file:
    output_file.write(decoded_text)

# This has problems since there are multiple instances of the same letter in the mapping2. 
# So we will clean up the program, since the idea was established and put it in another file.