from collections import Counter
from pathlib import Path

# Standard English letter frequencies (%)
ENGLISH_FREQUENCIES = {
    'e': 12.0, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31,
    'n': 6.95, 's': 6.28, 'r': 6.02, 'h': 5.92, 'd': 4.32,
    'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30,
    'y': 2.11, 'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
    'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11, 'j': 0.10, 'z': 0.07
}

def analyze_frequency(text: str) -> dict[str, float]:
    """Calculates percentage frequency of alphabetic characters in the text."""
    letters = [char.lower() for char in text if char.isalpha()]
    total_letters = len(letters)
    
    if total_letters == 0: #if somehow file is empty.
        return {}
        
    counts = Counter(letters)
    return {char: (count / total_letters) * 100 for char, count in counts.items()}


def generate_frequency_mapping(cipher_text: str) -> dict[str, str]:
    """
    Maps cipher letters to standard English letters based on ranked frequencies.
    """
    cipher_freqs = analyze_frequency(cipher_text)
    
    # Sort cipher letters by frequency (descending)
    sorted_cipher = [pair[0] for pair in sorted(cipher_freqs.items(), key=lambda item: item[1], reverse=True)]
    
    # Sort English reference letters by frequency (descending)
    sorted_english = [pair[0] for pair in sorted(ENGLISH_FREQUENCIES.items(), key=lambda item: item[1], reverse=True)]
    
    # Map ranked cipher letters directly to ranked English letters
    return dict(zip(sorted_cipher, sorted_english))


def generate_frequency_mapping_with_overrides(
    cipher_text: str,
    manual_overrides: dict[str, str],
) -> dict[str, str]:
    """Build a frequency mapping while reserving letters used by overrides."""
    overrides = {
        cipher_letter.lower(): english_letter.lower()
        for cipher_letter, english_letter in manual_overrides.items()
    }
    if len(set(overrides.values())) != len(overrides):
        raise ValueError("Manual overrides must map to unique English letters.")

    cipher_frequencies = analyze_frequency(cipher_text)
    ranked_cipher = sorted(
        cipher_frequencies,
        key=cipher_frequencies.get,
        reverse=True,
    )
    ranked_english = sorted(
        ENGLISH_FREQUENCIES,
        key=ENGLISH_FREQUENCIES.get,
        reverse=True,
    )

    available_cipher = [letter for letter in ranked_cipher if letter not in overrides]
    reserved_english = set(overrides.values())
    available_english = [
        letter for letter in ranked_english if letter not in reserved_english
    ]
    automatic_mapping = dict(zip(available_cipher, available_english))
    return {**automatic_mapping, **overrides}


def decrypt_text(text: str, mapping: dict[str, str]) -> str:
    """Decrypts text using the provided mapping while preserving casing and non-alpha characters."""
    decoded_chars = []
    for char in text:
        lower_char = char.lower()
        if lower_char in mapping:
            mapped_char = mapping[lower_char]
            decoded_chars.append(mapped_char.upper() if char.isupper() else mapped_char)
        else:
            decoded_chars.append(char)
    return "".join(decoded_chars)


def main():
    input_file = Path("PartA/cipher3a.txt")
    output_file = Path("PartA/cipher3a_decoded.txt")

    if not input_file.exists():
        print(f"Error: {input_file} not found.")
        return

    cipher_text = input_file.read_text(encoding="utf-8")

    # Override specific letters manually once you spot words until the text is fully decoded. This is a one-time manual override to speed up the process.
    manual_overrides = {
        's':'h',
        'f':'r',
        'o':'w',
        'k':'a',
        'y':'m',
        'u':'i',
        'z':'n',
        'n':'g',
        'e':'f',
        'v':'j',
        'q':'y',
        'm':'v',
        'r':'z',
        'i':'b',
    }

    final_mapping = generate_frequency_mapping_with_overrides(cipher_text, manual_overrides)

    # With the method of redoing the final mapping based on manual overrides, 
    # we remove duplicates and speed up the process of finding the correct mapping. 

    decoded_text = decrypt_text(cipher_text, final_mapping)

    output_file.write_text(decoded_text, encoding="utf-8")
    print(f"Decoded text written to {output_file}")
    
    print('Key:"' + "".join(
        final_mapping.get(cipher_letter, "?")
        for cipher_letter in "abcdefghijklmnopqrstuvwxyz"
    ) + '"')

    

if __name__ == "__main__":
    main()