from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import time, re
from neo4j import GraphDatabase

graphdb = GraphDatabase.driver(uri="bolt://localhost:11003", auth=("neo4j","1234"))
# graphdb = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))
session = graphdb.session()

def index(request):
    if 'id_user' in request.session:
        id = request.session['id_user']

        query = """
        OPTIONAL MATCH (u:User{ID:'"""+str(id)+"""'})-[r:givesRating]->(m:Movie)
        WITH COUNT(m) as jumRating
        OPTIONAL MATCH (u2:User{ID:'"""+str(id)+"""'})<-[r2:isTaggedBy]-(m2:Movie)
        RETURN jumRating, COUNT(m2) as jumTag
        """
        hasil = session.run(query)
        for i in hasil:
            jum_rating = i.data()["jumRating"]
            jum_tag = i.data()["jumTag"]

        # movie by recommendation
        if jum_tag==0 and jum_rating==0:
            movie_rekomendasi = False
        elif jum_tag>0 and jum_rating==0:
            movie_rekomendasi = rekomendasi_0(id)
        elif jum_rating==1:
            movie_rekomendasi = rekomendasi_1(id)
        elif jum_rating>1:
            movie_rekomendasi = rekomendasi_2(id)

        # movie recommendation by genre fav
        if jum_tag==0 and jum_rating==0:
            movie_genre = False
        else:
            movie_genre = genre_favorite(id)

    else:
        movie_genre = False
        movie_rekomendasi = False

    # top rated movies
    movie_top = top_rated()

    context ={
        'movie_top' : movie_top,
        'movie_genre' : movie_genre,
        'movie_rekomendasi' : movie_rekomendasi,
    }
    return render(request, 'index.html', context)

def top_rated():
    data = {}
    query = """
    MATCH (u:User)-[r:givesRating]->(m:Movie)-[:hasLink]->(l:Link)
    RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum, l.IMDB_ID, l.TMDB_ID
    ORDER BY Avg DESC
    LIMIT 10
    """
    hasil = session.run(query)
    for i in hasil:
        data[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3), 'jumlah':i.data()["jum"], 'tmdb':i.data()["l.TMDB_ID"],}
        if len(i.data()["l.IMDB_ID"]) != 7:
            data[i.data()["m.ID"]]['imdb'] = '0'*(7-len(i.data()["l.IMDB_ID"])) + i.data()["l.IMDB_ID"]
        else:
            data[i.data()["m.ID"]]['imdb'] = i.data()["l.IMDB_ID"]
    
    return data

def genre_favorite(id):
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
    WITH m, AVG(r.Rating) AS Avg, COUNT(m) as jum
    MATCH (m:Movie)-[r:hasLink]->(l:Link)
    RETURN m.ID, m.Title, m.Genre, Avg, jum, l.IMDB_ID, l.TMDB_ID
    ORDER BY Avg DESC
    LIMIT 10
    """
    hasil = session.run(query)
    for i in hasil:
        if i.data()['Avg'] >= 3:
            favorit[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3), 'jumlah':i.data()["jum"], 'tmdb':i.data()["l.TMDB_ID"]}
            if len(i.data()["l.IMDB_ID"]) != 7:
                favorit[i.data()["m.ID"]]['imdb'] = '0'*(7-len(i.data()["l.IMDB_ID"])) + i.data()["l.IMDB_ID"]
            else:
                favorit[i.data()["m.ID"]]['imdb'] = i.data()["l.IMDB_ID"]
    
    return favorit

def rekomendasi_0(id):
    rekomendasi = []
    movie = {}
    limit = 0
    query = """
    MATCH(u:User{ID:'"""+str(id)+"""'})<-[:isTaggedBy]-(s:Movie)-[:hasGenre]->(c:Genre)<-[:hasGenre]-(z:Movie)
    WHERE NOT EXISTS ((u)-[:isTaggedBy]->(z))
    WITH s, z
    MATCH (s)-[:hasGenre]->(sc:Genre)
    WITH s, z, COLLECT(DISTINCT id(sc)) AS s1, COLLECT(DISTINCT sc.name) AS g1
    MATCH (z)-[:hasGenre]->(zc:Genre)
    WITH s, z, s1, COLLECT(DISTINCT id(zc)) AS s2, g1, COLLECT(DISTINCT zc.name) AS g2
    WITH z.ID as Recommendate, gds.alpha.similarity.jaccard(s1,s2) AS jaccard 
    RETURN Recommendate
    ORDER BY jaccard DESC
    """
    hasil = session.run(query)
    for i in hasil: 
        if i.data()["Recommendate"] not in rekomendasi and limit<10:
            query = """
            MATCH (u:User)-[r:givesRating]->(m:Movie{ID:'"""+str(i.data()["Recommendate"])+"""'})-[:hasLink]->(l:Link)
            RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum, l.IMDB_ID, l.TMDB_ID
            """
            result = session.run(query)
            for j in result:
                movie[j.data()["m.ID"]] = {'title':j.data()["m.Title"], 'genre':j.data()["m.Genre"], 'avg':round(j.data()["Avg"], 3), 'jumlah':j.data()["jum"], 'tmdb':j.data()["l.TMDB_ID"],}
                if len(j.data()["l.IMDB_ID"]) != 7:
                    movie[j.data()["m.ID"]]['imdb'] = '0'*(7-len(j.data()["l.IMDB_ID"])) + j.data()["l.IMDB_ID"]
                else:
                    movie[j.data()["m.ID"]]['imdb'] = j.data()["l.IMDB_ID"]

            rekomendasi.append(i.data()["Recommendate"])
            limit+=1
    
    return movie

def rekomendasi_1(id):
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
    

    movie_recommendation = {}
    limit = 0
    for i in movie_all:
        if limit<10:
            query = """
            MATCH (u:User)-[r:givesRating]->(m:Movie{ID:'"""+str(i)+"""'})-[:hasLink]->(l:Link)
            RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum, l.IMDB_ID, l.TMDB_ID
            """
            result = session.run(query)
            for j in result:
                movie_recommendation[i] = {'title':j.data()["m.Title"], 'genre':j.data()["m.Genre"], 'avg':round(j.data()["Avg"], 3), 'jumlah':j.data()["jum"], 'tmdb':j.data()["l.TMDB_ID"],}
                if len(j.data()["l.IMDB_ID"]) != 7:
                    movie_recommendation[i]['imdb'] = '0'*(7-len(j.data()["l.IMDB_ID"])) + j.data()["l.IMDB_ID"]
                else:
                    movie_recommendation[i]['imdb'] = j.data()["l.IMDB_ID"]
            limit+=1

    return movie_recommendation

def rekomendasi_2(id):
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
    match (u:User{ID:'"""+str(similarUser)+"""'})-[r:givesRating]->(m:Movie)-[:hasLink]->(l:Link)
    RETURN m, m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum, l.IMDB_ID, l.TMDB_ID, r.Rating
    order by r.Rating DESC
    LIMIT 10
    """
    hasil = session.run(query)
    for i in hasil:
        if i.data()["m"] not in movie_user:
            movie_selected[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3), 'jumlah':i.data()["jum"], 'tmdb':i.data()["l.TMDB_ID"]}
            if len(i.data()["l.IMDB_ID"]) != 7:
                movie_selected[i.data()["m.ID"]]['imdb'] = '0'*(7-len(i.data()["l.IMDB_ID"])) + i.data()["l.IMDB_ID"]
            else:
                movie_selected[i.data()["m.ID"]]['imdb'] = i.data()["l.IMDB_ID"]
    nodes = session.run(query)
            
    return movie_selected

def user_add_tag(request):
    if 'id_user' not in request.session:
        return redirect('login')
    else:
        id = request.session['id_user']
        
        timestamp = int(time.time())
        query = """
        MATCH (u:User{ID:'"""+str(id)+"""'}), (m:Movie{ID:'"""+str(request.POST['id_movie'])+"""'})
        merge (u)<-[r:isTaggedBy {Tag:'"""+str(request.POST['tag'])+"""',TimeStamp:'"""+str(timestamp)+"""' }]-(m)
        """
        session.run(query)
        return redirect('home')

def user_add_rate(request):
    if 'id_user' not in request.session:
        return redirect('login')
    else:
        id = request.session['id_user']
        
        timestamp = int(time.time())
        query = """
        MATCH (u:User{ID:'"""+str(id)+"""'})-[r:givesRating]->(m:Movie{ID:'"""+str(request.POST['id_movie'])+"""'}) 
        set r.Rating="""+str(request.POST['rating'])+""", r.TimeStamp='"""+str(timestamp)+"""'
        return count(r) as jum
        """
        hasil = session.run(query)

        if hasil.single()['jum'] == 0:
            query = """
            MATCH (u:User{ID:'"""+str(id)+"""'}), (m:Movie{ID:'"""+str(request.POST['id_movie'])+"""'})
            merge (u)-[r:givesRating {Rating:toFloat("""+request.POST['rating']+"""),TimeStamp:'"""+str(timestamp)+"""' }]->(m)
            """
            session.run(query)
        return redirect('home')

def search(request):
    if request.method == "POST":
        data = {}
        query = """
        match (m:Movie)-[:hasGenre]->(g:Genre),
        (u:User)-[r:givesRating]->(m:Movie)-[:hasLink]->(l:Link)
        where m.Title=~ '(?i).*"""+str(request.POST['query'])+""".*' or g.name =~ '(?i).*"""+str(request.POST['query'])+""".*'
        RETURN m.ID, m.Title, m.Genre, AVG(r.Rating) AS Avg, COUNT(m) as jum, l.IMDB_ID, l.TMDB_ID
        ORDER BY Avg DESC
        """
        hasil = session.run(query)
        for i in hasil:
            data[i.data()["m.ID"]] = {'title':i.data()["m.Title"], 'genre':i.data()["m.Genre"], 'avg':round(i.data()["Avg"], 3), 'jumlah':i.data()["jum"], 'tmdb':i.data()["l.TMDB_ID"],}
            if len(i.data()["l.IMDB_ID"]) != 7:
                data[i.data()["m.ID"]]['imdb'] = '0'*(7-len(i.data()["l.IMDB_ID"])) + i.data()["l.IMDB_ID"]
            else:
                data[i.data()["m.ID"]]['imdb'] = i.data()["l.IMDB_ID"]

        print(data)
        context ={
            'data' : data,
            'query' : request.POST['query'],
        }
        return render(request, 'search.html', context)

def register(request):
    if request.method == "POST":
        # print(request.POST['id_user'])
        # print(request.POST['password'])
        # print(request.POST['confirm_password'])
        if re.search('[a-zA-Z]', request.POST['id_user']) or request.POST['password'] != request.POST['confirm_password']:
            return redirect('register')
        else:
            query = """
            MATCH (u:User{ID:'"""+str(request.POST['id_user'])+"""'})
            return count(u) as jum
            """
            hasil = session.run(query)
            
            if hasil.single()['jum'] != 0:
                return redirect('register')
            else:
                query = """
                CREATE (u:User{ID:'"""+str(request.POST['id_user'])+"""', password:'"""+str(request.POST['password'])+"""', role:'user'})
                """
                session.run(query)
                return redirect('login')

    return render(request, 'register.html')

def login(request):
    if 'id_user' in request.session:
        del request.session['id_user']

    if request.method == "POST":
        query = """
        MATCH (u:User{ID:'"""+str(request.POST['id_user'])+"""', password:'"""+str(request.POST['password'])+"""'})
        return count(u) as jum, u.role as role
        """
        hasil = session.run(query)
        for i in hasil: 
            jum = i.data()['jum']
            role = i.data()['role']

        if jum == 1:
            request.session['id_user'] = request.POST['id_user']
            if role == 'user':
                return redirect('home')
            else:
                return redirect('recommender:recommender_index')
        else:
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    del request.session['id_user']
    return redirect('home')