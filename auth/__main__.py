if __name__ == '__main__':
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from uvicorn import run
    from auth import authjs
    from auth.controllers import transport
    
    transport.app.mount('/authjs', authjs.app, name='AuthJS')
    run(transport.app, host='0.0.0.0', port=8000)