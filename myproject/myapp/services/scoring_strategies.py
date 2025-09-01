# services/scoring_strategies.py

class ScoringStrategy:
    def calculate_score(self, questions, post_data):
        raise NotImplementedError()


class StandardScoring(ScoringStrategy):
    def calculate_score(self, questions, post_data):
        score = 0
        for question in questions:
            selected = post_data.get(f'question_{question.id}')
            if selected == question.correct_option:
                score += 1
        return score
