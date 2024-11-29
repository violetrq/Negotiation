from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['role'] = p.participant.vars.get('role')

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    participant_role = models.StringField()  # Changed from 'role' to 'participant_role'

    def role(self):
        return self.participant.vars.get('role')

    def is_worker(self):
        return self.participant.vars.get('role') == 'Worker'

    def is_recruiter(self):
        return self.participant.vars.get('role') == 'Recruiter'



    age = models.IntegerField(
        label='Please enter your age.',
        min=18, max=120
    )
    gender = models.StringField(
        label='Please select your gender.',
        choices=[
            'Male', 'Female', 'Other', 'Prefer not to say'
        ]
    )
    education = models.StringField(
        label='What is the highest level of education you have completed?',
        choices=[
            'High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Other'
        ]
    )
    experience = models.IntegerField(
        label='How many years of work experience do you have?',
        min=0, max=60
    )
    race = models.StringField(
        label='Please select your race/ethnicity.',
        choices=[
            'Asian or Pacific Islander', 'Black or African American', 'Hispanic or Latino',
            'Native American or Alaskan Native', 'White or Caucasian', 'Multiracial or Biracial',
            'A race/ethnicity not listed here'
        ]
    )
    ability = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="On a scale from 0 (No ability) to 10 (High ability), how would you rate your ability to complete this type of task?",
        choices=[[i, str(i)] for i in range(11)]
    )
    risk = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="On a scale from 0 (Not willing to take risks) to 10 (Very willing to take risks), how willing are you to take risks?",
        choices=[[i, str(i)] for i in range(11)]
    )
    helpful = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="On a scale from 0 (Not helpful) to 10 (Very helpful), how helpful do you find ChatGPT in completing this task?",
        choices=[[i, str(i)] for i in range(11)]
    )
    future = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        label="On a scale from 0 (Not willing) to 10 (Very willing), how likely are you to use ChatGPT in your future work?",
        choices=[[i, str(i)] for i in range(11)]
    )
    why_future = models.LongStringField(
        label="Could you please explain why you would or would not use ChatGPT in your future work?"
    )
    feedback = models.LongStringField(
        label='Please provide any feedback you have about this experiment.'
    )
