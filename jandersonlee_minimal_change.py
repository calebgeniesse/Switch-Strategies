import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market][Switch] Minimal change"
        self.author_ = "jandersonlee"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-minimal-change")

        # Default strategy parameters
        # First param is the percent threshold to start penalizing switches, 
        # second param is the amount of increase penalties by
        self.default_params_ = [0.3, 10]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 14

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def score(self, design, params):

        switches = 0
        score = 100

        for i in range(0, len(design['sequence'])):
            if design['secstruct1'][i] != design['secstruct2'][i]:
                # If between the states it switches from paired to unpaired
                switches += 1
            elif design['secstruct1'][i] != ".":
                # Or if it remains paired, but what it pairs with is different
                pair1 = design['sequence'][design['pairmap1'][i]]
                pair2 = design['sequence'][design['pairmap2'][i]]
                if pair1 != pair2:
                    switches += 1

        # Convert to percentage so threshold applies for seqs of all lengths
        switches = float(switches) / len(design['sequence'])

        if switches > params[0]:
            score -= (switches * params[1])

        return score
