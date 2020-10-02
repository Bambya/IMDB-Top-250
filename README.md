## IMDB-Top-250

Movie lists have always fascinated me. Popular movie lists (of movies they supposedly think are the best) range from mainstream audience lists like **IMDB**, to more arthouse and less mainstream lists like **Letterboxd**, the Critics' top 100 list by **Sight and Sound** and many more. In this project, I have written code in python to extract the IMDB top 250 movies of all time, ranked by users. 

**MongoDB** is used for storing the dataset in a .json format. This json file can be later converted to csv/excel or any different format according to one's needs. You will have to download and install MongoDB and also a GUI of your choice. (Robo 3T is a good option). Mongo Uri and website name https://www.imdb.com/chart/top/ are given in the cfg file.

#### Why get this list? What's the use of it?

We can periodically get this list, like for example every other month and then observe the changing trends. Since the rankings of the movies are always prone to changes, we can observe these variations for every movie on the list. For this we can use basic Machine Learning libraries like Pandas, Matplotlib, Numpy, Seaborn, etc. I have attached the dataset for the month of September 2020 in this repository. After getting the list for the coming months, I will analyse the data further.
Other analyses we can look into are:-
- Which directors' movies are mostly being preferred by the audience?
- Which years or decades have produced the most successful movies?
- How does the movie vote count vary with its ranking and release year?

I later plan to look into the other lists that I have mentioned above and then compare them.

#### Let's get Started

As mentioned above, install MongoDB and a GUI and then set the mongodb connection according to the uri. Download the files to your disk. Then run locally from your command line.

- Install dependencies

```
pip install -r requirements.txt
```                               

- Start the process

```
python imdb250.py
```
