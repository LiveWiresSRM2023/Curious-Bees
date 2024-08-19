import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from collections import Counter
from datetime import datetime
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate('curious.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_data():
    # Fetch posts
    posts_ref = db.collection('posts')
    posts = [post.to_dict() for post in posts_ref.stream()]

    # Fetch events
    events_ref = db.collection('events')
    events = [event.to_dict() for event in events_ref.stream()]

    # Fetch profiles
    profiles_ref = db.collection('profile')
    profiles = [profile.to_dict() for profile in profiles_ref.stream()]

    # Fetch users
    users_ref = db.collection('users')
    users = [user.to_dict() for user in users_ref.stream()]

    return posts, events, profiles, users

def preprocess_and_analyze(posts, events, profiles, users):
    # Process posts data
    post_df = pd.DataFrame(posts)
    post_df['timestamp'] = pd.to_datetime(post_df['timestamp'], errors='coerce')

    post_analysis = {
        'post_titles': post_df['title'].tolist(),
        'post_upvotes': post_df['upvote'].tolist(),
        'hashtags_labels': post_df.explode('hashtags')['hashtags'].value_counts().index.tolist(),
        'hashtags_values': post_df.explode('hashtags')['hashtags'].value_counts().tolist(),
    }
    top_5_posts = post_df.nlargest(5, 'upvote')
    post_analysis['top_5_post_titles'] = top_5_posts['title'].tolist()
    post_analysis['top_5_post_upvotes'] = top_5_posts['upvote'].tolist()

    # Process events data
    event_df = pd.DataFrame(events)
    event_status = event_df['status'].value_counts()
    event_venues = event_df['venue'].value_counts()
    time_slots = {
        'Morning': sum(event_df['time'].apply(lambda t: datetime.strptime(t, '%H:%M:%S').hour < 12)),
        'Afternoon': sum(event_df['time'].apply(lambda t: 12 <= datetime.strptime(t, '%H:%M:%S').hour < 17)),
        'Evening': sum(event_df['time'].apply(lambda t: 17 <= datetime.strptime(t, '%H:%M:%S').hour < 21)),
        'Night': sum(event_df['time'].apply(lambda t: datetime.strptime(t, '%H:%M:%S').hour >= 21)),
    }
    event_analysis = {
        'status_labels': event_status.index.tolist(),
        'status_values': event_status.tolist(),
        'venue_labels': event_venues.index.tolist(),
        'venue_values': event_venues.tolist(),
        'time_slots_labels': list(time_slots.keys()),
        'time_slots_values': list(time_slots.values()),
    }

    # Process profiles data
    profile_df = pd.DataFrame(profiles)
    profile_analysis = {
        'college_labels': [],
        'college_values': [],
        'department_labels': [],
        'department_values': [],
        'position_labels': [],
        'position_values': [],
    }
    if 'college' in profile_df.columns:
        college_counts = profile_df['college'].value_counts()
        profile_analysis['college_labels'] = college_counts.index.tolist()
        profile_analysis['college_values'] = college_counts.tolist()
    if 'department' in profile_df.columns:
        department_counts = profile_df['department'].value_counts()
        profile_analysis['department_labels'] = department_counts.index.tolist()
        profile_analysis['department_values'] = department_counts.tolist()
    if 'position' in profile_df.columns:
        position_counts = profile_df['position'].value_counts()
        profile_analysis['position_labels'] = position_counts.index.tolist()
        profile_analysis['position_values'] = position_counts.tolist()

    # Process users data
    user_df = pd.DataFrame(users)
    user_df['timestamp'] = pd.to_datetime(user_df['timestamp'], format='%B %d, %Y at %I:%M:%S %p UTC%z')
    user_df.set_index('timestamp', inplace=True)
    daily_user_counts = user_df.resample('D').size()
    user_analysis = {
        'dates': daily_user_counts.index.date.tolist(),
        'user_counts': daily_user_counts.values.tolist()
    }

    return post_analysis, event_analysis, profile_analysis, user_analysis

def save_to_json(post_analysis, event_analysis, profile_analysis, user_analysis, output_file='analysis_results.json'):
    results = {
        'post_analysis': post_analysis,
        'event_analysis': event_analysis,
        'profile_analysis': profile_analysis,
        'user_analysis': user_analysis
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    posts, events, profiles, users = fetch_data()
    post_analysis, event_analysis, profile_analysis, user_analysis = preprocess_and_analyze(posts, events, profiles, users)
    save_to_json(post_analysis, event_analysis, profile_analysis, user_analysis)
