from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import openai
import os
import random
from openai import OpenAI
from dotenv import load_dotenv


# Set your OpenAI API key here or use an environment variable
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1
    recruiter_budget = c(10)
    negotiation_time = 180  # 3 minutes in seconds
    negotiation_penalty = c(1)  # $1 penalty for failed negotiations
    base_payment = c(1.50)  # Base payment for completing Phase 1

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            if player.role() == 'Recruiter':
                player.num_correct = player.participant.vars.get('num_correct', 0)



class Group(BaseGroup):
    deal_price = models.CurrencyField(min=0, max=Constants.recruiter_budget)
#    is_finished = models.BooleanField(initial=False)
    negotiation_successful = models.BooleanField(initial=False)
    final_wage = models.CurrencyField()
    negotiation_time_remaining = models.IntegerField(initial=Constants.negotiation_time)

    def set_final_payoffs(self):
        worker = self.get_player_by_role('Worker')
        recruiter = self.get_player_by_role('Recruiter')
        joint_revenue = self.calculate_joint_revenue()

        if self.negotiation_successful:
            worker.payoff = Constants.base_payment + self.final_wage
            recruiter.payoff = (Constants.base_payment +
                                joint_revenue - self.final_wage)
        else:
            # Failed negotiation - apply penalty
            worker.payoff = (Constants.base_payment +
                             worker.suggested_wage -
                             Constants.negotiation_penalty)
            recruiter.payoff = (Constants.base_payment +
                                joint_revenue -
                                worker.suggested_wage -
                                Constants.negotiation_penalty)

    def set_payoffs(self):
        def set_payoffs(self):
            # Find worker and recruiter using participant vars
            worker = None
            recruiter = None

            for p in self.get_players():
                if p.participant.vars.get('role') == 'Worker':
                    worker = p
                else:
                    recruiter = p

            if not worker or not recruiter:
                print("DEBUG: Could not find worker or recruiter")
                return

            if self.field_maybe_none('deal_price') is not None:
                self.negotiation_successful = True
                worker.payoff = self.field_maybe_none('deal_price')
                recruiter.payoff = Constants.recruiter_budget - self.field_maybe_none('deal_price')
            else:
                # Failed negotiation - apply penalty
                suggested_wage = worker.participant.vars.get('suggested_wage', 0)
                worker.payoff = suggested_wage - Constants.negotiation_penalty
                recruiter.payoff = Constants.recruiter_budget - suggested_wage - Constants.negotiation_penalty


class Player(BasePlayer):
    suggested_wage = models.FloatField(blank=True)
    paired_with = models.IntegerField(blank=True)
    has_ai_expert = models.BooleanField(initial=False)
    num_correct = models.IntegerField(initial=0)
    amount_proposed = models.CurrencyField(min=0, max=Constants.recruiter_budget)
    amount_accepted = models.CurrencyField(min=0, max=Constants.recruiter_budget)
    ai_chat_log = models.LongStringField(blank=True)

    def role(self):
        return self.participant.vars.get('role', '')

#here needs to pay attention
    def other_role(self):
        return 'Recruiter' if self.role() == 'Worker' else 'Worker'

    def is_worker(self):
        return self.role() == 'Worker'

    def is_recruiter(self):
        return self.role() == 'Recruiter'

    def chat_with_ai(self, message):
        client = OpenAI(api_key=OPENAI_API_KEY)
        print(f"Sending message to OpenAI: {message}")  # Debug print
        # Prepare the prompt
        prompt = f"You are an AI assistant helping an worker negotiate their salary. The worker says: {message}\nAI Assistant:"

        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping with salary negotiation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )

            # Extract the AI's response
            ai_response = response.choices[0].message.content

            # Update the AI chat log
            chat_log = self.field_maybe_none('ai_chat_log')
            if chat_log:
                chat_log = eval(chat_log)
            else:
                chat_log = []
            chat_log.append({"role": "user", "content": message})
            chat_log.append({"role": "assistant", "content": ai_response})
            self.ai_chat_log = str(chat_log)

            return ai_response

        except Exception as e:
            print(f"Error in AI chat: {str(e)}")
            return "I'm sorry, but I encountered an error. Please try again."