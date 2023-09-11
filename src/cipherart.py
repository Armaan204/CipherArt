import png
import os

# Set the working directory to your desired location
os.chdir('your-directory')

# Unique string for message identification
MESSAGE_TERMINATOR = "011001100110011001100110"

def encode_message_as_binary(msg):
    # Convert the message into a binary string
    bin_message = ''.join(format(ord(char), '08b') for char in msg)
    bin_message += MESSAGE_TERMINATOR
    return bin_message

def load_image_data(image_file):
    # Read image data from a PNG file
    image_data = png.Reader(image_file).read()
    pixel_rows = list(image_data[2])
    return pixel_rows

def embed_message_in_pixels(pixels, message):
    '''Embeds the message into the image pixels'''
    message_index = 0
    for row in pixels:
        for i in range(len(row)):
            if message_index >= len(message):
                return pixels  # Stop encoding when message is exhausted
            if row[i] % 2 != int(message[message_index]):
                if row[i] == 0:
                    row[i] = 1
                else:
                    row[i] = row[i] - 1
            message_index += 1
    return pixels

def save_encoded_image(pixels, output_file):
    png.from_array(pixels, 'RGB').save(output_file)

def extract_message_from_pixels(pixels):
    extracted_message = []
    for row in pixels:
        for c in row:
            extracted_message.append(str(c % 2))
    extracted_message = ''.join(extracted_message)
    message = decode_message(extracted_message)
    return message

def decode_message(binary_message):
    binary_message = binary_message.split(MESSAGE_TERMINATOR)[0]
    message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])
    return message

MENU = """
Custom Image Encryption Tool

1. Encode a message into an image
2. Decode a message from an image
3. Exit
"""

def main():
    print(MENU)
    user_choice = ""
    while user_choice not in ("1", "2", "3"):
        user_choice = input("Your choice: ")

    if user_choice == "1":
        image_file = input("Enter the filename of the PNG image to encode: ")
        message_to_encode = input("Enter the message to encode: ")

        print("-ENCODING-")
        pixels = load_image_data(image_file)
        binary_message = encode_message_as_binary(message_to_encode)
        encoded_pixels = embed_message_in_pixels(pixels, binary_message)
        save_encoded_image(encoded_pixels, image_file + "-encoded.png")
        print("Message encoded successfully!")

    elif user_choice == "2":
        image_file = input("Enter the filename of the PNG image to decode: ")
        print("-DECODING-")
        pixels = load_image_data(image_file)
        extracted_message = extract_message_from_pixels(pixels)
        print("Decoded message:", extracted_message)

if __name__ == "__main__":
    main()
