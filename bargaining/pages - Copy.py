from otree.api import Page, WaitPage
from .models import Constants


class Bargaining(Page):
    timeout_seconds = Constants.negotiation_time

    def before_next_page(self):
        if not self.group.field_maybe_none('negotiation_successful'):
            role = self.participant.vars.get('role')
            if role == 'Worker':
                suggested_wage = self.participant.vars.get('suggested_wage', 0)
            else:
                # Get paired worker's suggested wage
                paired_id = self.participant.vars.get('paired_with')
                paired_worker = next((p for p in self.group.get_players()
                                      if p.id_in_group == paired_id), None)
                suggested_wage = paired_worker.participant.vars.get('suggested_wage', 0) if paired_worker else 0

            self.group.final_wage = suggested_wage - Constants.negotiation_penalty
            self.group.set_payoffs()

    def is_displayed(self):
        role = self.participant.vars.get('role')
        if role == 'Worker':
            return self.participant.vars.get('wants_to_negotiate', False)
        elif role == 'Recruiter':
            paired_id = self.participant.vars.get('paired_with')
            paired_worker = next((p for p in self.group.get_players()
                                if p.id_in_group == paired_id), None)
            return paired_worker.participant.vars.get('wants_to_negotiate', False) if paired_worker else False
        return False

    def vars_for_template(self):
        if not self.player.is_worker():
            # Find paired worker using participant vars
            paired_id = self.participant.vars.get('paired_with')
            paired_worker = next((p for p in self.group.get_players()
                                  if p.id_in_group == paired_id), None)
            suggested_wage = paired_worker.participant.vars.get('suggested_wage') if paired_worker else 0
        else:
            suggested_wage = self.participant.vars.get('suggested_wage')

        return {
            'has_ai_expert': self.participant.vars.get('has_ai_expert', False),
            'is_worker': self.player.is_worker(),
            'suggested_wage': suggested_wage
        }

    def app_after_this_page(self, upcoming_apps):  # ADD THIS METHOD
        return 'questionnaire'

    def js_vars(self):
        return dict(
            my_id=self.player.id_in_group,
            is_worker=self.player.is_worker()
        )

    @staticmethod
    def live_method(player, data):
        group = player.group

        # Get the paired player
        paired_id = player.participant.vars.get('paired_with')
        other = next((p for p in group.get_players()
                      if p.id_in_group == paired_id), None)

        if not other:
            print(f"DEBUG: No pair found for player {player.id_in_group}")
            return

        print(f"DEBUG: Processing message between {player.id_in_group} and {other.id_in_group}")

        if data.get('type') == 'ai_chat':
            ai_response = player.chat_with_ai(data['message'])
            return {player.id_in_group: {'type': 'ai_response', 'message': ai_response}}

        if data.get('type') == 'negotiate':
            return {other.id_in_group: dict(negotiate_response=data['message'])}

        if data.get('type') == 'propose' or data.get('type') == 'accept':
            try:
                amount = float(data['amount'])
            except Exception:
                print('Invalid message received', data)
                return

            if data['type'] == 'accept':
                if amount == other.field_maybe_none('amount_proposed'):
                    player.amount_accepted = amount
                    group.deal_price = amount
                    group.negotiation_successful = True
                    group.is_finished = True
                    group.set_payoffs()
                    return {0: dict(finished=True)}

            if data['type'] == 'propose':
                player.amount_proposed = amount

            proposals = []
            for p in [player, other]:
                amount_proposed = p.field_maybe_none('amount_proposed')
                if amount_proposed is not None:
                    proposals.append([p.id_in_group, amount_proposed])
            return {0: dict(proposals=proposals)}
class BargainingWaitPage(WaitPage):
    def is_displayed(self):
        role = self.participant.vars.get('role')
        if role == 'Worker':
            return self.participant.vars.get('wants_to_negotiate', False)
        elif role == 'Recruiter':
            paired_id = self.participant.vars.get('paired_with')
            paired_worker = next((p for p in self.group.get_players()
                                if p.id_in_group == paired_id), None)
            return paired_worker.participant.vars.get('wants_to_negotiate', False) if paired_worker else False
        return False





class Results(Page):
    def vars_for_template(self):
        workers = [p for p in self.group.get_players() if p.participant.vars.get('role') == 'Worker']
        worker = workers[0] if workers else None
        return {
            'worker_num_correct': worker.num_correct if worker else None,
            'deal_price': self.player.group.field_maybe_none('deal_price'),
            'payoff': self.player.payoff
        }


page_sequence = [BargainingWaitPage, Bargaining]