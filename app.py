"""Titik masuk: merakit aplikasi. Vercel mencari variabel 'app' di file ini."""
from web import buat_app

app = buat_app()

if __name__ == "__main__":
    app.run(debug=True)