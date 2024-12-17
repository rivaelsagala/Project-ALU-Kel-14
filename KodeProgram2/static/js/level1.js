// level1.js

const puzzleContainer = document.getElementById('puzzle');
const shuffleButton = document.getElementById('shuffleButton');
const checkButton = document.getElementById('checkButton');
const resetButton = document.getElementById('resetButton');

let pieces = [];
let moveCount = 0;

// Membagi gambar menjadi 16 bagian (4x4)
function splitImage(imageSrc) {
    pieces = [];
    puzzleContainer.innerHTML = ''; // Bersihkan kontainer
    const rows = 4, cols = 4;
    const img = new Image();
    img.src = imageSrc;

    img.onload = () => {
        const pieceWidth = img.width / cols;
        const pieceHeight = img.height / rows;
        
        for (let y = 0; y < rows; y++) {
            for (let x = 0; x < cols; x++) {
                const canvas = document.createElement('canvas');
                canvas.width = pieceWidth;
                canvas.height = pieceHeight;
                const context = canvas.getContext('2d');
                context.drawImage(
                    img,
                    x * pieceWidth, y * pieceHeight,
                    pieceWidth, pieceHeight,
                    0, 0,
                    pieceWidth, pieceHeight
                );
                const piece = canvas.toDataURL();
                pieces.push({ piece, x, y });
            }
        }
        shufflePieces();
    };
}

// Mengacak posisi potongan gambar
function shufflePieces() {
    moveCount = 0;
    updateMoveCount();
    pieces = pieces.sort(() => Math.random() - 0.5);
    displayPieces();
}

// Menampilkan potongan gambar di kontainer puzzle
function displayPieces() {
    puzzleContainer.innerHTML = '';
    pieces.forEach((item, index) => {
        const img = document.createElement('img');
        img.src = item.piece;
        img.classList.add('puzzle-piece');
        img.dataset.index = index;
        img.onclick = () => handlePieceClick(index);
        puzzleContainer.appendChild(img);
    });
}

// Menghitung langkah
function updateMoveCount() {
    document.getElementById('moveCount').textContent = moveCount;
}

// Fungsi untuk menangani klik pada potongan gambar
function handlePieceClick(index) {
    moveCount++;
    updateMoveCount();
    // Logika pergerakan dan pengecekan kemenangan dapat ditambahkan di sini
}

// Periksa apakah puzzle telah selesai
function checkSolution() {
    // Periksa urutan potongan, implementasikan sesuai kebutuhan
    alert("Check solution functionality is not implemented yet.");
}

// Reset puzzle
function resetPuzzle() {
    splitImage('/static/uploads/ikan.jpg');
}

shuffleButton.addEventListener('click', shufflePieces);
checkButton.addEventListener('click', checkSolution);
resetButton.addEventListener('click', resetPuzzle);

// Muat gambar dan pecah menjadi bagian-bagian saat halaman dimuat
splitImage('/static/uploads/ikan.jpg');
