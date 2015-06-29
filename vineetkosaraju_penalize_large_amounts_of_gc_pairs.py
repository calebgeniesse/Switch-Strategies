import strategy_template

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Strategy Market][Switch] Penalize large amounts of GC pairs" # Title of the strategy submission
        self.author_ = "vineetkosaraju" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-penalize-large-amounts-of-gc-pairs"

        # Default strategy parameters
        self.default_params_ = [0.4, 0.2]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 4

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False
        

	def score(self, design, params):
        perGC = float(design['gc'] / (design['gu'] + design['gc'] + design['ua']))
        
        if perGC > params[0]:   return 100 - ((perGC - params[0])*100)
        elif perGC < params[1]: return 100 - ((params[1] - perGC)*100)
        else:                   return 100