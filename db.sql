create database coen281;

create table coen281.tweets (
    tweet_id bigint PRIMARY KEY,
    author_id bigint,
    tweet_text varchar(300)
                            )