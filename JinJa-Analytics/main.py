# import firebase_admin
# from firebase_admin import credentials, firestore
# import pandas as pd
# from collections import Counter
# from datetime import datetime
# import plotly.graph_objects as go
# import plotly.io as pio
# from jinja2 import Environment, FileSystemLoader

# # Initialize Firebase Admin
# cred = credentials.Certificate('curious.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# def fetch_data():
#     # Fetch posts
#     posts_ref = db.collection('posts')
#     posts = posts_ref.stream()
#     posts_data = [post.to_dict() for post in posts]

#     # Fetch events
#     events_ref = db.collection('events')
#     events = events_ref.stream()
#     events_data = [event.to_dict() for event in events]

#     # Fetch profiles
#     profiles_ref = db.collection('profile')
#     profiles = profiles_ref.stream()
#     profiles_data = [profile.to_dict() for profile in profiles]

#     return posts_data, events_data, profiles_data

# def preprocess_and_analyze(posts, events, profiles):
#     # Process posts data
#     post_df = pd.DataFrame(posts)
#     post_df['timestamp'] = pd.to_datetime(post_df['timestamp'], errors='coerce')
    
#     # Post Popularity
#     post_analysis = {
#         'post_titles': post_df['title'].tolist(),
#         'post_upvotes': post_df['upvote'].tolist(),
#         'hashtags_labels': post_df.explode('hashtags')['hashtags'].value_counts().index.tolist(),
#         'hashtags_values': post_df.explode('hashtags')['hashtags'].value_counts().tolist(),
#     }

#     # Process events data
#     event_df = pd.DataFrame(events)
#     event_status = event_df['status'].value_counts()
#     event_venues = event_df['venue'].value_counts()
#     time_slots = {
#         'Morning': sum(event_df['time'].apply(lambda t: datetime.strptime(t, '%H:%M:%S').hour < 12)),
#         'Afternoon': sum(event_df['time'].apply(lambda t: 12 <= datetime.strptime(t, '%H:%M:%S').hour < 17)),
#         'Evening': sum(event_df['time'].apply(lambda t: 17 <= datetime.strptime(t, '%H:%M:%S').hour < 21)),
#         'Night': sum(event_df['time'].apply(lambda t: datetime.strptime(t, '%H:%M:%S').hour >= 21)),
#     }
#     event_analysis = {
#         'status_labels': event_status.index.tolist(),
#         'status_values': event_status.tolist(),
#         'venue_labels': event_venues.index.tolist(),
#         'venue_values': event_venues.tolist(),
#         'time_slots_labels': list(time_slots.keys()),
#         'time_slots_values': list(time_slots.values()),
#     }

#     # Process profiles data
#     profile_df = pd.DataFrame(profiles)
#     college_counts = profile_df['college'].value_counts()
#     department_counts = profile_df['department'].value_counts()
#     position_counts = profile_df['position'].value_counts()
#     profile_analysis = {
#         'college_labels': college_counts.index.tolist(),
#         'college_values': college_counts.tolist(),
#         'department_labels': department_counts.index.tolist(),
#         'department_values': department_counts.tolist(),
#         'position_labels': position_counts.index.tolist(),
#         'position_values': position_counts.tolist(),
#     }

#     return post_analysis, event_analysis, profile_analysis

# def create_plotly_figure(data, chart_type='bar', title='', labels_key='labels', values_key='values'):
#     fig = go.Figure()
#     fig.add_trace(
#         go.Bar(
#             x=data[labels_key],
#             y=data[values_key],
#             marker_color='indianred'
#         )
#     )
#     fig.update_layout(
#         title=title,
#         xaxis_title='Categories',
#         yaxis_title='Values'
#     )
#     return pio.to_html(fig, full_html=False)

# # def render_template(post_data, event_data, profile_data):
# #     env = Environment(loader=FileSystemLoader('templates'))
# #     template = env.get_template('template.html')
# #     output = template.render(
# #         post_data=post_data,
# #         event_data=event_data,
# #         profile_data=profile_data
# #     )
# #     with open('output.html', 'w') as f:
# #         f.write(output)
# #     print("HTML file has been generated as 'output.html'")
# def render_template(post_data, event_data, profile_data):
#     env = Environment(loader=FileSystemLoader('templates'))
#     template = env.get_template('template.html')
#     output = template.render(
#         post_data=post_data,
#         event_data=event_data,
#         profile_data=profile_data
#     )
#     with open('output.html', 'w', encoding='utf-8') as f:
#         f.write(output)
#     print("HTML file has been generated as 'output.html'")


# def main():
#     posts, events, profiles = fetch_data()
#     post_analysis, event_analysis, profile_analysis = preprocess_and_analyze(posts, events, profiles)

#     # Generate Plotly charts
#     post_popularity_chart = create_plotly_figure(
#         post_analysis, 
#         title='Posts Popularity',
#         labels_key='post_titles',
#         values_key='post_upvotes'
#     )
#     hashtags_chart = create_plotly_figure(
#         post_analysis, 
#         title='Hashtag Frequency',
#         labels_key='hashtags_labels',
#         values_key='hashtags_values'
#     )
#     events_status_chart = create_plotly_figure(
#         event_analysis,
#         title='Events by Status',
#         labels_key='status_labels',
#         values_key='status_values'
#     )
#     events_venue_chart = create_plotly_figure(
#         event_analysis,
#         title='Events by Venue',
#         labels_key='venue_labels',
#         values_key='venue_values'
#     )
#     events_time_slots_chart = create_plotly_figure(
#         event_analysis,
#         title='Events by Time Slot',
#         labels_key='time_slots_labels',
#         values_key='time_slots_values'
#     )
#     profiles_college_chart = create_plotly_figure(
#         profile_analysis,
#         title='Profiles by College',
#         labels_key='college_labels',
#         values_key='college_values'
#     )
#     profiles_department_chart = create_plotly_figure(
#         profile_analysis,
#         title='Profiles by Department',
#         labels_key='department_labels',
#         values_key='department_values'
#     )
#     profiles_position_chart = create_plotly_figure(
#         profile_analysis,
#         title='Profiles by Position',
#         labels_key='position_labels',
#         values_key='position_values'
#     )

#     # Render the template
#     render_template(
#         post_data={
#             'post_popularity_chart': post_popularity_chart,
#             'hashtags_chart': hashtags_chart
#         },
#         event_data={
#             'events_status_chart': events_status_chart,
#             'events_venue_chart': events_venue_chart,
#             'events_time_slots_chart': events_time_slots_chart
#         },
#         profile_data={
#             'profiles_college_chart': profiles_college_chart,
#             'profiles_department_chart': profiles_department_chart,
#             'profiles_position_chart': profiles_position_chart
#         }
#     )

# if __name__ == '__main__':
#     main()
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from collections import Counter
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
from jinja2 import Environment, FileSystemLoader

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

    return posts_data, events_data, profiles_data

def preprocess_and_analyze(posts, events, profiles):
    # Process posts data
    post_df = pd.DataFrame(posts)
    post_df['timestamp'] = pd.to_datetime(post_df['timestamp'], errors='coerce')
    
    # Post Popularity (Top 5)
    top_posts = post_df.nlargest(5, 'upvote')
    post_analysis = {
        'post_titles': top_posts['title'].tolist(),
        'post_upvotes': top_posts['upvote'].tolist(),
        'hashtags_labels': post_df.explode('hashtags')['hashtags'].value_counts().index.tolist()[:5],
        'hashtags_values': post_df.explode('hashtags')['hashtags'].value_counts().tolist()[:5],
    }

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
    college_counts = profile_df['college'].value_counts()
    department_counts = profile_df['department'].value_counts()
    position_counts = profile_df['position'].value_counts()
    profile_analysis = {
        'college_labels': college_counts.index.tolist(),
        'college_values': college_counts.tolist(),
        'department_labels': department_counts.index.tolist(),
        'department_values': department_counts.tolist(),
        'position_labels': position_counts.index.tolist(),
        'position_values': position_counts.tolist(),
    }

    return post_analysis, event_analysis, profile_analysis

def create_plotly_figure(data, chart_type='bar', title='', labels_key='labels', values_key='values', colors=None):
    fig = go.Figure()
    if chart_type == 'bar':
        fig.add_trace(
            go.Bar(
                x=data[labels_key],
                y=data[values_key],
                marker_color=colors if colors else 'indianred'
            )
        )
    elif chart_type == 'pie':
        fig.add_trace(
            go.Pie(
                labels=data[labels_key],
                values=data[values_key],
                marker=dict(colors=colors) if colors else None
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title='Categories' if chart_type == 'bar' else '',
        yaxis_title='Values' if chart_type == 'bar' else ''
    )
    return pio.to_html(fig, full_html=False)

def render_template(post_data, event_data, profile_data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')
    output = template.render(
        post_data=post_data,
        event_data=event_data,
        profile_data=profile_data
    )
    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(output)
    print("HTML file has been generated as 'output.html'")

def main():
    posts, events, profiles = fetch_data()
    post_analysis, event_analysis, profile_analysis = preprocess_and_analyze(posts, events, profiles)

    # Generate Plotly charts
    post_popularity_chart = create_plotly_figure(
        post_analysis, 
        chart_type='bar',
        title='Top 5 Posts Popularity',
        labels_key='post_titles',
        values_key='post_upvotes',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    hashtags_chart = create_plotly_figure(
        post_analysis, 
        chart_type='pie',
        title='Top 5 Hashtags Frequency',
        labels_key='hashtags_labels',
        values_key='hashtags_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    events_status_chart = create_plotly_figure(
        event_analysis,
        chart_type='pie',
        title='Events by Status',
        labels_key='status_labels',
        values_key='status_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    events_venue_chart = create_plotly_figure(
        event_analysis,
        chart_type='bar',
        title='Events by Venue',
        labels_key='venue_labels',
        values_key='venue_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    events_time_slots_chart = create_plotly_figure(
        event_analysis,
        chart_type='pie',
        title='Events by Time Slot',
        labels_key='time_slots_labels',
        values_key='time_slots_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    profiles_college_chart = create_plotly_figure(
        profile_analysis,
        chart_type='bar',
        title='Profiles by College',
        labels_key='college_labels',
        values_key='college_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    profiles_department_chart = create_plotly_figure(
        profile_analysis,
        chart_type='bar',
        title='Profiles by Department',
        labels_key='department_labels',
        values_key='department_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    profiles_position_chart = create_plotly_figure(
        profile_analysis,
        chart_type='bar',
        title='Profiles by Position',
        labels_key='position_labels',
        values_key='position_values',
        colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )

    # Render the template
    render_template(
        post_data={
            'post_popularity_chart': post_popularity_chart,
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
        }
    )

if __name__ == '__main__':
    main()
