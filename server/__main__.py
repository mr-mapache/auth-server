import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    from uvicorn import run
    from server.entrypoint import api, settings
    run(api, host=settings.api.host, port=settings.api.port, log_level='info')