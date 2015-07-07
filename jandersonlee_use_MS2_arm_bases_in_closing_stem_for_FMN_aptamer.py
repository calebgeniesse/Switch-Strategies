import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market][Switch] Use MS2 arm bases in closing stem for FMN aptamer"
        self.author_ = "jandersonlee"

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-fd0c2g5dp697q"

        # Default strategy parameters
        self.default_params_ = [5, 1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 31

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
            bases = design['site']

            # get all RNA elements in both states
            elems = design['secstruct_elements1']
            elems.extend(design['secstruct_elements2'])

            for base in bases:
                elem = self.findRNAElement(eterna_utils.RNAELEMENT_STACK, base, elems)
                if elem is not None:

                    matchlen = -1

                    for i in elem.indices_:
                        for k in range(0, len(MS2consensus) - 1):
                            pmatchlen = 0
                            for j in range(k, len(MS2consensus)):
                                if i + j < len(design['sequence']) and MS2consensus[j] == design['sequence'][i + j]:
                                    pmatchlen += 1
                                else:
                                    break
                            if pmatchlen > matchlen:
                                matchlen = pmatchlen

                    if 1 < matchlen < params[0]:
                        score += params[1] * (matchlen)
                    elif params[0] <= matchlen:
                        score += params[1] * (params[0])

        return score
