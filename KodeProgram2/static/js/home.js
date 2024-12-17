// Menampilkan alert saat halaman dimuat
window.onload = function () {
  document.getElementById("alertMessage").style.display = "block";
};

// Fungsi untuk menyembunyikan alert
function hideAlert() {
  document.getElementById("alertMessage").style.display = "none";
}
