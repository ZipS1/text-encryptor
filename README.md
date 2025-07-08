# Text-Encryptor

A simple console application that **embeds text into images** (and extracts it) using the Least Significant Bit (LSB) method. Each character is converted to its 8-bit binary ASCII representation, split into 3-2-3 bits for the R, G, and B channels, then hidden in the image’s pixel data.

**Text-Encryptor** provides two operations:
1. **Encrypt**: Hide a text message inside a BMP image file.  
2. **Decrypt**: Recover the hidden text from an encrypted image, given the same seed used during encryption.

## Prerequisites

- Python 3.7 or higher  
- [Pillow](https://pypi.org/project/Pillow/) library  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/ZipS1/text-encryptor.git
   cd text-encryptor
   ```
2. Install dependencies:  
   ```bash
   pip install Pillow
   ```

## Usage

All commands assume you are in the repository directory and that your images/text files are in the same folder as `main.py`.

1. **Run the program**  
   ```bash
   python main.py
   ```
2. **Encrypt a message**  
   - Choose **encrypt** from the menu.  
   - Enter the source image filename (e.g., `input.bmp`).  
   - Enter your text (manually or load from a file).  
   - Enter a numeric seed (any integer) to randomize pixel selection.  
   - Enter the output image filename (e.g., `encrypted.bmp`).  

3. **Decrypt a message**  
   - Choose **decrypt** from the menu.  
   - Enter the encrypted image filename.  
   - Enter the same seed used during encryption.  
   - View the recovered text on screen or save it to a file.

## Technology Stack

- Python 3  
- [Pillow](https://pypi.org/project/Pillow/) (PIL)  
- Standard library modules: `os`, `sys`, `random`, `itertools`
