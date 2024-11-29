from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'your_app_name'
    players_per_group = 2
    num_rounds = 1
    compensation_amount = c(1)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    agreed_to_participate = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],
        ],
        label="Do you agree to participate in this experiment?"
    )
    left_voluntarily = models.BooleanField(initial=False)
    forced_to_leave = models.BooleanField(initial=False)

    # Add fields for comprehension questions
    q1 = models.StringField(
        label="The experiment consists of...",
        choices=[
            ['A', 'Only negotiation phase'],
            ['B', 'Only performance evaluation'],
            ['C', 'Performance evaluation followed by negotiation'],
            ['D', 'Multiple rounds of negotiations']
        ],
        widget=widgets.RadioSelect
    )

    q2 = models.StringField(
        label="If you achieve highest performance as a worker, your contribution will be...",
        choices=[
            ['A', '$1.50'],
            ['B', '$2.00'],
            ['C', '$2.50'],
            ['D', '$3.00']
        ],
        widget=widgets.RadioSelect
    )

    q3 = models.StringField(
        label="If you achieve highest performance as a recruiter, your contribution will be...",
        choices=[
            ['A', '$1.50'],
            ['B', '$2.00'],
            ['C', '$2.50'],
            ['D', '$3.00']
        ],
        widget=widgets.RadioSelect
    )

    q4 = models.StringField(
        label="The joint revenue in negotiations equals...",
        choices=[
            ['A', "Only worker's contribution"],
            ['B', "Only recruiter's contribution"],
            ['C', "Sum of both participants' contributions"],
            ['D', 'Fixed amount regardless of performance']
        ],
        widget=widgets.RadioSelect
    )

    q5 = models.StringField(
        label="During negotiations, you have...",
        choices=[
            ['A', '1 minute to reach agreement'],
            ['B', '2 minutes to reach agreement'],
            ['C', '3 minutes to reach agreement'],
            ['D', 'Unlimited time to reach agreement']
        ],
        widget=widgets.RadioSelect
    )

    q6 = models.StringField(
        label="If no agreement is reached...",
        choices=[
            ['A', 'Negotiation continues indefinitely'],
            ['B', 'Both parties receive their full contributions'],
            ['C', 'Both parties incur a $1.00 penalty'],
            ['D', 'A new negotiation begins']
        ],
        widget=widgets.RadioSelect
    )

    q7 = models.StringField(
        label="During negotiations, participants can...",
        choices=[
            ['A', 'Only submit wage proposals'],
            ['B', 'Only use chat window'],
            ['C', 'Use both chat window and submit proposals'],
            ['D', 'Neither chat nor submit proposals']
        ],
        widget=widgets.RadioSelect
    )

    q8 = models.StringField(
        label="Which communication is NOT allowed during negotiations?",
        choices=[
            ['A', 'Wage proposals'],
            ['B', 'Professional messages'],
            ['C', 'Personal information'],
            ['D', 'Discussion of terms']
        ],
        widget=widgets.RadioSelect
    )

    q9 = models.StringField(
        label="If agreement is reached, the worker receives...",
        choices=[
            ['A', 'The suggested wage'],
            ['B', 'The agreed wage amount'],
            ['C', 'The joint revenue'],
            ['D', 'Their original contribution']
        ],
        widget=widgets.RadioSelect
    )

    q10 = models.StringField(
        label="If agreement is reached, the recruiter receives...",
        choices=[
            ['A', 'The suggested wage'],
            ['B', 'The agreed wage amount'],
            ['C', 'The joint revenue'],
            ['D', 'Joint revenue minus agreed wage']
        ],
        widget=widgets.RadioSelect
    )
    all_correct = models.BooleanField(
        initial=False,
        doc="Indicates if the player answered all questions correctly"
    )