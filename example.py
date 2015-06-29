import strategy_template

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Example] Title - 60%% GC" # Title of the strategy submission
        self.author_ = "Example Author" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "http://getsatisfaction.com/eternagame/topics/examplelink"

        # Default strategy parameters
        self.default_params_ = [0.6]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 1

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False


    def score(self, design, params):
        return 100-(abs(params[0] - float(design['gc']) / (design['gu'] + design['gc'] + design['ua']))) * 100