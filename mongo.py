from flask import Flask, Response,request,jsonify,make_response
from flask_mongoengine import MongoEngine
from decouple import config
import json

app=Flask(__name__)
password=config("password")
db_name="API"
DB_URI="mongodb+srv://admin:{}@flaskcon.3su2lne.mongodb.net/{}?retryWrites=true&w=majority".format(password,db_name)

db=MongoEngine()
db.connect(db=db_name,username="admin",password=config("password"),host=DB_URI)

class Movie(db.Document):
    movie_id=db.IntField()
    name=db.StringField()
    director=db.StringField()

    def to_json(self):
        return{
            "movie_id":self.movie_id,
            "name":self.name,
            "director":self.director
        }


@app.route('/movies/createMovie',methods=['POST'])
def createmovie():
    #To create Movie details
    movie1=Movie(movie_id=1,name="Imitation Game",director="Morten Tyldum")
    movie1.save()
    movie2=Movie(movie_id=2,name="Rush",director="Ron Howard")
    movie2.save()
    # Movie2.save()
    return Response("Saved")

@app.route('/movies',methods=['GET','POST'])
def movies_api():
    if request.method=="GET":
        movies=[]
        for movie in Movie.objects:
            movies.append(movie.to_json())
        return make_response(jsonify(movies),200)
    elif request.method=="POST":
        content=request.json
        print("Content",content)
        movie=Movie(movie_id=content['movie_id'],name=content['name'],director=content['director'])
        movie.save()
        return make_response(" ",201)

@app.route('/movies/<int:movie_id>',methods=['GET','PUT','DELETE'])
def read_update_delete_movie(movie_id):
    if request.method=="GET":
        #To view the movie according to its id
        movie_obj=Movie.objects(movie_id=movie_id).first()
        if movie_obj:
            return make_response(jsonify(movie_obj.to_json()),200)
        else:
            return make_response("Movie Not Found",404)
    elif request.method=="PUT":
        #Update
        content=request.json
        movie_obj=Movie.objects(movie_id=movie_id).first()
        movie_obj.update(director=content['director'],name=content['name'])
        return make_response("Movie Details Updated",201)
    elif request.method=="DELETE":
        #Delete
        content=request
        movie_obj=Movie.objects(movie_id=movie_id).first()
        movie_obj.delete()
        return make_response("Movie Deleted",201)



if __name__=="__main__":
    app.run(debug=True)