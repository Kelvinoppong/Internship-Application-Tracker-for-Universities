from app import create_app, db
from app.models import User, Application

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Application': Application}

if __name__ == '__main__':
    app.run(debug=True) 