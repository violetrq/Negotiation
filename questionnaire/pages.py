from otree.api import Page, WaitPage
from .models import Constants

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['participant_role', 'age', 'gender', 'education', 'experience', 'race', 'ability', 'risk', 'helpful', 'future', 'why_future', 'feedback']

#    def vars_for_template(self):
#        self.player.participant_role = self.participant.vars.get('role', '')
#        return {}

    def vars_for_template(self):
        return {
            'role': self.player.role(),  # Get role from player
            'suggested_wage': self.participant.vars.get('suggested_wage'),
            'is_worker': self.player.is_worker()
        }


    def before_next_page(self):
        self.player.participant_role = self.participant.vars.get('role')
class ThankYou(Page):
    pass

page_sequence = [Questionnaire, ThankYou]