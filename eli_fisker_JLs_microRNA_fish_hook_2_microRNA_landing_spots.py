import eterna_utils
import strategy_template
import re


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the strategy submission
        self.title_ = "[Strategy Market] [Switch] JL's microRNA fish hook 2: MicroRNA landing spots"

        self.author_ = "Eli Fisker"

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-jl-s-microrna-fish-hook-2-microrna-landing-spots"

        # Default strategy parameters
        self.default_params_ = [-5.0, 6, 28, 2.0, 8, 14, 2.0, 11, 2.0, 8, 14, 2, 2.0, 11, 6, 19, 2.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 52

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    def canPair(self, b1, b2):
        return ((b1 == 'G' and (b2 == 'U' or b2 == 'C')) or
            (b1 == 'U' and (b2 == 'A' or b2 == 'G')) or
            (b1 == 'A' and (b2 == 'U')) or
            (b1 == 'C' and (b2 == 'G')))

    def findLongestComplement(self, seq1, start1, stop1, seq2, start2, stop2):
        comp = None
        complength = 0
        compstart = -1

        for n in range(start2, stop2 - (stop1 - start1)):
            pcomp = []
            pcomplength = 0
            pstart = -1
            for i in range(start1, stop1):
                if self.canPair(seq1[i], seq2[i + n]):
                    pcomp.append(i+n)
                    pcomplength += 1
                    if pstart == -1:
                        pstart = i
                else:
                    pcomp.append(-1)

            if pcomplength > complength:
                complength = pcomplength
                comp = pcomp
                compstart = pstart

        return (comp, complength, compstart)

    def score(self, design, params):

        score = 100

        if "miRNA" not in design['labtitle']:
            score = eterna_utils.UNSCORABLE
        else:
            MS2consensus = "ACAUGAGGAUCACCCAUGU"
            start = design['sequence'].find(MS2consensus)
            stop = start + len(MS2consensus)
            seq = design['sequence']
            miRNA = design['oligo-seq']

            if "turn-off" in design['puztitle']:
                (comp, complength, compstart) = self.findLongestComplement(miRNA, 0, len(miRNA), seq, 0, len(seq))
                if complength != 0 :
                    if comp[compstart] < start:
                        score += params[0]  # large penalty
                    elif params[1] <= comp[compstart] - start <= params[2]:
                        score += (params[3] * complength)

            else:
                # MS2 in early half
                if stop + start < len(seq):
                    (comp, complength, compstart) = self.findLongestComplement(miRNA, len(miRNA) - params[4], len(miRNA), seq, start - params[5], start)
                    score += (params[6] * complength)

                    (comp, complength, compstart) = self.findLongestComplement(miRNA, 0, params[7], seq, stop, stop + params[7])
                    score += (params[8] * complength)
                else:
                    (comp, complength, compstart) = self.findLongestComplement(miRNA, len(miRNA) - params[9], len(miRNA), seq, start - params[10], start - params[11])
                    score += (params[12] * complength)

                    (comp, complength, compstart) = self.findLongestComplement(miRNA, 0, params[13], seq, stop + params[14], stop + params[15])
                    score += (params[16] * complength)                

        return score
