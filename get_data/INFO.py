

fieids_url = {
    "artists" : "http://y.saoju.net/yyj/api/artist/",
    "produces" : "http://y.saoju.net/yyj/api/produce/",
    "musicals":"http://y.saoju.net/yyj/api/musical/",
    "musicalproduces":"http://y.saoju.net/yyj/api/musicalproduces/",
    "citys" : "http://y.saoju.net/yyj/api/city/",
    "theatres":"http://y.saoju.net/yyj/api/theatre/", #这里的theatre要删掉location这个foreign key
    "stages":"http://y.saoju.net/yyj/api/stage/",
    "shows":"http://y.saoju.net/yyj/api/search_day/?date={}"
}

columns_needed = {
    "citys":["pk","fields.name"],
    "artists": ["pk","fields.name","fields.note"],
    "musicals":["pk",'fields.name', 'fields.is_original',
       'fields.progress', 'fields.premiere_date',
       'fields.info'],
    "produces":['pk', 'fields.name'],
    "musicalproduces":['pk', 'fields.title', 'fields.musical','fields.produce'],
    "theatres":['pk', 'fields.name','fields.city'],
    "stages":['pk', 'fields.name','fields.theatre', 'fields.seats'],

}

database_schema = """

    CREATE TABLE artists (
        artist_id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        note VARCHAR(30)
    );
    
    CREATE TABLE citys (
        city_id SERIAL PRIMARY KEY,
        city_name VARCHAR(20)
    );


    CREATE TABLE musicals (
        musical_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        is_original boolean,
        progress varchar(5),
        premiere_date date,
        info varchar(300)
    );
    CREATE TABLE produces (
        produce_id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    );
    CREATE TABLE musicalproduces (
        musicalproduce_id SERIAL PRIMARY KEY,
        title VARCHAR(20),
        musical_id INT REFERENCES musicals(musical_id),
        produce_id INT REFERENCES produces(produce_id)
        
    );
    CREATE TABLE theatres (
        theatre_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        city_id INT REFERENCES citys(city_id)
    );    
    CREATE TABLE stages (
        stage_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        theatre_id INT,
        seats INT
    ); 
    create table shows(
    show_id SERIAL PRIMARY KEY,
    date date,
    city varchar(10),
    musical varchar(50),
    "cast" varchar(100),
    theatre varchar(50)   
)
"""