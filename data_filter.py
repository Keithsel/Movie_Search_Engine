# -*- coding: utf-8 -*-
"""Data_filter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LY8-W3PnmOxT4DAYLGvWASqWxHtQjCZY
"""
import sys

sys.path.insert(1, '/home/chunporo/Documents/GitHub/Movie_Search_Engine/data')
import dataProcessing
import pandas as pd
import json
import time


def extract_tags(input_string):
    tags = []

    words = input_string.split()

    for word in words:
        if word.startswith('+'):
            tags.append(word[1:])

    return tags


def extract_keyword(input):
    if "+" not in input:
        return input
    else:
        tag_start = input.find("+")
        return input[:tag_start].strip()


def title_search(dataframe, keyword):
    filtered_df = dataframe[dataframe['title'].str.contains(keyword, case=False, na=False)]
    return filtered_df


def tag_search(dataframe, tags, genres_tags, language_tags, production_countries_tags, production_companies_tags,
               collection_tags):
    if len(tags) == 0:
        return dataframe
    for tag in tags:
        tag = tag.lower()
        if tag == "+adult":
            dataframe = dataframe[dataframe['adult'].str.contains("FALSE", case=False, na=False)]
        elif tag in genres_tags:
            dataframe = dataframe[dataframe['genres'].str.contains(tag, case=False, na=False)]
        elif tag in language_tags:
            dataframe = dataframe[dataframe['original_language'].str.contains(tag, case=False, na=False)]
        elif tag in production_countries_tags:
            dataframe = dataframe[dataframe['production_countries'].str.contains(tag, case=False, na=False)]
        elif tag in production_companies_tags:
            dataframe = dataframe[dataframe['production_companies'].str.contains(tag, case=False, na=False)]
        elif tag in collection_tags:
            dataframe = dataframe[dataframe['belongs_to_collection'].str.contains(tag, case=False, na=False)]
        else:
            return pd.DataFrame()
    return dataframe


def DataFilter(User_input):
    data_movie_path = '/home/chunporo/Documents/GitHub/Movie_Search_Engine/data/movies_metadata.csv'
    # df = dataProcessing.preprocess_movie_data(data_movie_path)
    df = pd.read_csv(data_movie_path)
    genres_tags = dataProcessing.unique_genres
    language_tags = dataProcessing.unique_language
    production_companies_tags = dataProcessing.unique_production_companies
    production_countries_tags = dataProcessing.unique_production_countries
    collection_tags = dataProcessing.unique_collection
    print(genres_tags)
    keyword = extract_keyword(User_input)
    tags = extract_tags(User_input)
    Movie_list = title_search(df, keyword)
    # print(df.genres.values[0])
    Movie_list = tag_search(Movie_list, tags, genres_tags, language_tags, production_countries_tags, production_companies_tags,
                            collection_tags)
    return Movie_list


start_time = time.time()
result = DataFilter("batman +adventure +animation")
print(result.title)
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
