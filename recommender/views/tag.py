import json
import time
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from neo4j import GraphDatabase

# graphdb = GraphDatabase.driver(uri="bolt://localhost:11003", auth=("neo4j","1234"))
graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))

def tag(request):
    session = graphdb.session()
    query = "MATCH(m:Movie)-[r:isTaggedBy]->(u:User) RETURN u.ID AS id_user, m.ID AS id_movie, m.Title AS title, collect(r.Tag) AS tag ORDER BY id_user"
    nodes = session.run(query)
    data = json.dumps(nodes.data())
    data = json.loads(data)

    queryMovie = "MATCH(m:Movie) RETURN m.ID as id, m.Title as title"
    movies = session.run(queryMovie)
    movies = json.dumps(movies.data())
    movies = json.loads(movies)

    queryUser = "MATCH(u:User) RETURN u.ID as id"
    users = session.run(queryUser)
    users = json.dumps(users.data())
    users = json.loads(users)

    context ={
        'isTag' : True,
        'title':'Tag',
        'data':data,
        'movies':movies,
        'users':users
    }
    return render(request, 'recommender/tag/index.html', context)

def istagby_tag(request):
    timestamp = int(time.time())
    session = graphdb.session()
    query = """
    MATCH (u:User{ID:'"""+str(request.POST['user_id'])+"""'}), (m:Movie{ID:'"""+str(request.POST['movie_id'])+"""'})
    merge (u)<-[r:isTaggedBy {Tag:'"""+str(request.POST['tag'])+"""',TimeStamp:'"""+str(timestamp)+"""' }]-(m)
    """
    session.run(query)    
    return HttpResponseRedirect('/tag')

def ubah_tag(request):
    if request.POST['old_tag']==request.POST['tag']: 
        return HttpResponseRedirect('/recommender/tag')

    session = graphdb.session()
    query = """
    MATCH (m:Movie{ID:'"""+str(request.POST['movie_id'])+"""'})-[r:isTaggedBy {Tag:'"""+str(request.POST['old_tag'])+"""'}]->(u:User{ID:'"""+str(request.POST['user_id'])+"""'})
    SET r.Tag = '"""+str(request.POST['tag'])+"""'
    """
    session.run(query)  
    return HttpResponseRedirect('/recommender/tag')

def hapus_tag(request):
    session = graphdb.session()
    query = """
    MATCH (m:Movie{ID:'"""+str(request.POST['movie_id'])+"""'})-[r:isTaggedBy {Tag:'"""+str(request.POST['tag'])+"""'}]->(u:User{ID:'"""+str(request.POST['user_id'])+"""'})
    DELETE r
    """
    session.run(query)  
    return HttpResponseRedirect('/recommender/tag')