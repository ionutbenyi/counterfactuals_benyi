
class StatisticsInterpreter:

    def interpret_results(self, true_positive, false_positive, true_negative, false_negative):
        # confusion matrix:
        # compute precision & recall
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)

        print("Precision = "+ str(precision))
        print("Recall = "+str(recall))