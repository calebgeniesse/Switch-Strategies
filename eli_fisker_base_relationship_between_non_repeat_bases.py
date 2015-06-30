import strategy_template

class Strategy(strategy_template.Strategy):
    def __init__(self):

        strategy_template.Strategy.__init__(self)

        self.title_ = "[Strategy Market] [Switch] Base relationship between non repeat bases" # Title of the strategy submission
        self.author_ = "Eli Fisker" # Author of the strategy submisison

        # URL where the strategy was initially submitted
        self.url_ = "https://getsatisfaction.com/eternagame/topics/-strategy-market-switch-base-relationship-between-non-repeat-bases"

        # Default strategy parameters
        # The first few are for percent of single bases, afterwards it is rewards, then penalties
        self.default_params_ = [0.65, 0.55, 0.08, 
                                1.0, 1.0, 1.0, 1.0, 1.0, 
                                -1.0, -1.0
                                ]

        # Number of lines of code used to implement the strategy
        # Function headers not included in the count
        # Long if statements split into multiple lines only counts as 1 line
        self.code_length_ = 23

        self.publishable_ = True
        self.denormalized_ = True
        self.comprehensive = False
    
    def percentDifference(self, value1, value2):
        if value1 == value2: return 0 # also takes care of when value1 == value2 == 0
        return (( float(abs(value1 - value2)) /( float(value1 + value2) / 2))*100)

    def score(self, design, params):

        singleA = singleU = singleG = singleC = 0
        score = 100

        seq = design['sequence']
        seqlength = len(seq)
        seq_range = range(0, seqlength)

        for i in seq_range:

            if (i > 0 and seq[i] != seq[i-1]) and (i < seqlength - 1 and seq[i] != seq[i+1]):
                if seq[i] == "A": singleA += 1
                elif seq[i] == "U": singleU += 1
                elif seq[i] == "G": singleG += 1
                elif seq[i] == "C": singleC += 1

        percentsingles = float(singleA + singleG + singleC + singleU) / seqlength

        if singleA + singleU > singleC + singleG: score += params[3]
        if singleA > singleU: score += params[4]
        if singleU > singleG: score += params[5]
        if singleG > singleC: score += params[6]

        # Percent difference
        # Defined as ABS(value1 - value2) / ( (value1 + value2) / 2) * 100

        if (self.percentDifference(singleA, singleU) <= params[2] and 
            self.percentDifference(singleA, singleG) <= params[2] and 
            self.percentDifference(singleA, singleC) <= params[2] and
            self.percentDifference(singleU, singleG) <= params[2] and
            self.percentDifference(singleU, singleC) <= params[2] and
            self.percentDifference(singleG, singleC) <= params[2]):
            score += params[7]

        if("Same State" in design['puztitle'] and (params[0] < percentsingles)): score += params[8]
        elif( "Exclusion" in design['puztitle'] and (params[1] < percentsingles)): score += params[9]

        return score