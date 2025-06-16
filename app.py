from flask import Flask, render_template, request
from markupsafe import Markup # <-- Import Markup from markupsafe

app = Flask(__name__)

#Extends the keyword to match the length of the text
def _extend_key(key, length):
    extended_key = key * (length // len(key) + 1)
    return extended_key[:length]

#Convert an uppercase letter to its corresponding interger equivalent
def _char_to_int(char):
    return ord(char.upper()) - ord('A')

#Convert a 0-25 integer to its uppercase letter equivalent
def _int_to_char(integer):
    return chr(integer + ord('A'))

#Encrypt plaintext using the Vigenere cipher
def encrypt_vigenere(plaintext, keyword):
    ciphertext = []
    # Clean and convert plaintext and keywprd to uppercase
    processed_plaintext = "".join(filter(str.isalpha, plaintext)).upper()
    processed_keyword = "".join(filter(str.isalpha, keyword)).upper()

    if not processed_keyword:
        return "Error: Keyword cannot be empty or contain only non-alphabetic character"
    if not processed_plaintext:
        return plaintext #If the processed plaintext is empty, return the plaintext
    
    extended_key = _extend_key(processed_keyword, len(processed_plaintext))

    key_index = 0

    #Iterate through original plaintext to preserve non-alphabetic charcthers
    for char in plaintext:
        if 'A' <= char.upper() <= 'Z':
            p_val = _char_to_int(char)
            k_val = _char_to_int(extended_key[key_index])
            c_val = (p_val + k_val) % 26
            encrypted_char = _int_to_char(c_val)
            if char.islower(): #Maintain original case
                ciphertext.append(encrypted_char.lower())
            else:
                ciphertext.append(encrypted_char)
            key_index += 1
        else:
            ciphertext.append(char)

    return "".join(ciphertext)

#Decrypt ciphertext using the Vigenere cipher
def decrypt_vigenere(ciphertext, keyword):
    plaintext = []
    # Clean and convert ciphertext and keyword to uppercase
    processed_ciphertext = "".join(filter(str.isalpha, ciphertext)).upper()
    processed_keyword = "".join(filter(str.isalpha, keyword)).upper()

    if not processed_keyword:
        return "Error: Keyword cannnot be empty or contain only non-alphabetic character"
    if not processed_ciphertext:
        return ciphertext # If the processed ciphertext is empty, return the original ciphertext

    extended_key = _extend_key(processed_keyword, len(processed_ciphertext))

    key_index = 0

    for char in ciphertext: # Iterate throuh original ciphertext
        if 'A' <= char.upper() <= 'Z':
            c_val = _char_to_int(char)
            k_val = _char_to_int(extended_key[key_index])
            p_val = (c_val - k_val + 26)% 26
            decrypted_char = _int_to_char(p_val)
            if char.islower(): # Maintain original case
                plaintext.append(decrypted_char.lower())
            else:
                plaintext.append(decrypted_char)
            key_index += 1 # Only advance key_index for alphabetic characters
        else:
            plaintext.append(char) # Keep non-

    return "".join(plaintext)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = ""
    keyword = ""
    operation = ""
    error = None

    if request.method == 'POST':
        input_text = request.form['input_text']
        keyword = request.form['keyword']
        operation = request.form['operation']

        # Basic validation for keyword (must contain at least one alphabet)
        if not any(char.isalpha() for char in keyword):
            error = "Keyword must contain at least one alphabetic character."
        else:
            if operation == 'encrypt':
                result = encrypt_vigenere(input_text, keyword)
            elif operation == 'decrypt':
                result = decrypt_vigenere(input_text, keyword)    

            # If the result itself is an error string from the cipher function
            if result and result.startswith("Error:"):
                error = result
                result = None # Clear result so it's not displayed as a successful output

    return render_template('index.html', result=result, input_text=input_text, keyword=keyword, operation=operation, error=error)

if __name__ == '__main__':
    app.run(debug=True)
