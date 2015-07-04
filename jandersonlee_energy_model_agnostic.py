import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market][Switch] Energy Model Agnostic"
        self.author_ = "jandersonlee"

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-energy-model-agnostic"

        # Default strategy parameters
        # First param is the percent threshold to start penalizing switches, 
        # second param is the amount of increase penalties by
        self.default_params_ = [0.3, 10]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 16

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def score(self, design, params):

        switches = 0
        score = 100
        states = [1, 2]

        for n in range(0, len(states)):
            for i in range(0, len(design['sequence'])):
                if design['secstruct' + str(states[n]) + "_v1"][i] != design['secstruct' + str(states[n]) + "_v2.2"][i]:
                    switches += 1
                elif design['secstruct' + str(states[n]) + "_v1"][i] != ".":
                    pair1 = design['sequence'][design['pairmap' + str(states[n]) + "_v1"][i]]
                    pair2 = design['sequence'][design['pairmap' + str(states[n]) + "_v2.2"][i]]
                    if pair1 != pair2:
                        switches += 1

        # Convert to percentage so threshold applies for seqs of all lengths
        switches = float(switches) / len(design['sequence'])

        if switches > params[0]:
            score -= (switches * params[1])

        return score
