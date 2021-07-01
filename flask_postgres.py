from app import app, db
from app.models import user,courses

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': user,'Courses':courses}

if __name__=="__main__":
    app.run(debug=True)


#Set the environment Variable Database_URL as 'postgresql://username:password@localhost:portnumber/database_name ,(If password contains @ replace by %40).