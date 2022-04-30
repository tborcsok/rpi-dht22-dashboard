from dotenv import load_dotenv
load_dotenv()
from webapp import app, server

if __name__=='__main__':
    app.run_server()
