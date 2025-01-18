import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    from auth.controllers.api import api
    from auth.controllers.cqs import router
    