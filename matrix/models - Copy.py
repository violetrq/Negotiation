from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range
)
import random
# Define your matrices here (3x4 matrices)
MATRICES = [
    [[8.1, 4.0, 5.0, 4.6], [0.8, 4.1, 1.1, 8.3], [6.5, 3.4, 1.9, 2.4]],
    [[0.9, 6.1, 7.6, 7.3], [1.2, 8.6, 6.6, 8.3], [4.0, 3.4, 7.1, 5.7]],
    [[8.6, 9.3, 7.7, 6.8], [3.8, 2.4, 6.5, 9.4], [1.6, 0.7, 6.4, 4.2]],
    [[7.2, 9.8, 0.3, 8.0], [9.8, 2.7, 8.2, 3.6], [2.8, 1.2, 1.8, 4.7]],
    [[8.7, 2.5, 8.0, 6.4], [3.4, 0.9, 1.6, 5.8], [7.5, 4.6, 2.3, 9.3]],
    [[0.4, 1.0, 0.7, 4.6], [2.5, 9.0, 3.4, 5.2], [6.4, 0.8, 2.1, 8.1]],
    [[1.6, 1.7, 5.1, 1.9], [7.5, 9.0, 8.4, 2.3], [4.6, 5.9, 6.5, 3.0]],
    [[0.6, 9.3, 2.4, 5.5], [0.8, 5.1, 3.2, 4.6], [1.8, 4.0, 6.7, 7.6]],
    [[1.4, 8.9, 6.1, 5.5], [6.2, 1.7, 3.5, 2.8], [3.8, 9.6, 1.3, 7.1]],
    [[2.7, 8.6, 5.5, 3.9], [0.8, 9.1, 4.6, 2.4], [4.7, 3.4, 6.1, 7.3]]
]

class Constants(BaseConstants):
    name_in_url = 'matrix_game'
    players_per_group = 4  # Changed to 6 players per group
    num_rounds = len(MATRICES)
    # Payment structure as per instructions
    base_payment = 1.50  # Base payment for completing Phase 1
    worker_payments = {
        1: 2.00,  # Highest performing worker
        2: 1.50   # Second highest performing worker
    }
    recruiter_payments = {
        1: 3.00,  # Highest performing recruiter
        2: 2.50   # Second highest performing recruiter
    }
    negotiation_penalty = 1.00  # Penalty for failed negotiation
    negotiation_time = 180  # 3 minutes in seconds


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            print("DEBUG: Starting session creation")
            for group in self.get_groups():
                # Get the players
                players = group.get_players()

                # Assign roles - players 0,1 are workers, players 2,3 are recruiters
                workers = players[:2]
                recruiters = players[2:]

                # Assign worker roles
                for w in workers:
                    w.participant.vars['role'] = 'Worker'
                    w.has_ai_expert = random.choice([True, False])

                # Assign recruiter roles
                for r in recruiters:
                    r.participant.vars['role'] = 'Recruiter'
                    r.has_ai_expert = False

                # Create pairs: worker 0 with recruiter 0, worker 1 with recruiter 1
                for i in range(2):
                    worker = workers[i]
                    recruiter = recruiters[i]

                    # Store pairing
                    worker.participant.vars['paired_with'] = recruiter.id_in_group
                    recruiter.participant.vars['paired_with'] = worker.id_in_group

                    print(f"DEBUG: Paired Worker {worker.id_in_group} with Recruiter {recruiter.id_in_group}")
class Group(BaseGroup):
    def set_rankings(self):
        subsession_players = self.subsession.get_players()

        for p in self.get_players():
            all_rounds = p.in_all_rounds()
            p.num_correct = sum(round.correct_answer for round in all_rounds)

        workers = [p for p in self.get_players() if p.role() == 'Worker']
        recruiters = [p for p in self.get_players() if p.role() == 'Recruiter']

        # Rank workers and calculate their wages
        sorted_workers = sorted(workers, key=lambda x: -x.num_correct)
        base_wages = {1: 2, 2: 1.5}
        noise = [0.3, 0.2, 0.1]

        for rank, worker in enumerate(sorted_workers, 1):
            worker.worker_rank = rank
            base_wage = base_wages[rank]
            random_noise = random.choice(noise)
            random_sign = random.choice([-1, 1])
            worker.suggested_wage = base_wage + (random_noise * random_sign)

        # Rank recruiters and set their wages based on rank
        sorted_recruiters = sorted(recruiters, key=lambda x: -x.num_correct)
        recruiter_wages = {1: 3.0, 2: 2.5}  # Added rank 3 wage
        # Or alternatively, use get() with a default value:
        for rank, recruiter in enumerate(sorted_recruiters, 1):
            recruiter.recruiter_rank = rank
            recruiter.suggested_wage = recruiter_wages.get(rank, 2.5)  # Default to 2.5 if rank not found

    def set_payoffs(self):
        players = self.get_players()
        workers = [p for p in players if p.is_worker()]
        recruiters = [p for p in players if p.is_recruiter()]

        # Now you can work with workers and recruiters directly
        for worker, recruiter in zip(workers, recruiters):
            # Your payoff calculation logic here
            pass

class Player(BasePlayer):
    # Existing fields
    correct_answer = models.BooleanField(initial=False)
    time_spent = models.FloatField(blank=True)
    num_correct = models.IntegerField(initial=0)
    total_time = models.FloatField(initial=0)

    # New fields
    paired_with = models.IntegerField()
    worker_rank = models.IntegerField(null=True,blank=True)
    recruiter_rank = models.IntegerField(null=True,blank=True)
    suggested_wage = models.FloatField(blank=True)
    has_ai_expert = models.BooleanField(initial=False)
    wants_to_negotiate = models.BooleanField(
        choices=[
            [True, 'Negotiate'],
            [False, 'Accept suggested wage']
        ],
        blank=True
    )
    has_ai_expert = models.BooleanField(blank=True)

    def role(self):
        if self.participant.vars['role'] == 'Worker':
            return 'Worker'
        else:
            return 'Recruiter'

    def get_partner(self):
        if self.is_worker():
            return self.group.get_players()[2] if self == self.group.get_players()[0] else self.group.get_players()[3]
        else:
            return self.group.get_players()[0] if self == self.group.get_players()[2] else self.group.get_players()[1]

    def is_worker(self):
        return self.role() == 'Worker'

    def is_recruiter(self):
        return self.role() == 'Recruiter'

    def get_current_matrix(self):
        return MATRICES[self.round_number - 1]

    def check_answer(self, index1, index2):
        matrix = self.get_current_matrix()
        value1 = matrix[index1[0]][index1[1]]
        value2 = matrix[index2[0]][index2[1]]
        self.correct_answer = (abs(value1 + value2 - 10) < 0.01)  # Using approximate equality
        if self.correct_answer:
            self.num_correct += 1
        return self.correct_answer

    def calculate_results(self):
        if self.is_worker():
            all_rounds = self.in_all_rounds()
            self.num_correct = sum(p.correct_answer for p in all_rounds)

    def calculate_contribution(self):
        """Calculate player's contribution based on rank and role"""
        if self.is_worker():
            return Constants.worker_payments.get(self.worker_rank, 0)
        else:
            return Constants.recruiter_payments.get(self.recruiter_rank, 0)

    def calculate_final_payoff(self):
        """Calculate final payoff including base payment"""
        base = Constants.base_payment
        if not self.wants_to_negotiate:
            # Accepted suggested wage
            if self.is_worker():
                return base + self.suggested_wage
            else:
                worker = self.get_partner()
                return base + (self.calculate_contribution() +
                               worker.calculate_contribution() -
                               worker.suggested_wage)
        else:
            # Negotiation case - handled in bargaining app
            pass