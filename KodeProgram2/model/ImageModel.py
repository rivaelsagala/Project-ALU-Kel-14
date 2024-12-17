from PIL import Image
import os

class ImageModel:
    @staticmethod
    def split_image(image_path, rows, cols, output_folder):
        image = Image.open(image_path)
        width, height = image.size
        piece_width = width // cols
        piece_height = height // rows
        pieces = []
        
        for i in range(rows):
            for j in range(cols):
                box = (j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height)
                piece = image.crop(box)
                piece_filename = f"{i}_{j}.png"
                piece_path = os.path.join(output_folder, piece_filename)
                piece.save(piece_path)
                pieces.append(piece_filename)
        
        return pieces
