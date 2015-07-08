import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = ("[Strategy Market] [Switch]"
                       "Base pair difference between states for"
                       "MS2/FMN switches")

        self.author_ = "Eli Fisker"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/"
                     "-strategy-market-switch-"
                     "base-pair-difference-between-states-for-"
                     "ms2-fmn-switches")

        # Default strategy parameters
        # First three are awards, then the penalty,
        # then the percent differences relating to the awards/penalty
        # Final parameter is the amount to increasingly penalize by
        self.default_params_ = [3.0, 2.0, 1.0, -1.0, .05, 0.1, 0.15, 0.15, 1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 18

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def percentDifference(self, val1, val2):

        # also takes care of when val1 == val2 == 0
        if val1 == val2:
            return 0

        return ((float(abs(val1 - val2)) / (float(val1 + val2) / 2)) * 100)

    def score(self, design, params):

        bpcount1 = design['gc1'] + design['gu1'] + design['ua1']
        bpcount2 = design['gc2'] + design['gu2'] + design['ua2']
        perdiff = self.percentDifference(bpcount1, bpcount2)

        score = 100

        if "miRNA" in design['labtitle']:
            score = eterna_utils.UNSCORABLE
        elif perdiff < params[4]:
            score += params[0]
        elif perdiff < params[5]:
            score += params[1]
        elif perdiff < params[6]:
            score += params[2]
        elif perdiff > params[7]:
            score += ((perdiff - params[7]) * params[8])

        return score
