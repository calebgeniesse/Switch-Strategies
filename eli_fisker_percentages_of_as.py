import strategy_template

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Strategy Market] [Switch] Percentages of A's." # Title of the strategy submission
        self.author_ = "Eli Fisker" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-percentages-of-a-s"

        # Default strategy parameters
        self.default_params_ = [0.29, 0.35, 0.31, 0.33, 1, 2]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 7

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False
        

    def score(self, design, params):

        perA = design['sequence'].count('A') / len(design['sequence'])

        score = 100
        if params[0] < perA < params[1]: score += params[4]
        if params[2] < perA < params[3]: score += params[5]
        if perA > params[1]: score -= ((perA - params[1])*100)
        if perA < params[0]: score -= ((params[0] - perA)*100)

        return score