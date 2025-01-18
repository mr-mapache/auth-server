import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    from uvicorn import run
    from authjs import api
    run(api, host='0.0.0.0', port=8000)