from otree.api import Page, WaitPage
from .models import Constants

class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

class Instructions(Page):

    def before_next_page(self):
        # We can simplify this since proceeding means they agreed to participate
        pass
class ProcessGroupDecision(WaitPage):
    def after_all_players_arrive(self):
        pass

    def app_after_this_page(self, upcoming_apps):
        pass

class Results(Page):
    def is_displayed(self):
        return self.player.left_voluntarily or self.player.forced_to_leave


class ComprehensionQuestions(Page):
    form_model = 'player'  # Make sure this line exists

    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    def is_displayed(self):
        return not self.player.left_voluntarily and not self.player.forced_to_leave

    def error_message(self, values):
        # Define correct answers with explanations
        correct_answers = {
            'q1': {'answer': 'C',
                   'explanation': 'The experiment consists of performance evaluation followed by negotiation.'},
            'q2': {'answer': 'B', 'explanation': 'For workers, the highest performance contribution is $1.50.'},
            'q3': {'answer': 'D', 'explanation': 'For recruiters, the highest performance contribution is $2.50.'},
            'q4': {'answer': 'C',
                   'explanation': 'The joint revenue equals the sum of both participants\' contributions.'},
            'q5': {'answer': 'C', 'explanation': 'You have 5 minutes to reach an agreement during negotiations.'},
            'q6': {'answer': 'C', 'explanation': 'If no agreement is reached, both parties incur a $1.00 penalty.'},
            'q7': {'answer': 'C',
                   'explanation': 'During negotiations, participants can use both chat window and submit proposals.'},
            'q8': {'answer': 'C', 'explanation': 'Sharing personal information is not allowed during negotiations.'},
            'q9': {'answer': 'B',
                   'explanation': 'If agreement is reached, the worker receives the agreed wage amount.'},
            'q10': {'answer': 'D',
                    'explanation': 'If agreement is reached, the recruiter receives the joint revenue minus agreed wage.'}
        }

        # Check answers and create error messages with explanations
        errors = {}
        for field_name, value in values.items():
            if value != correct_answers[field_name]['answer']:
                errors[field_name] = f'Incorrect. The correct answer is: {correct_answers[field_name]["explanation"]}'

        if errors:
            return errors



page_sequence = [GroupingWaitPage, Instructions, ProcessGroupDecision,ComprehensionQuestions,Results]
