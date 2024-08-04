import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from collections import Counter
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
from jinja2 import Environment, FileSystemLoader
import plotly.express as px

# Initialize Firebase Admin
cred = credentials.Certificate('curious.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_data():
    # Fetch posts
    posts_ref = db.collection('posts')
    posts = posts_ref.stream()
    posts_data = [post.to_dict() for post in posts]

    # Fetch events
    events_ref = db.collection('events')
    events = events_ref.stream()
    events_data = [event.to_dict() for event in events]

    # Fetch profiles
    profiles_ref = db.collection('profile')
    profiles = profiles_ref.stream()
    profiles_data = [profile.to_dict() for profile in profiles]

    # Fetch users
    users_ref = db.collection('users')
    users = users_ref.stream()
    users_data = [user.to_dict() for user in users]

    return posts_data, events_data, profiles_data, users_data

def preprocess_and_analyze(posts, events, profiles, users):
    # Process posts data
    post_df = pd.DataFrame(posts)
    post_df['timestamp'] = pd.to_datetime(post_df['timestamp'], errors='coerce')
    
    # Post Popularity
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
        'dates': daily_user_counts.index.date,
        'user_counts': daily_user_counts.values
    }

    return post_analysis, event_analysis, profile_analysis, user_analysis


def create_plotly_figure(data, chart_type='bar', title='', labels_key='labels', values_key='values', color=None):
    fig = go.Figure()
    
    if chart_type == 'bar':
        # Use Plotly Express for better color handling
        fig = px.bar(
            x=data[labels_key],
            y=data[values_key],
            color=data[labels_key],  # Color bars based on labels
            color_discrete_sequence=px.colors.qualitative.Plotly  # Define a color scale
        )
    elif chart_type == 'pie':
        fig.add_trace(
            go.Pie(
                labels=data[labels_key],
                values=data[values_key],
                hole=0.3
            )
        )
    elif chart_type == 'line':
        fig.add_trace(
            go.Scatter(
                x=data['dates'],
                y=data['user_counts'],
                mode='lines+markers',
                marker=dict(color='royalblue')
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title='Categories' if chart_type != 'line' else 'Date',
        yaxis_title='Values'
    )
    return pio.to_html(fig, full_html=False)

def main():
    posts, events, profiles, users = fetch_data()
    post_analysis, event_analysis, profile_analysis, user_analysis = preprocess_and_analyze(posts, events, profiles, users)

    # Generate Plotly charts
    post_popularity_chart = create_plotly_figure(
        post_analysis, 
        title='Posts Popularity',
        labels_key='post_titles',
        values_key='post_upvotes'
    )
    top_5_posts_chart = create_plotly_figure(
        post_analysis, 
        title='Top 5 Popular Posts',
        labels_key='top_5_post_titles',
        values_key='top_5_post_upvotes'
    )
    hashtags_chart = create_plotly_figure(
        post_analysis, 
        chart_type='pie',
        title='Top 5 Hashtags Frequency',
        labels_key='hashtags_labels',
        values_key='hashtags_values'
    )
    events_status_chart = create_plotly_figure(
        event_analysis,
        title='Events by Status',
        labels_key='status_labels',
        values_key='status_values'
    )
    events_venue_chart = create_plotly_figure(
        event_analysis,
        title='Events by Venue',
        labels_key='venue_labels',
        values_key='venue_values'
    )
    events_time_slots_chart = create_plotly_figure(
        event_analysis,
        title='Events by Time Slot',
        labels_key='time_slots_labels',
        values_key='time_slots_values'
    )
    profiles_college_chart = create_plotly_figure(
        profile_analysis,
        title='Profiles by College',
        labels_key='college_labels',
        values_key='college_values'
    )
    profiles_department_chart = create_plotly_figure(
        profile_analysis,
        title='Profiles by Department',
        labels_key='department_labels',
        values_key='department_values'
    )
    profiles_position_chart = create_plotly_figure(
        profile_analysis,
        title='Profiles by Position',
        labels_key='position_labels',
        values_key='position_values'
    )
    users_chart = create_plotly_figure(
        user_analysis,
        chart_type='line',
        title='Daily User Registrations',
        color='royalblue'
    )

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

    # Render the template with data
    html_output = template.render(
        post_data={
            'post_popularity_chart': post_popularity_chart,
            'top_5_posts_chart': top_5_posts_chart,
            'hashtags_chart': hashtags_chart
        },
        event_data={
            'events_status_chart': events_status_chart,
            'events_venue_chart': events_venue_chart,
            'events_time_slots_chart': events_time_slots_chart
        },
        profile_data={
            'profiles_college_chart': profiles_college_chart,
            'profiles_department_chart': profiles_department_chart,
            'profiles_position_chart': profiles_position_chart
        },
        user_data={
            'users_chart': users_chart
        }
    )

    # Write output to HTML file with UTF-8 encoding
    with open('analytics.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

if __name__ == '__main__':
    main()
