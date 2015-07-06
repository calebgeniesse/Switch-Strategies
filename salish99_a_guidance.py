import strategy_template
import re
import eterna_utils

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Strategy Market][Switch]A guidance" # Title of the strategy submission
        self.author_ = "salish99" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-a-guidance"

        # Default strategy parameters

        # params organization:
        self.default_params_ = [0.4, -1, 2, 5, 3, -1.0, 3.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 27

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def findRNAElement(self, type, bp, elements):

        for i in range(0, len(elements)):
            if elements[i].type_ == type and bp in elements[i].indices_:
                return elements[i]

        return None

    def score(self, design, params):

        score = 100

        perA = 0
        for i in range(0, len(design['sequence'])):
            if design['sequence'][i] == "A":
                perA += 1

        perA = float(perA) / len(design['sequence'])

        # Limit the number of As by percentage - 40%
        if perA > params[0]:
            score += params[1]

        # count AA (2), AAA (3), AAAA (4), AAAAA(5) occurences and penalize
        for i in range(params[2], params[3] + 1):
            seq = "A" * i
            count = design['sequence'].count(seq)
            if count > params[4]:
                score += (params[5] * (count - params[4]))

        # big bonus to quad(4) A when 1 or more A is in a loop (creates hinge)
        quadlocs = [m.start() for m in re.finditer("AAAA", design['sequence'])]
        
        # get all RNA elements in both states
        elems = design['secstruct_elements1']
        elems.extend(design['secstruct_elements2'])

        for loc in quadlocs:
            for i in range(loc, loc+4):
                elem = self.findRNAElement(eterna_utils.RNAELEMENT_LOOP, i, elems)
                if elem is not None:
                    score += params[6]
                    break

        return score