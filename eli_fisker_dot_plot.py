import strategy_template


class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        # Title, author of the submission
        self.title_ = "[Strategy Market] [Switch] Dot plot"
        self.author_ = "Eli Fisker"

        # URL where the strategy was initially submitted
        self.url_ = ("https://getsatisfaction.com/eternagame/topics/"
                     "-strategy-market-switch-dot-plot")

        # Default strategy parameters
        self.default_params_ = [5.0, 3.0, 5.0, 1.0, 5.0, 1.0]

        # Number of lines of code used to implement the strategy
        self.code_length_ = 40

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False

    # Take the longer dotplot, compare all its values to the other plot
    # Where it differs, tally up a count and how much it differs by
    def amountMatch(plot1, plot2):

        # Make sure plot1 is the longer plot and plot2 is the shorter one
        # If same length, then don't do anything
        if len(plot1) < len(plot2):
            plot2, plot1 = plot1, plot2

        count = 0
        diff = 0

        for i in range(0, len(plot1)):

            prob_plot1 = plot1[i][2]
            prob_plot2 = 0

            for j in range(0, len(plot2)):
                # Base pairs match up, comparing same bases
                if plot2[j][0] == plot1[i][0] and plot2[j][1] == plot2[i][1]:
                    prob_plot2 = plot2[j][2]
                    break

            if prob_plot2 != prob_plot1:
                count += 1
                diff += abs(prob_plot2 - prob_plot1)

        return (count, diff)

    def score(self, design, params):

        score = 100

        # Strategy only applies to MS2 switches
        if "miRNA" in design['labtitle']:
            score = eterna_utils.UNSCORABLE
        else:

            # To determine if a switch is partial moving or full moving,
            # look at the aptamer binding spots. If 50% of them or less
            # move (one stack) then it is only partially moving. Otherwise,
            # it is fully moving.

            # What the bases binding occured in were, and which state (1 or 2)
            # the binding occured in.
            bases = design['site']
            state = str(design['on_state'])

            switchbp = 0

            for base in bases:
                if design['secstruct' + state][base] == '(':
                    pair1 = design['sequence'][design['pairmap1'][base]]
                    pair2 = design['sequence'][design['pairmap2'][base]]
                    if pair1 != pair2:
                        switchbp += 1

            if float(switchbp) / len(bases) <= 0.5:
                # Partial switch
                # U = upper, L = lower
                diff = amountMatch(design['dotplot1u'], design['dotplot2l'])[1]

                # If the difference was small:
                # state1 top has well match with state1 bottom
                if diff < params[0]:
                    score += params[1]

                diff = amountMatch(design['dotplot2l'], design['dotplot1l'])[1]

                # If the difference was small:
                # state2 is more present in state1 prediction
                if diff < params[2]:
                    score -= (diff * params[3])

            else:
                # Full moving switch
                # U = upper, L = lower
                diff = amountMatch(design['dotplot2l'], design['dotplot1u'])[1]
                if diff < params[4]:
                    score += params[5]

        return score
