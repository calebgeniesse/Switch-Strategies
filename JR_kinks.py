import strategy_template
import eterna_utils


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the submission
        self.title_ = "[Strategy Market][Switch] kinks"
        self.author_ = "JR"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/"
                     "-strategy-market-switch-kinks")

        # Default strategy parameters

        # params organization:
        self.default_params_ = [0.5, -1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 19

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
            for base in design['site']:
                # Elem1 is kink in aptamer state
                elem1 = self.findRNAElement(
                    eterna_utils.RNAELEMENT_LOOP,
                    base,
                    design['secstruct_elements' + str(design['on_state'])]
                )

                # Elem2 is kink splitting into interior loop
                elem2 = self.findRNAElement(
                    eterna_utils.RNAELEMENT_LOOP,
                    base,
                    design['secstruct_elements' + str(design['off_state'])]
                )

                if (elem1 is not None and elem2 is None and
                        elem1.score_ > params[0]):
                    score += params[1]

        return score
