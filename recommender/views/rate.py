import json
import time
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from neo4j import GraphDatabase

# graphdb = GraphDatabase.driver(uri="bolt://localhost:11003", auth=("neo4j","1234"))
graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))

def rate(request):
    session = graphdb.session()
    query = """
    MATCH(m:Movie)<-[r:givesRating]-(u:User) 
    RETURN  m.ID AS id_movie,  m.Title AS title, AVG(r.Rating) AS avg, COUNT(u) AS tot  ORDER BY avg DESC
    """
    nodes = session.run(query)
    data = json.dumps(nodes.data())
    data = json.loads(data)

    queryMovie = """
     MATCH(m:Movie) RETURN m.ID as id, m.Title as title
    """
    movies = session.run(queryMovie)
    movies = json.dumps(movies.data())
    movies = json.loads(movies)

    context ={
        'isRate' : True,
        'title' : 'Rate',
        'data':data,
        'movies':movies
    }
    return render(request, 'recommender/rate/index.html', context)

def give_rate(request):
    timestamp = int(time.time())
    session = graphdb.session()
    query = """
    MATCH (u:User{ID:'"""+str(request.POST['user_id'])+"""'}), (m:Movie{ID:'"""+str(request.POST['movie_id'])+"""'})
    merge (u)-[r:givesRating {Rating:"""+request.POST['rating']+""",TimeStamp:'"""+str(timestamp)+"""' }]->(m)
    """
    session.run(query)
    return HttpResponseRedirect('/recommender/rate/')

def getuser_rate(request):
    session = graphdb.session()
    query = """
     MATCH(u:User), (m:Movie {ID:'"""+str(request.GET['id'])+"""'}) 
     WHERE NOT (u)-[:givesRating]->() OR NOT (u)-[:givesRating]->(m)
     return u
    """
    nodes = session.run(query)
    data = json.dumps(nodes.data())
    data = json.loads(data)

    data = {
        'data':data
    }
    return JsonResponse(data)