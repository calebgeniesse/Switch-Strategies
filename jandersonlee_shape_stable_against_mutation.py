import strategy_template
import eterna_utils
import inv_utils

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market][Switch] Shape stable against mutation"
        self.author_ = "jandersonlee"

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-shape-stable-against-mutation"

        # Default strategy parameters
        # First param is penalty for state 1, second is for state 2
        self.default_params_ = [-1.0, -1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 14

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def score(self, design, params):

        score = 100
        seq = design['sequence']

        for i in range(0, len(seq)):

            # Pairs the same way in both states, avoiding double counting
            # by only looking at the opening bases

            if( (design['pairmap1'][i] == design['pairmap2'][i]) and 
                (design['secstruct1'][i] == design['secstruct2'][i] == '(') ):

                # Try swapping the sequence
                bp1 = design['pairmap1'][i]
                newSequence = seq[:i] + seq[bp1] + seq[(i+1):bp1] + seq[i] + seq[(bp1+1):]

                # viennaconstraint includes the binding (On state)
                newSS_binding = inv_utils.fold(newSequence, False, design['viennaconstraint'])
                newSS_nobinding = inv_utils.fold(newSequence)

                if(newSS_binding != design['secstruct' + str(design['on_state'])]):
                    score += params[0]

                if(newSS_nobinding != design['secstruct' + str(design['off_state'])]):
                    score += params[1]

        return score
