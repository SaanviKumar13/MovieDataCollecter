from bs4 import BeautifulSoup
import requests
import pandas as pd

url = (
    "https://www.imdb.com/search/title/?sort=user_rating,asc&groups=top_1000&count=100"
)
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

page = BeautifulSoup(response.content, "html.parser")
names = []
release_date = []
content_rating = []
time = []
user_rating = []
vote_count = []
metascore = []
description = []

movies_info = page.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})

for movie in movies_info:
    names.append(movie.find("h3").text)

    release_date.append(
        movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[0].text
    )

    time.append(
        movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[1].text
    )

    content_rating.append(
        movie.find_all(
            "span", attrs={"class": "sc-b0691f29-8 ilsLEX dli-title-metadata-item"}
        )[2].text
    )

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
        user_rating.append(parts[0])
        vote_count.append(parts[1][1:-1])

    description.append(
        movie.find("div", attrs={"class": "ipc-html-content-inner-div"}).text
    )

    # metascore.append(
    #     movie.find("span", attrs={"class": "sc-b0901df4-0 bcQdDJ metacritic-score-box"})
    # )

movie_data = pd.DataFrame(
    {
        "Movie Name": names,
        "Year of release": release_date,
        "Time": time,
        "Stars": user_rating,
        "Rating": content_rating,
        "Votes": vote_count,
        "Description": description,
        # "Metascore": metascore,
    }
)

movie_data.to_excel("Movie_Data_IMDB.xlsx", index=False)
