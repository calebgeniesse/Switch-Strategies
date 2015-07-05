import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market][Switch] Fix one Stem of FMN Aptamer loop"
        self.author_ = "jandersonlee"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/-strategy-market-switch")

        # Default strategy parameters
        # First param is the percent threshold to start penalizing switches, 
        # second param is the amount of increase penalties by
        self.default_params_ =  [1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 40

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def findRNAElement(self, type, bp, elements):

        if isinstance(bp, list):
            # More than one base pair to find
            for i in range(0, len(elements)):
                if elements[i].type_ != type:
                    continue
                
                match = True
                for n in range(0, len(bp)):
                    if n not in elements[i].indices_:
                        match = False
                        break
                if match:
                    return elements[i]

        else:
            for i in range(0, len(elements)):
                if elements[i].type_ == type and bp in elements[i].indices_:
                    return elements[i]
        
        return None

    def score(self, design, params):

        score = 100

        if "miRNA" in design['labtitle']:
            score = eterna_utils.UNSCORABLE
        else:

            state = design['on_state']
            otherstate = (state % 2) + 1
            state, otherstate = str(state), str(otherstate)

            bases = design['site']

            rnaelements = []

            # Find the two closing stacks
            for i in range(0, len(bases)):
                base = bases[i]
                if design['secstruct' + state][base] != ".":
                    elem = self.findRNAElement(eterna_utils.RNAELEMENT_STACK, base, design['secstruct_elements' + state])
                    if elem is not None and elem not in rnaelements:
                        rnaelements.append(elem)

            # Check if the stacks are fixed
            numfixed = 0
            for i in range(0, len(rnaelements)):
                elem = rnaelements[i]
                rnaelem = self.findRNAElement(eterna_utils.RNAELEMENT_STACK, elem.indices_, design['secstruct_elements' + otherstate])
                if rnaelem is not None:
                    numfixed += 1

            if numfixed == 1:
                score += params[0]

        return score
