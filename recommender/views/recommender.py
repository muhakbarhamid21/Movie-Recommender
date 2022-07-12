from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from neo4j import GraphDatabase

# graphdb = GraphDatabase.driver(uri="bolt://localhost:11003", auth=("neo4j","1234"))
graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))
session = graphdb.session()

def recommender_index(request):
    user = {}
    query = """
    MATCH (n:User) RETURN n.ID
    """
    hasil = session.run(query)
    for i in hasil:
        user[i.data()["n.ID"]] = {'jumRating':0, 'jumTag':0}

    query = """
    MATCH (u:User)-[r:givesRating]->(m:Movie)
    RETURN u.ID, COUNT(m) as jumRating
    """
    hasil = session.run(query)
    for i in hasil:
        user[i.data()["u.ID"]]['jumRating'] = i.data()["jumRating"]
    
    query = """
    MATCH (u:User)<-[r:isTaggedBy]-(m:Movie)
    RETURN u.ID, COUNT(m) as jumTag
    """
    hasil = session.run(query)
    for i in hasil:
        user[i.data()["u.ID"]]['jumTag'] = i.data()["jumTag"]


    context ={
        'isRecommendation' : True,
        'title':'Recommendation',
        'data':user,
    }
    return render(request,'recommender/rekomendasi/index.html',context)


def genre_favorit(request, id):
    genre = {'War':0, 'Crime':0, 'Action':0, 'Thriller':0, 'Mystery':0, 'Animation':0, 'IMAX':0, 'Adventure':0, 'Sci-Fi':0, 'Romance':0, 'Drama':0, 'Comedy':0}
    movie = []

    # Ambil movie distinct dari taggedBy
    query = """
    MATCH (u:User{ID:'"""+str(id)+"""'})<-[r:isTaggedBy]-(m:Movie)
    return DISTINCT m
    """
    hasil = session.run(query)
    for i in hasil:
        if i.data()['m'] not in movie:
            movie.append(i.data()['m'])

    # Ambil movie distinct dari givesRating
    query = """
    MATCH (u:User{ID:'"""+str(id)+"""'})-[r:givesRating]->(m:Movie)
    return DISTINCT m
    """
    hasil = session.run(query)
    for i in hasil:
        if i.data()['m'] not in movie:
            movie.append(i.data()['m'])

    # Hitung kemunculan genre di tiap movie yang didapat sebelumnya
    jum_genre = {}
    for i in genre:
        jum_genre[i] = 0
        for j in movie:
            temp = j['Genre'].split("|")
            if i in temp:
                jum_genre[i]+=1
    
    # Ambil genre yang paling banyak muncul
    maxi = max(jum_genre, key=jum_genre.get)

    # ambil movie favorit berdasarkan movie yang memiliki genre maxi dan memiliki rata-rata rating >=3
    favorit = {}
    query = """
    MATCH (u:User)-[r:givesRating]->(m:Movie)-[:hasGenre]->(g:Genre{name:'"""+maxi+"""'})
    RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg
    ORDER BY Avg DESC
    """
    hasil = session.run(query)
    for i in hasil:
        if i.data()['Avg'] >= 3:
            favorit[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3)}

    context ={
        'isRecommendation' : True,
        'title':'Genre Favorit',
        'data' : jum_genre,
        'movie': favorit,
        'genre': maxi,
    }
    return render(request,'recommender/rekomendasi/genre-favorit.html',context)


def rekomendasi_user_baru(request):
    data = {}
    query = """
    MATCH (u:User)-[r:givesRating]->(m:Movie)
    RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum
    ORDER BY Avg DESC
    """
    hasil = session.run(query)
    for i in hasil:
        data[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3), 'jumlah':i.data()["jum"]}
        print(data)
    
    context ={
        'isRecommendation' : True,
        'title':'Rekomendasi Movie',
        'data' : data,
    }
    return render(request,'recommender/rekomendasi/rekomendasi-user-baru.html',context)


def rekomendasi_0(request, id):
    rekomendasi = []
    query = """
    MATCH(u:User{ID:'"""+str(id)+"""'})<-[:isTaggedBy]-(s:Movie)-[:hasGenre]->(c:Genre)<-[:hasGenre]-(z:Movie)
    WHERE NOT EXISTS ((u)-[:isTaggedBy]->(z))
    WITH s, z
    MATCH (s)-[:hasGenre]->(sc:Genre)
    WITH s, z, COLLECT(DISTINCT id(sc)) AS s1, COLLECT(DISTINCT sc.name) AS g1
    MATCH (z)-[:hasGenre]->(zc:Genre)
    WITH s, z, s1, COLLECT(DISTINCT id(zc)) AS s2, g1, COLLECT(DISTINCT zc.name) AS g2
    WITH s, z, s1, s2, g1, g2
    RETURN s.Title as UserShow, z.Title as Recommendate, g1 as UserShowCategory, g2 as RecommendateShowCategory, gds.alpha.similarity.jaccard(s1,s2) AS jaccard ORDER BY jaccard DESC
    """
    hasil = session.run(query)
    for i in hasil: 
        rekomendasi.append({'UserShow':i.data()["UserShow"], 'Recommendate':i.data()["Recommendate"], 'UserShowCategory':i.data()["UserShowCategory"], 'RecommendateShowCategory':i.data()["RecommendateShowCategory"], 'jaccard':round(i.data()["jaccard"], 3),})

    context ={
        'isRecommendation' : True,
        'title':'Rekomendasi Movie',
        'data' : rekomendasi,
    }
    return render(request,'recommender/rekomendasi/rekomendasi-0.html',context)


def rekomendasi_1(request, id):
    movie_all = {}
    distinct = []
    rekomendasi_jaccard = []
    movie_1 = {}
    query = """
    MATCH(u:User{ID:'"""+str(id)+"""'})<-[:isTaggedBy]-(s:Movie)-[:hasGenre]->(c:Genre)<-[:hasGenre]-(z:Movie)
    WHERE NOT EXISTS ((u)-[:isTaggedBy]->(z))
    WITH s, z
    MATCH (s)-[:hasGenre]->(sc:Genre)
    WITH s, z, COLLECT(DISTINCT id(sc)) AS s1, COLLECT(DISTINCT sc.name) AS g1
    MATCH (z)-[:hasGenre]->(zc:Genre)
    WITH s, z, s1, COLLECT(DISTINCT id(zc)) AS s2, g1, COLLECT(DISTINCT zc.name) AS g2
    WITH s, z, s1, s2, g1, g2
    RETURN z.ID, z.Title, z.Genre, s.Title as UserShow, z.Title as Recommendate, g1 as UserShowCategory, g2 as RecommendateShowCategory, gds.alpha.similarity.jaccard(s1,s2) AS jaccard 
    ORDER BY jaccard DESC
    """
    hasil = session.run(query)
    for i in hasil: 
        if i.data()['Recommendate'] not in distinct:
            rekomendasi_jaccard.append({'UserShow':i.data()["UserShow"], 'Recommendate':i.data()["Recommendate"], 'UserShowCategory':i.data()["UserShowCategory"], 'RecommendateShowCategory':i.data()["RecommendateShowCategory"], 'jaccard':round(i.data()["jaccard"], 3),})
            distinct.append(i.data()['Recommendate'])
            movie_1[i.data()['z.ID']] = {'title':i.data()["z.Title"], 'genre':i.data()["z.Genre"], 'value':i.data()["jaccard"]}
            movie_all[i.data()['z.ID']] = {'title':i.data()["z.Title"], 'genre':i.data()["z.Genre"], 'value':i.data()["jaccard"]}


    user = []
    query = """
    MATCH (p1:User {ID:'"""+str(id)+"""'})-[x:givesRating]->(m:Movie)
    WITH p1, gds.alpha.similarity.asVector(m, x.Rating) AS p1avg
    MATCH (p2:User)-[y:givesRating]->(m:Movie) WHERE p2 <> p1
    WITH p1, p2, p1avg, gds.alpha.similarity.asVector(m, y.Rating) AS p2avg
    RETURN p1.ID AS SelectedUser,
    p2.ID AS SimilarUser,
    gds.alpha.similarity.pearson(p1avg, p2avg, {vectorType: "maps"}) AS pearson
    ORDER BY pearson DESC
    """
    nodes = session.run(query)
    for i,node in enumerate(nodes): 
        user.append({'SelectedUser': node.data()["SelectedUser"], 'SimilarUser': node.data()["SimilarUser"], 'pearson': node.data()["pearson"]})
        if i==0:
            similarUser = node.data()["SimilarUser"]
            
    movie_user = []
    query = """
    match (u:User{ID:'"""+str(id)+"""'})-[r:givesRating]->(m:Movie)
    return m, m.ID, m.Title, r.Rating
    order by r.Rating DESC
    """
    nodes = session.run(query)
    for node in nodes: 
        movie_user.append(node.data()["m"])

    movie_2 = {}
    query = """
    match (u:User{ID:'"""+str(similarUser)+"""'})-[r:givesRating]->(m:Movie)
    return m, m.ID, m.Title, m.Genre, r.Rating
    order by r.Rating DESC
    """
    nodes = session.run(query)
    for node in nodes: 
        if node.data()["m"] not in movie_user:
            movie_2[node.data()["m.ID"]] = {'title':node.data()["m.Title"], 'genre':node.data()["m.Genre"], 'value':node.data()["r.Rating"]}
            if node.data()["m.ID"] not in movie_all:
                movie_all[node.data()["m.ID"]] = {'title':node.data()["m.Title"], 'genre':node.data()["m.Genre"], 'value':node.data()["r.Rating"]}

    for i in movie_all:
        value_1 = 0
        value_2 = 0
        if i in movie_1:
            value_1 = movie_1[i]['value']*0.5
        if i in movie_2:
            value_2 = (movie_2[i]['value']-0)/5-0
            value_2 *= 0.5
        value = value_1 + value_2
        movie_all[i]['value'] = value

    context ={
        'isRecommendation' : True,
        'title':'Rekomendasi Movie',
        'rekomendasi_jaccard' : rekomendasi_jaccard,
        'rekomendasi_pearson' : movie_2,
        'rekomendasi_akhir' : movie_all
    }
    return render(request,'recommender/rekomendasi/rekomendasi-1.html',context)


def rekomendasi_2(request, id):
    user = []

    query = """
    MATCH (p1:User {ID:'"""+str(id)+"""'})-[x:givesRating]->(m:Movie)
    WITH p1, gds.alpha.similarity.asVector(m, x.Rating) AS p1avg
    MATCH (p2:User)-[y:givesRating]->(m:Movie) WHERE p2 <> p1
    WITH p1, p2, p1avg, gds.alpha.similarity.asVector(m, y.Rating) AS p2avg
    RETURN p1.ID AS SelectedUser,
    p2.ID AS SimilarUser,
    gds.alpha.similarity.pearson(p1avg, p2avg, {vectorType: "maps"}) AS pearson
    ORDER BY pearson DESC
    """
    nodes = session.run(query)
    for i,node in enumerate(nodes): 
        user.append({'SelectedUser': node.data()["SelectedUser"], 'SimilarUser': node.data()["SimilarUser"], 'pearson': node.data()["pearson"]})
        if i==0:
            similarUser = node.data()["SimilarUser"]

    movie_user = []
    query = """
    match (u:User{ID:'"""+str(id)+"""'})-[r:givesRating]->(m:Movie)
    return m, m.ID, m.Title, r.Rating
    order by r.Rating DESC
    """
    nodes = session.run(query)
    for node in nodes: 
        movie_user.append(node.data()["m"])

    movie_selected = {}
    query = """
    match (u:User{ID:'"""+str(similarUser)+"""'})-[r:givesRating]->(m:Movie)
    return m, m.ID, m.Title, m.Genre, r.Rating
    order by r.Rating DESC
    """
    nodes = session.run(query)
    for node in nodes: 
        if node.data()["m"] not in movie_user:
            movie_selected[node.data()["m.ID"]] = {'title':node.data()["m.Title"], 'genre':node.data()["m.Genre"], 'rating':node.data()["r.Rating"]}
            
    context ={
        'isRecommendation' : True,
        'title':'Rekomendasi Movie',
        'user' : user,
        'movie':movie_selected,
        'user_selected':similarUser,
    }
    return render(request,'recommender/rekomendasi/rekomendasi-2.html',context)


def tambah_user(request):
    query = """
    create (u:User{ID:'"""+str(request.POST['id'])+"""'}) return u
    """
    session.run(query)

    return HttpResponseRedirect('/recommender')


def ubah_user(request):
    query = """
    match (u:User{ID:'"""+str(request.POST['id_awal'])+"""'}) set u.ID = '"""+str(request.POST['id'])+"""'
    """
    session.run(query)

    return HttpResponseRedirect('/recommender')


def hapus_user(request):
    query = """
    MATCH (u:User{ID:'"""+str(request.POST['id'])+"""'})
    DETACH DELETE u
    """
    session.run(query)

    return HttpResponseRedirect('/recommender')
