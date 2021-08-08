""" ENCRYPTING PRINCIPLE
Каждый символ переводится в ASCII-число, затем в двоичную СС
RGB каналы пикселя также переводятся в двоичную СС

Двоичное представление числа делится на 3 части:
3, 2, 3 бита на каждый канал соответственно

Далее эти части вставляются в младшие разряды двоичного представления
каждого канала
"""

from PIL import Image  # TODO: make seed
import os
from sys import platform
import sys


class Encryptor:
    def __init__(self):
        self.curpix = None
        self.image = None

    def _setup_image(self, image_path):
        self.image = Image.open(image_path)
        self.image.load()

    def _get_next_pixel(self):
        if self.curpix is None:
            return (0, 0)

        xsize, ysize = self.image.size
        x, y = self.curpix

        if x < xsize - 1:
            return (x + 1, y)
        else:
            return (0, y + 1)

    def _split_char_to_channels(self, char):
        ascii_char = ord(char)
        bin_char = bin(ascii_char)[2:].rjust(8, "0")
        rcomp = bin_char[:3]
        gcomp = bin_char[3:5]
        bcomp = bin_char[5:]
        return (rcomp, gcomp, bcomp)

    def _encrypt_pixel(self, char, pix_rgb):
        ascii_comps = self._split_char_to_channels(char)
        new_rgb = []
        for ch_ind in range(3):
            ascii_comp = ascii_comps[ch_ind]
            bin_channel = bin(pix_rgb[ch_ind])[2:]
            new_channel = bin_channel[:-len(ascii_comp)] + ascii_comp
            new_rgb.append(new_channel)
        new_rgb = [int(i, 2) for i in new_rgb]
        return tuple(new_rgb)

    def encrypt(self, image_path, text, encrypted_image_name):
        self._setup_image(image_path)
        self.curpix = self._get_next_pixel()

        for char in text:
            pix_rgb = self.image.getpixel(self.curpix)
            encrypted_rgb = self._encrypt_pixel(char, pix_rgb)
            self.image.putpixel(self.curpix, encrypted_rgb)
            self.curpix = self._get_next_pixel()

        self._put_end_symbol()
        self.image.save(encrypted_image_name, "BMP")

    def _put_end_symbol(self):
        pix_rgb = self.image.getpixel(self.curpix)
        encrypted_rgb = self._encrypt_pixel("\0", pix_rgb)
        self.image.putpixel(self.curpix, encrypted_rgb)

    def _decrypt_pixel(self, pix_rgb):
        pix_rgb = list(pix_rgb)
        pix_rgb = [bin(i)[2:] for i in pix_rgb]

        bin_char = pix_rgb[0][-3:] + pix_rgb[1][-2:] + pix_rgb[2][-3:]
        return chr(int(bin_char, 2))

    def decrypt(self, image_path):
        self._setup_image(image_path)
        self.curpix = self._get_next_pixel()

        text = ""
        symbol = ""

        while symbol != "\0":
            rgb = self.image.getpixel(self.curpix)
            symbol = self._decrypt_pixel(rgb)
            text += symbol
            self.curpix = self._get_next_pixel()
        return text


class ConsoleUI():
    def __init__(self):
        self.enc = Encryptor()

    def run(self):
        self._clearwin()
        print("Welcome to Picture Encryptor")
        print("All files should be in same directory as this program")
        user_choice = self._choose_option(("encrypt", "decrypt"))
        if user_choice == "encrypt":
            self._encrypt_UI()
        else:
            self._decrypt_UI()

    def _choose_option(self, options_list): # DRY principle disturbance
        print("Enter number of option:")
        for i in range(len(options_list)):
            print(f"{i+1} - {options_list[i]}")

        valid_inputs = [str(i) for i in range(1, len(options_list)+ 1)]

        user_choice = input(": ")
        while user_choice not in valid_inputs:
            print("Incorrect input!")
            user_choice = input(": ")

        return options_list[int(user_choice) - 1]

    def _encrypt_UI(self):
        self._clearwin()
        image_name = input("Enter picture name: ")

        text_options = ("manual text input", "load text from file")
        user_choice = self._choose_option(text_options)

        if user_choice == "manual text input":
            text = input("Enter text: ")
        else:
            filename = input("Enter filename: ")
            with open(filename, "r") as f:
                text = f.read()

        output_image = input("Enter encrypted image filename: ")

        print("Encrypting...")
        self.enc.encrypt(image_name, text, output_image)
        print("Encrypting completed successfully!")
        os.system("pause")
        sys.exit()

    def _decrypt_UI(self):
        self._clearwin()
        image_name = input("Enter picture name: ")

        text_options = ("console output", "file output")
        user_choice = self._choose_option(text_options)

        print("Decrypting...")
        text = self.enc.decrypt(image_name)

        print("Decrypting completed successfully!")
        if user_choice == "console output":
            print("\n", text)
        else:
            filename = input("Enter output filename: ")
            with open(filename, "w") as f:
                w.write(text)
        os.system("pause")
        sys.exit()

    def _clearwin(self):
        if platform == "win32":
            os.system("cls")
        elif platform in ("linux", "darwin"):
            os.system("clear")
        else:
            print("Error: unknown OS")


def main():
    UI = ConsoleUI()
    UI.run()


if __name__ == '__main__':
    main()
