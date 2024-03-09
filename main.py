from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = (
    "https://www.imdb.com/search/title/?sort=user_rating,asc&groups=top_1000&count=100"
)
USER_AGENT = "Mozilla/5.0"
COLUMNS = [
    "Movie Name",
    "Year of release",
    "Time",
    "Stars",
    "Rating",
    "Votes",
    "Description",
]


def get_movie_data(url):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    page = BeautifulSoup(response.content, "html.parser")
    movies_info = page.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})
    data = []
    for movie in movies_info:
        names = movie.find("h3").text

        release_date = movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[0].text

        duration = movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[1].text

        stars = movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[2].text

        vote_data = []

        vote_data.append(
            movie.find(
                "span",
                attrs={
                    "class": "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"
                },
            ).text
        )

        for item in vote_data:
            parts = item.split("\xa0")
            ratings = parts[0]
            votes = parts[1][1:-1]

            description = movie.find(
                "div", attrs={"class": "ipc-html-content-inner-div"}
            ).text

        data.append([names, release_date, duration, stars, ratings, votes, description])
    return data


def main():
    movie_data = get_movie_data(URL)
    movie_df = pd.DataFrame(movie_data, columns=COLUMNS)
    movie_df.to_excel("Movie_Data_IMDB.xlsx", index=False)


if __name__ == "__main__":
    main()
