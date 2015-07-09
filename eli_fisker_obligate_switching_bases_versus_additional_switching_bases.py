import eterna_utils
import strategy_template
import re


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = ("[Strategy Market] [Switch] "
                       "Obligate switching bases versus "
                       "additional switching bases")
        self.author_ = "Eli Fisker"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/"
                     "-strategy-market-switch-obligate-"
                     "switching-bases-versus-additional-switching-bases")

        # Default strategy parameters
        # Linear function for penalties/rewards

        # y = -5x + 2
        # y = reward
        # x = additional switching / obligate switching

        # x = 0.2, y = 1.0
        # x = 0.5, y = -0.5
        # x = 1, y = -3

        self.default_params_ = [-5.0, 2.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 37

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

        if "miRNA" in design['labtitle']:
            score = eterna_utils.UNSCORABLE
        else:
            MS2consensus = "ACAUGAGGAUCACCCAUGU"
            MS2start = design['sequence'].find(MS2consensus)
            obligate = range(MS2start, MS2start + len(MS2consensus))

            bases = design['site']
            bases.sort()

            strands = [bases[0], 100]
            for i in range(1, len(bases)):
                if bases[i] - bases[i-1] > 1:
                    strands[1] = bases[i]
                    break

            for n in range(1, 3):  # states
                for i in range(0, len(strands)):
                    elem = self.findRNAElement(
                        eterna_utils.RNAELEMENT_STACK,
                        strands[i],
                        design['secstruct_elements' + str(n)]
                    )
                    if elem is not None:
                        obligate.extend(elem.indices_)

            additionalswitches = obligateswitches = 0

            for i in range(0, len(design['sequence'])):

                if design['pairmap1'][i] != design['pairmap2'][i]:
                    if i in obligate:
                        obligateswitches += 1
                    else:
                        additionalswitches += 1

            perswitches = float(additionalswitches) / obligateswitches
            score += (params[0] * perswitches) + params[1]

        return score
