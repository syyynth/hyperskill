from django.core.management.base import BaseCommand

from tube.models import Tag, Video, VideoTag


class Command(BaseCommand):
    help = 'videos helper'

    def handle(self, *args, **options):
        video_files = ['nature_walk.mp4', 'city_tour.mp4', 'cooking_tutorial.mp4', 'yoga_session.mp4',
                       'coding_lesson.mp4', 'music_concert.mp4', 'art_exhibition.mp4', 'wildlife_documentary.mp4',
                       'sports_match.mp4', 'science_lecture.mp4', 'travel_vlog.mp4', 'mountain_hike.mp4',
                       'beach_trip.mp4', 'baking_bread.mp4', 'meditation_guide.mp4', 'math_tutorial.mp4',
                       'orchestra_performance.mp4', 'sculpture_tour.mp4', 'ocean_documentary.mp4',
                       'basketball_game.mp4', 'physics_lecture.mp4']
        video_titles = ['Nature Walk', 'City Tour', 'Cooking Tutorial', 'Yoga Session', 'Coding Lesson',
                        'Music Concert', 'Art Exhibition', 'Wildlife Documentary', 'Sports Match', 'Science Lecture',
                        'Travel Vlog', 'Mountain Hike', 'Beach Trip', 'Baking Bread', 'Meditation Guide',
                        'Math Tutorial', 'Orchestra Performance', 'Sculpture Tour', 'Ocean Documentary',
                        'Basketball Game', 'Physics Lecture']

        tag_names = ['Nature', 'Travel', 'Cooking', 'Fitness', 'Education', 'Music', 'Art', 'Wildlife', 'Sports',
                     'Science', 'Travel', 'Nature', 'Nature', 'Cooking', 'Fitness', 'Education', 'Music', 'Art',
                     'Wildlife', 'Sports', 'Education']

        videos = [Video(file=file, title=title) for file, title in zip(video_files, video_titles)]
        tags = [Tag(name=name) for name in tag_names]
        video_tags = [VideoTag(video=video, tag=tag) for video, tag in zip(videos, tags)]

        Video.objects.bulk_create(videos)
        Tag.objects.bulk_create(tags)
        VideoTag.objects.bulk_create(video_tags)
