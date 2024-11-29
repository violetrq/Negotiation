from otree.api import Page, WaitPage
from .models import Constants

class MatrixTask(Page):
    form_model = 'player'
    form_fields = ['time_spent']

    def get_timeout_seconds(self):
        return 60

    def vars_for_template(self):
        return {
            'matrix': self.player.get_current_matrix(),
            'round_number': self.round_number,
            'num_rounds': Constants.num_rounds,
        }

    @staticmethod
    def live_method(player, data):
        if 'index1' in data and 'index2' in data:
            is_correct = player.check_answer(data['index1'], data['index2'])
            player.time_spent = data['time_spent']
            player.total_time += player.time_spent
            return {player.id_in_group: {'submitted': True, 'is_correct': is_correct}}

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        self.group.set_rankings()

class NegotiationDecision(Page):
    form_model = 'player'
    form_fields = ['wants_to_negotiate']

    def is_displayed(self):
        return self.player.is_worker() and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'suggested_wage': self.player.field_maybe_none('suggested_wage'),
            'rank': self.player.field_maybe_none('worker_rank'),  # Added this line
            'has_ai_expert': self.player.field_maybe_none('has_ai_expert')
        }

    def before_next_page(self):
        if self.player.is_worker():
            # Store decision and data in participant vars
            self.participant.vars['wants_to_negotiate'] = self.player.wants_to_negotiate
            self.participant.vars['suggested_wage'] = self.player.field_maybe_none('suggested_wage')

            # Find paired recruiter and update their vars
            for p in self.group.get_players():
                if p.is_recruiter() and p.field_maybe_none('paired_with') == self.player.id_in_group:
                    # Set the same next app for the recruiter
                    next_app = 'bargaining' if self.player.wants_to_negotiate else 'questionnaire'
                    p.participant.vars['next_app'] = next_app
                    p.participant.vars['suggested_wage'] = self.player.field_maybe_none('suggested_wage')
                    break

            # Set next app for worker
            self.participant.vars['next_app'] = 'bargaining' if self.player.wants_to_negotiate else 'questionnaire'



    def app_after_this_page(self, upcoming_apps):
        return self.participant.vars.get('next_app', 'questionnaire')

class PostQuestionnaire(Page):
    def is_displayed(self):
        if self.round_number != Constants.num_rounds:
            return False

        # For workers
        if self.player.is_worker():
            return self.player.field_maybe_none('wants_to_negotiate') is False
        # For recruiters - follow paired worker's decision
        else:
            paired_worker = self.group.get_players()[0] if self.player == self.group.get_players()[2] else self.group.get_players()[1]
            worker_choice = paired_worker.field_maybe_none('wants_to_negotiate')
            return worker_choice is not None and worker_choice is False


class Bargaining(Page):
    def is_displayed(self):
        # Only show in final round
        if self.round_number != Constants.num_rounds:
            return False

        # For workers
        if self.player.is_worker():
            return self.player.field_maybe_none('wants_to_negotiate') is True
        # For recruiters - find their paired worker's decision
        else:
            # Get paired worker (players[0] with players[2], players[1] with players[3])
            paired_worker = self.group.get_players()[0] if self.player == self.group.get_players()[2] else self.group.get_players()[1]
            # Only show negotiation if worker has made a decision AND chose to negotiate
            worker_choice = paired_worker.field_maybe_none('wants_to_negotiate')
            return worker_choice is not None and worker_choice is True

    def vars_for_template(self):
        if not self.player.is_worker():
            paired_worker = (self.group.get_players()[0]
                             if self.player == self.group.get_players()[2]
                             else self.group.get_players()[1])
            suggested_wage = paired_worker.field_maybe_none('suggested_wage')
        else:
            suggested_wage = self.player.field_maybe_none('suggested_wage')

        return {
            'has_ai_expert': self.player.field_maybe_none('has_ai_expert') if self.player.is_worker() else False,
            'is_worker': self.player.is_worker(),
            'suggested_wage': suggested_wage
        }

class PostQuestionnaire(Page):
    def is_displayed(self):
        # Show only if it's last round AND
        # either: player is worker who chose NOT to negotiate OR
        # player is recruiter whose paired worker chose NOT to negotiate
        if self.round_number != Constants.num_rounds:
            return False

        if self.player.is_worker():
            return self.player.field_maybe_none('wants_to_negotiate') == False
        else:  # is recruiter
            worker = self.group.get_players()[0] if self.player == self.group.get_players()[2] else \
            self.group.get_players()[1]
            return worker.field_maybe_none('wants_to_negotiate') == False

    def vars_for_template(self):
        return {
            'suggested_wage': self.player.field_maybe_none('suggested_wage'),
            'is_worker': self.player.is_worker()
        }



class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds  # Only display on last round

    def vars_for_template(self):
        # Get all previous rounds data
        all_rounds = self.player.in_all_rounds()
        total_correct = sum(p.correct_answer for p in all_rounds)

        return {
            'num_correct': total_correct,
            'total_rounds': Constants.num_rounds,
            'suggested_wage': self.player.field_maybe_none('suggested_wage'),
            'rank': self.player.field_maybe_none('worker_rank' if self.player.is_worker() else 'recruiter_rank'),
            'is_worker': self.player.is_worker(),
        }


class FinalWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds  # Use subsession instead of self

    def after_all_players_arrive(self):
        for group in self.subsession.get_groups():  # Loop through all groups
            group.set_rankings()

class DecisionWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.is_recruiter() and self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        # Ensure all workers have made their decisions
        pass

class RecruiterDecision(Page):
    def is_displayed(self):
        return self.player.is_recruiter() and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'worker_decision': self.participant.vars.get('paired_worker_wants_negotiate'),
            'suggested_wage': self.participant.vars.get('paired_worker_suggested_wage')
        }

    def app_after_this_page(self, upcoming_apps):
        return 'bargaining' if self.participant.vars.get('paired_worker_wants_negotiate') else 'questionnaire'

class AcceptedWageResults(Page):
    def is_displayed(self):
        return (self.round_number == Constants.num_rounds and
                not self.participant.vars.get('wants_to_negotiate', True))

    def vars_for_template(self):
        return {
            'is_worker': self.player.is_worker(),
            'suggested_wage': self.player.field_maybe_none('suggested_wage'),
            'total_contribution': self.player.calculate_contribution()
        }


#page_sequence = [MatrixTask, FinalWaitPage, Results, NegotiationDecision, Bargaining, PostQuestionnaire]
page_sequence = [MatrixTask, FinalWaitPage, Results, NegotiationDecision, DecisionWaitPage, AcceptedWageResults]


#page_sequence = [RecruiterWait, WorkerTask, ResultsWaitPage, Results]