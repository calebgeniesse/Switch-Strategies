import strategy_template

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Strategy Market][Switch] Penalize large amounts of GC pairs" # Title of the strategy submission
        self.author_ = "vineetkosaraju" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-penalize-large-amounts-of-gc-pairs"

        # Default strategy parameters
        self.default_params_ = [0.4, 0.2, 0.4, 0.2, 1.0, 1.0, 1.0, 1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 8

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False
        

    def score(self, design, params):
        perGCstate1 = float(design['gc1']) / (design['gu1'] + design['gc1'] + design['ua1'])
        perGCstate2 = float(design['gc2']) / (design['gu2'] + design['gc2'] + design['ua2'])

        score = 100

        if perGCstate1 > params[0]: score -= ((perGCstate1 - params[0])*100*params[4])
        elif perGCstate1 < params[1]: score -= ((params[1] - perGCstate1)*100*params[5])

        if perGCstate2 > params[2]: score -= ((perGCstate2 - params[0])*100*params[6])
        elif perGCstate2 < params[3]: score -= ((params[1] - perGCstate2)*100*params[7])
        
        return score