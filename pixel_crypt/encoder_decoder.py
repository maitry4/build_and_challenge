import customtkinter as ctk
from PIL import Image
from typing import List, Iterator, Tuple

class SteganographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pixel Crypt")
        self.geometry("700x400")
        self.build()

    def build(self) -> None:
        """Lays out the GUI elements for encoding and decoding operations."""
        
        # Encoding Section
        self.encode_label = ctk.CTkLabel(self, text="Encode Message into Image")
        self.encode_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.image_path_entry = ctk.CTkEntry(self, placeholder_text="Enter image path")
        self.image_path_entry.grid(row=1, column=0, padx=20, pady=5)
        
        self.message_entry = ctk.CTkEntry(self, placeholder_text="Enter message to encode")
        self.message_entry.grid(row=2, column=0, padx=20, pady=5)
        
        self.resulting_image_entry = ctk.CTkEntry(self, placeholder_text="Enter resulting image path")
        self.resulting_image_entry.grid(row=3, column=0, padx=20, pady=5)
        
        self.encode_button = ctk.CTkButton(self, text="Encode", command=self.encode_image)
        self.encode_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.encode_result_label = ctk.CTkLabel(self, text="")
        self.encode_result_label.grid(row=5, column=0, padx=20, pady=5)

        # Decoding Section
        self.decode_label = ctk.CTkLabel(self, text="Decode Message from Image")
        self.decode_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.decode_image_path_entry = ctk.CTkEntry(self, placeholder_text="Enter image path to decode")
        self.decode_image_path_entry.grid(row=1, column=1, padx=20, pady=5)
        
        self.decode_button = ctk.CTkButton(self, text="Decode", command=self.decode_image)
        self.decode_button.grid(row=2, column=1, padx=20, pady=10)
        
        self.decode_result_label = ctk.CTkLabel(self, text="")
        self.decode_result_label.grid(row=3, column=1, padx=20, pady=5)

    def genData(self, data: str) -> List[str]:
        """
        Convert encoding data into 8-bit binary form using ASCII values of characters.
        
        Parameters:
            data (str): The message to be encoded.
            
        Returns:
            List[str]: A list of binary representations of each character in the message.
        """
        return [format(ord(i), '08b') for i in data]

    def modPix(self, pix: Iterator[Tuple[int, int, int]], data: str) -> Iterator[Tuple[int, int, int]]:
        """
        Modify pixels according to the 8-bit binary data of the message.
        
        Parameters:
            pix (Iterator[Tuple[int, int, int]]): An iterator of pixel tuples from the image.
            data (str): The message to be encoded.
            
        Yields:
            Iterator[Tuple[int, int, int]]: Modified pixels as tuples.
        """
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                                    imdata.__next__()[:3] +
                                    imdata.__next__()[:3]]
            
            for j in range(0, 8):
                if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                    pix[j] = pix[j] - 1 if pix[j] != 0 else pix[j] + 1

            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] = pix[-1] - 1 if pix[-1] != 0 else pix[-1] + 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg: Image.Image, data: str) -> None:
        """
        Encode the data into the image by modifying its pixels.
        
        Parameters:
            newimg (Image.Image): The image where data will be encoded.
            data (str): The message to be encoded.
        """
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def encode_image(self) -> None:
        """Handles the encoding process, saves the resulting image, and updates the GUI with a success message."""
        try:
            img_path = self.image_path_entry.get()
            message = self.message_entry.get()
            result_img_path = self.resulting_image_entry.get()

            image = Image.open(img_path, 'r')
            if len(message) == 0:
                raise ValueError("Message cannot be empty")

            new_img = image.copy()
            self.encode_enc(new_img, message)
            new_img.save(result_img_path)
            
            self.encode_result_label.configure(text="Message encoded successfully!")
        except Exception as e:
            self.encode_result_label.configure(text=f"Error: {e}")

    def decode_image(self) -> None:
        """Handles the decoding process and updates the GUI with the decoded message."""
        try:
            img_path = self.decode_image_path_entry.get()
            image = Image.open(img_path, 'r')
            decoded_message = self.decode_data(image)
            self.decode_result_label.configure(text=f"Decoded Message: {decoded_message}")
        except Exception as e:
            self.decode_result_label.configure(text=f"Error: {e}")

    def decode_data(self, image: Image.Image) -> str:
        """
        Decode a hidden message from an image file.
        
        Parameters:
            image (Image.Image): The image containing the hidden message.
        
        Returns:
            str: The decoded message from the image.
        """
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]
            
            binstr = ''.join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()
