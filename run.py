import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__))) #intuk inisialisasi jika app tidak ditemukan pada docker

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
