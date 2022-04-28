#imports
from flask import (
    Flask,
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for,
    abort
)
from flask_sqlalchemy import SQLAlchemy
import sys

#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Magdalena150@localhost:5432/dbp20'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)


#models
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'Todo: id={self.id}, description={self.description}'


db.create_all()

#controller
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo_post():
    error = False
    response = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        response['description'] = description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(response)

@app.route('/todos/create_get', methods=['GET'])
def create_todo_get():
    try:
        description = request.args.get('description', '')
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    return redirect(url_for('index'))


#run
if __name__ == '__main__':
    app.run(debug=True, port=5000)