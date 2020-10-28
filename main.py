#!/ur/bin/env python3

from app import app

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="192.168.1.10", port=8000)
