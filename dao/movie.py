from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self, data_filter):
        movies = self.session.query(Movie)

        director_id = data_filter.get('director_id')

        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)

        genre_id = data_filter.get('genre_id')
        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)

        year = data_filter.get('year')
        if year is not None:
            movies = movies.filter(Movie.year == year)

        return movies.all()

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
