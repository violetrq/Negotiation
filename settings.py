from os import environ
import os
from dotenv import load_dotenv

SESSION_CONFIGS = [
    dict(
        name='full_experiment',
        display_name="Full Experiment (Introduction+ Matrix +  Bargaining + Questionnaire)",
        num_demo_participants=4,
        app_sequence=['introduction','matrix',  'bargaining', 'questionnaire']
    ),
    dict(
        name='introduction',
        display_name="Introduction",
        num_demo_participants=2,
        app_sequence=['introduction']
    ),
    dict(
        name='experiment_AI',
        display_name="Experiment (Matrix +  Bargaining + Questionnaire)",
        num_demo_participants=4,
        app_sequence=['matrix', 'bargaining', 'questionnaire']
    ),
    dict(
        name='experiment',
        display_name="Experiment ( Matrix +  Bargaining + Questionnaire)",
        num_demo_participants=4,
        app_sequence=['matrix', 'bargaining', 'questionnaire']
    ),
    dict(
        name='matrix_game',
        display_name="Matrix Game Only",
        num_demo_participants=4,
        app_sequence=['matrix']
    ),
    dict(
        name='bargaining_with_ai',
        display_name="Bargaining with AI Assistance",
        num_demo_participants=4,
        app_sequence=['bargaining']
    ),
]

ROOMS = [
    dict(
        name='prolific',
        display_name='Prolific Study',
        wait_for_all_groups = False

),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '{{ 12345 }}'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# Add your OpenAI API key
# load .env 文件
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')