from otree.api import Page, WaitPage
from .models import Constants

class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

class Instructions(Page):
    form_model = 'player'
    form_fields = ['agreed_to_participate']

    def before_next_page(self):
        if self.player.field_maybe_none('agreed_to_participate') is False:
            self.player.left_voluntarily = True

class ProcessGroupDecision(WaitPage):
    def after_all_players_arrive(self):
        if any(p.field_maybe_none('agreed_to_participate') is False for p in self.group.get_players()):
            for p in self.group.get_players():
                if p.field_maybe_none('agreed_to_participate') is True:
                    p.forced_to_leave = True
                    p.payoff = Constants.compensation_amount

    def app_after_this_page(self, upcoming_apps):
        if any(p.field_maybe_none('agreed_to_participate') is False for p in self.group.get_players()):
            return upcoming_apps[-1]  # Skip to the last app (usually the payment app)

class Results(Page):
    def is_displayed(self):
        return self.player.left_voluntarily or self.player.forced_to_leave


class ComprehensionQuestions(Page):
    form_model = 'player'  # Make sure this line exists

    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    def is_displayed(self):
        return (self.player.field_maybe_none('agreed_to_participate') is True
                and not self.player.left_voluntarily
                and not self.player.forced_to_leave)


    def error_message(self, values):
        correct_answers = {
            'q1': 'C',
            'q2': 'B',
            'q3': 'D',
            'q4': 'C',
            'q5': 'C',
            'q6': 'C',
            'q7': 'C',
            'q8': 'C',
            'q9': 'B',
            'q10': 'D'
        }

        errors = {name: 'Wrong answer' for name, value in values.items()
                  if correct_answers[name] != value}
        if errors:
            return errors



page_sequence = [GroupingWaitPage, Instructions, ProcessGroupDecision,ComprehensionQuestions,Results]
