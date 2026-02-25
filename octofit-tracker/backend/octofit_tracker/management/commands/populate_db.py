from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create_user(**hero, password='password') for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero, password='password') for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Marvel', members=marvel_users)
        dc_team = Team.objects.create(name='DC', members=dc_users)

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(user=user, activity_type='Running', duration=30, calories=300, date=timezone.now().date())
            Activity.objects.create(user=user, activity_type='Cycling', duration=45, calories=400, date=timezone.now().date())

        # Create workouts
        for user in marvel_users + dc_users:
            Workout.objects.create(user=user, name='Morning Cardio', description='Cardio session', date=timezone.now().date())
            Workout.objects.create(user=user, name='Strength Training', description='Weights and resistance', date=timezone.now().date())

        # Create leaderboard
        Leaderboard.objects.create(team=marvel_team, score=1000)
        Leaderboard.objects.create(team=dc_team, score=950)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
