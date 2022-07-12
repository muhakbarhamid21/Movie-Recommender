from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from neo4j import GraphDatabase

# graphdb = GraphDatabase.driver(uri="bolt://localhost:11003", auth=("neo4j","1234"))
graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))
session = graphdb.session()

def movie(request):
    movie = {}
    link = {}
    query = """
    MATCH (m:Movie)-[r:hasLink]->(l:Link)
    return m.ID, m.Title, m.Genre, l.IMDB_ID, l.TMDB_ID
    """
    nodes = session.run(query)
    for node in nodes: 
        movie[node.data()["m.ID"]] = {'title':node.data()["m.Title"], 'genre':node.data()["m.Genre"], 'imdb':node.data()["l.IMDB_ID"], 'tmdb':node.data()["l.TMDB_ID"]}
        if len(node.data()["l.IMDB_ID"]) != 7:
            movie[node.data()["m.ID"]]['link'] = '0'*(7-len(node.data()["l.IMDB_ID"])) + node.data()["l.IMDB_ID"]
        else:
            movie[node.data()["m.ID"]]['link'] = node.data()["l.IMDB_ID"]

    context ={
        'isMovie' : True,
        'title' : 'Movie',
        'movie' : movie,
        'link' : link,
    }
    return render(request, 'recommender/movie/index.html', context)


def tambah_movie(request):
    query = """
    CREATE(movie :Movie {ID:'"""+str(request.POST['id'])+"""',Title:'"""+str(request.POST['title'])+"""',Genre:'"""+str(request.POST['genre'])+"""'});
    """
    session.run(query)
    query = """
    CREATE(link :Link {IMDB_ID:'"""+str(request.POST['imdb'])+"""',TMDB_ID:'"""+str(request.POST['tmdb'])+"""'});
    """
    session.run(query)
    query = """
    MATCH (a:Movie{ID:'"""+str(request.POST['id'])+"""'}), (b:Link{IMDB_ID:'"""+str(request.POST['imdb'])+"""'}) merge (a)-[r:hasLink]->(b);
    """
    session.run(query)

    genre = request.POST['genre'].split('|')
    for i in genre:
        query = """
        MERGE(genre :Genre {name:'"""+i+"""'});
        """
        session.run(query)
        query = """
        MATCH (a:Movie{ID:'"""+str(request.POST['id'])+"""'}), (b:Genre{name:'"""+i+"""'}) merge (a)-[r:hasGenre]->(b);
        """
        session.run(query)

    return HttpResponseRedirect('/recommender/movie')


def ubah_movie(request):
    query = """
    MATCH (a:Movie{ID:'"""+str(request.POST['id_awal'])+"""'})-[r:hasLink]->(b:Link)
    SET a.ID = '"""+str(request.POST['id'])+"""',
    a.Title = '"""+str(request.POST['title'])+"""',
    a.Genre = '"""+str(request.POST['genre'])+"""',
    b.IMDB_ID = '"""+str(request.POST['imdb'])+"""',
    b.TMDB_ID = '"""+str(request.POST['tmdb'])+"""'
    """
    session.run(query)
    
    query = """
    MATCH (a:Movie{ID:'"""+str(request.POST['id'])+"""'})-[r:hasGenre]->(b:Genre)
    DELETE r
    """
    session.run(query)

    genre = request.POST['genre'].split('|')
    for i in genre:
        query = """
        MERGE(genre :Genre {name:'"""+i+"""'});
        """
        session.run(query)
        query = """
        MATCH (a:Movie{ID:'"""+str(request.POST['id'])+"""'}), (b:Genre{name:'"""+i+"""'}) merge (a)-[r:hasGenre]->(b);
        """
        session.run(query)

    return HttpResponseRedirect('/recommender/movie')


def hapus_movie(request):
    query = """
    MATCH (a:Movie{ID:'"""+str(request.POST['id'])+"""'})
    DETACH DELETE a
    """
    session.run(query)
    
    query = """
    MATCH (a:Link{IMDB_ID:'"""+str(request.POST['imdb'])+"""'})
    DETACH DELETE a
    """
    session.run(query)

    return HttpResponseRedirect('/recommender/movie')