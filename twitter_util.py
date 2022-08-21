import tweepy
from tqdm import tqdm
from datetime import datetime
from translate import Translator

# set up api keys
CONSUMER_KEY = placeholder_key
CONSUMER_SECRET = placeholder_key
ACCESS_KEY = placeholder_key
ACCESS_SECRET = placeholder_key
BEARER_TOKEN = placeholder_key
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_KEY,
                       access_token_secret=ACCESS_SECRET)

language_dict = {'en', 'zh', 'hi', 'es', 'fr', 'ar', 'bn', 'ru'}

# translate text given the text, language of text and destination language
def translate_tweet(tweet, original_lang, target_lang):
    try:
        translator = Translator(from_lang=original_lang, to_lang=target_lang)
        translation = translator.translate(tweet)
        return translation
    except:
        print('Unable to translate')
        return tweet

# get the user's most recent tweets
# return a disctionary where key is the date and value is a list of tweets posted on that day
def get_tweets(username, num_tweets):
    all_tweets = {}
    try:
        uid = client.get_user(username=username).data.id
    except Exception as e:
        print('user not found')
        return None
    tweets = client.get_users_tweets(id=uid, tweet_fields=['created_at', 'lang'], max_results=num_tweets).data
    # return empty set if user has made no tweets
    if tweets is None:
        return {}
    for tweet in tweets:
        lang = tweet.lang
        if lang not in language_dict:
            lang = 'en'

        date = f"{tweet.created_at.year}-{tweet.created_at.month}-{tweet.created_at.day}"
        eng_tweet = translate_tweet(tweet.text, lang, 'en')
        if date in all_tweets:
            all_tweets[date].append(eng_tweet)
        else:
            all_tweets[date] = [eng_tweet]
    return all_tweets


# get all of a user's followers and their tweets
# return a disctionary where key is the username of the follower and value is the dictionary of tweets returned by the
# get tweets function
def get_followers_tweets(username, num_tweets, num_followers=5, progress=False):
    all_friends = {}
    uid = client.get_user(username=username).data.id
    followers = client.get_users_followers(id=uid, max_results=num_followers).data
    # return empty set if user has 0 followers
    if followers is None:
        return {}
    if progress is True:
        iterable = tqdm(followers)
    else:
        iterable = followers
    for follower in iterable:
        # print(follower.username)
        try:
            tweets = get_tweets(follower.username, num_tweets)
            all_friends[follower.username] = tweets
        except:
            continue

    return all_friends


def get_following_tweets(username, num_tweets, num_following=5, progress=False):
    all_friends = {}
    uid = client.get_user(username=username).data.id
    following = client.get_users_following(id=uid, max_results=num_following).data
    # return empty set if user has 0 followers
    if following is None:
        return {}
    if progress is True:
        iterable = tqdm(following)
    else:
        iterable = following
    for following in iterable:
        # print(follower.username)
        try:
            tweets = get_tweets(following.username, num_tweets)
            all_friends[following.username] = tweets
        except:
            continue

    return all_friends


def get_follow_metrics(username):
    public_metrics = client.get_user(username=username, user_fields='public_metrics').data.public_metrics
    return public_metrics['followers_count'], public_metrics['following_count']
# print(get_tweets('RoyZ1017', 5))
# print(get_followers_tweets('ESPN', 5))
# print(translate_tweet("bonjour! comment ca va?", 'fr', 'fr'))
# print(get_follow_metrics('ESPN'))
