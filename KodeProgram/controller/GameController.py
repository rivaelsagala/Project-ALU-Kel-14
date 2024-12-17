from flask import render_template, request, redirect, url_for, jsonify, session
import os
from PIL import Image
import random
from werkzeug.utils import secure_filename

class GameController:
    UPLOAD_FOLDER = 'static/uploads'
    PIECES_FOLDER = 'static/pieces'
    PUZZLE_SIZE = 3  # untuk puzzle 3x3
    
    @staticmethod
    def index():
        return render_template('index.html')
    
    @staticmethod
    def home():
        return render_template('home.html')

    @staticmethod
    def process_image():
        if 'file' not in request.files:
            return redirect('/home')
            
        file = request.files['file']
        if file.filename == '':
            return redirect('/home')
        
        # Validasi apakah file adalah gambar
        if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            return jsonify({'error': 'File is not an image'}), 400
            
        os.makedirs(GameController.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(GameController.PIECES_FOLDER, exist_ok=True)

        filename = secure_filename(file.filename)
        filepath = os.path.join(GameController.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        img = Image.open(filepath)
        img = img.resize((300, 300))  # Ukuran gambar untuk puzzle

        # Proses untuk level 1 (3x3)
        pieces_level1 = []
        width_level1 = img.width // 3
        height_level1 = img.height // 3

        for i in range(3):
            for j in range(3):
                left = j * width_level1
                upper = i * height_level1
                right = left + width_level1
                lower = upper + height_level1
                
                piece = img.crop((left, upper, right, lower))
                piece_path = f'piece1_{i}_{j}.png'
                full_path = os.path.join(GameController.PIECES_FOLDER, piece_path)
                piece.save(full_path)
                pieces_level1.append((i * 3 + j, f'/static/pieces/{piece_path}'))

        random.shuffle(pieces_level1)
        session['puzzle_state'] = [piece[0] for piece in pieces_level1]
        session['piece_paths'] = [piece[1] for piece in pieces_level1]

        # Proses untuk level 2 (4x4)
        pieces_level2 = []
        width_level2 = img.width // 4
        height_level2 = img.height // 4

        for i in range(4):
            for j in range(4):
                left = j * width_level2
                upper = i * height_level2
                right = left + width_level2
                lower = upper + height_level2
                
                piece = img.crop((left, upper, right, lower))
                piece_path = f'piece2_{i}_{j}.png'
                full_path = os.path.join(GameController.PIECES_FOLDER, piece_path)
                piece.save(full_path)
                pieces_level2.append((i * 4 + j, f'/static/pieces/{piece_path}'))

        random.shuffle(pieces_level2)
        session['puzzle_state_level2'] = [piece[0] for piece in pieces_level2]
        session['piece_paths_level2'] = [piece[1] for piece in pieces_level2]
        
        return redirect(url_for('web.level'))

    @staticmethod
    def level():
        level1_completed = session.get('level1_completed', False)
        return render_template('level.html', level1_completed=level1_completed)
    
    # LEVEL 1
    @staticmethod
    def level1():
        piece_paths = session.get('piece_paths')
        if not piece_paths:
            return redirect(url_for('web.home'))
        return render_template('level1.html', pieces=piece_paths, size=GameController.PUZZLE_SIZE)

    @staticmethod
    def level1_complete():
        session['level1_completed'] = True
        return render_template('level1_complete.html')

    @staticmethod
    def check_puzzle_state1():
        if not request.is_json:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        pieces = request.json.get('pieces', None)
        if pieces is None:
            return jsonify({'error': 'No pieces data provided'}), 400
        
        current_state = []
        
        # Ekstrak nomor urutan dari path gambar
        for piece in pieces:
            try:
                parts = piece.split('/')[-1].replace('piece1_', '').replace('.png', '').split('_')
                if len(parts) == 2:
                    row, col = map(int, parts)
                    index = row * 3 + col
                    current_state.append(index)
                else:
                    return jsonify({'error': 'Invalid piece format'}), 400
            except (ValueError, IndexError) as e:
                return jsonify({'error': f'Invalid piece data format: {str(e)}'}), 400
        
        # Target state untuk puzzle 3x3
        target_state = list(range(9))

        def manhattan_distance(state):
            distance = 0
            size = 3
            for i in range(len(state)):
                current_row = i // size
                current_col = i % size
                target_pos = state[i]
                target_row = target_pos // size
                target_col = target_pos % size
                distance += abs(current_row - target_row) + abs(current_col - target_col)
            return distance

        if manhattan_distance(current_state) == 0:
            return jsonify({'solved': True})
        return jsonify({'solved': False})

    # LEVEL 2
    @staticmethod
    def level2():
        piece_paths = session.get('piece_paths_level2')
        if not piece_paths:
            return redirect(url_for('web.home'))
        return render_template('level2.html', pieces=piece_paths, size=4)

    @staticmethod
    def level2_complete():
        session['level2_completed'] = True
        return render_template('level2_complete.html')

    @staticmethod
    def check_puzzle_state2():
        if not request.is_json:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        pieces = request.json.get('pieces', None)
        if pieces is None:
            return jsonify({'error': 'No pieces data provided'}), 400
        
        current_state = []
        
        # Ekstrak nomor urutan dari path gambar
        for piece in pieces:
            try:
                parts = piece.split('/')[-1].replace('piece2_', '').replace('.png', '').split('_')
                if len(parts) == 2:
                    row, col = map(int, parts)
                    index = row * 4 + col
                    current_state.append(index)
                else:
                    return jsonify({'error': 'Invalid piece format'}), 400
            except (ValueError, IndexError) as e:
                return jsonify({'error': f'Invalid piece data format: {str(e)}'}), 400
        
        # Target state untuk puzzle 4x4
        target_state = list(range(16))

        def manhattan_distance(state):
            distance = 0
            size = 4
            for i in range(len(state)):
                current_row = i // size
                current_col = i % size
                target_pos = state[i]
                target_row = target_pos // size
                target_col = target_pos % size
                distance += abs(current_row - target_row) + abs(current_col - target_col)
            return distance

        if manhattan_distance(current_state) == 0:
            return jsonify({'solved': True})
        return jsonify({'solved': False})
