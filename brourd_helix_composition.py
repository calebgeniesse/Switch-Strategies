import eterna_utils
from eterna_utils import *
import strategy_template


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market] [Switch] Helix Composition"
        self.author_ = "Brourd"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/"
                     "-strategy-market-switch-helix-composition")

        # Default strategy parameters
        # Row 1: penalties/awards for active helices
        # Row 2: thresholds for active helices
        # Row 3: penalties for passive helices
        # Row 4: thresholds for passive helices
        self.default_params_ = [1.0, 1.0, -1.0, -2.0, -1.0, -1.0,
                                2, 2, 0, 3, 2, 0, 1, 0, 2,
                                -1.0, -1.0, -1.0,
                                3, 2.0, 7, 0.05
                                ]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 81

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def findRNAElement(self, type, bplist, elements):

        for i in range(0, len(elements)):
            if elements[i].type_ != type:
                continue

            match = True
            for n in range(0, len(bplist)):
                if n not in elements[i].indices_:
                    match = False
                    break
            if match:
                return elements[i]
        return None

    def calculateBPAmount(self, element, sequence, secstruct, pmap):

        bpGC = bpGU = bpAU = 0

        # Theoretically, numBP = bpGC + bpGU + bpAU
        numBP = float(len(element.indices_)) / 2

        for i in element.indices_:
            # Avoid double counting by only looking forwards at "(" basepairs
            if secstruct[i] != '(':
                continue
            if ((sequence[i] == 'G' and sequence[pmap[i]] == 'C') or
                    (sequence[i] == 'C' and sequence[pmap[i]] == 'G')):
                bpGC += 1
            if ((sequence[i] == 'G' and sequence[pmap[i]] == 'U') or
                    (sequence[i] == 'U' and sequence[pmap[i]] == 'G')):
                bpGU += 1
            if ((sequence[i] == 'A' and sequence[pmap[i]] == 'U') or
                    (sequence[i] == 'U' and sequence[pmap[i]] == 'A')):
                bpAU += 1

        return (bpGC, bpGU, bpAU, numBP)

    def score(self, design, params):

        score = 100

        for n in range(1, 3):

            actives = []
            passives = []
            otherstate = (n % 2) + 1
            state = str(n)

            elems = design['secstruct_elements' + state]

            for i in range(0, len(elems)):
                rnaelem = self.findRNAElement(
                    eterna_utils.RNAELEMENT_STACK,
                    elems[i].indices_,
                    design['secstruct_elements' + str(otherstate)]
                )
                if rnaelem is not None:
                    passives.append(elems[i])
                else:
                    actives.append(elems[i])

            for i in range(0, len(actives)):
                bpGC, bpGU, bpAU, numBP = self.calculateBPAmount(
                    actives[i],
                    design['sequence'],
                    design['secstruct' + state],
                    design['pairmap' + state]
                )

                ''''
                # Copied params down here to better proofread
                # Row 1: penalties/awards for active helices
                # Row 2: thresholds for active helices
                # Row 3: penalties for passive helices
                # Row 4: thresholds for passive helices

                self.default_params_ = [0=1.0, 1=1.0, 2=-1.0, 3=-2.0, 4=-1.0, 5=-1.0,
                                6=2, 7=2, 8=0, 9=3, 10=2, 11=0, 12=1, 13=0, 14=2,
                                15=-1.0, 16=-1.0, 17=-1.0,
                                18=3, 19=2.0, 20=7, 21=0.05
                                ]

                '''
                if bpGC == params[6]:
                    score += params[0]
                elif bpGC > params[7] and bpGU == params[8]:
                    score += params[1] * (bpGC - params[7])

                #TODO RB 10/13/15
                #Rule for the elif below which I'm not sure is interpreted correctly:
                #      'If the number of G-C base pairs in an active helix exceeds 
                #       the count of two, and there are G-u base pairs between the
                #       G-C base pairs in the helix, then neither reward nor penalize
                #       up to a maximum of 3 G-C base pairs and two G-U base pairs between
                #       the G-C base pairs'
                #
                #   Should be ((bpGC >= params[9] but not sure about the second 'or' half
                #   also doesn't test the position of the G-U base pairs, but that is not trivial
                elif ((bpGC > params[9] and bpGU <= params[10]) or
                        (bpGC <= params[9] and bpGU > params[10])):
                    score += params[2]

                elif bpGC == params[11]:
                    score += params[3]
                elif bpGC == params[12] and bpGU > params[13]:
                    score += params[4]

                if numBP <= params[14]:
                    score += params[5]

            for i in range(0, len(passives)):
                bpGC, bpGU, bpAU, numBP = self.calculateBPAmount(
                    passives[i],
                    design['sequence'],
                    design['secstruct' + state],
                    design['pairmap' + state]
                )

                if numBP <= params[18]:
                    score += params[15]

                if bpGC <= (float(numBP) / params[19]) and numBP < params[20]:
                    score += params[16]

                for j in range(0, len(design['dotplot' + state])):
                    dot = design['dotplot' + state][j]
                    if (dot[0] in passives[i].indices_ or
                            dot[1] in passives[i].indices_ and
                            dot[2] <= params[21]):
                        # Alternative pairing
                        score += params[17]

        return score

#My own little test code
#designs = get_synthesized_designs_from_eterna_server()
#design = designs[1]
#print design
seq =       'AAAAGAAACAA'
struct =    '....(...)..'
design = get_design_from_sequence(seq,struct)
design['secstruct_elements1'] = design['secstruct_elements']
design['secstruct_elements2'] = design['secstruct_elements']
design['secstruct1'] = design['secstruct']
design['secstruct2'] = design['secstruct']
design['pairmap1'] = design['pairmap']
design['pairmap2'] = design['pairmap']
strat = Strategy()
score = strat.score(design,strat.default_params_)
print score
