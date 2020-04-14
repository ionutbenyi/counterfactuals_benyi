from allennlp.predictors import Predictor 
from allennlp.models.archival import load_archive
import os

class OIEParser:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../oie parsing resources/openie-model.2018-08-20.tar.gz')
        self.predictor = Predictor.from_path(filename)

    def _run_predictor_sentence(self, sentence):
        value = self.predictor.predict(sentence)
        return value

    def parse_sentence(self, sentence):
        tokenized_sentence = self._run_predictor_sentence(sentence)
        
        #build end vector:
        result_vector = []
        for word in tokenized_sentence["words"]:
            result_vector.append("")
        
        for verb in tokenized_sentence["verbs"]:
            tags = verb["tags"]

            t_count = 0
            for t in tags:
                if t != "O" and result_vector[t_count] == "":
                    result_vector[t_count] = tokenized_sentence["words"][t_count]
                t_count += 1

        final_string = ""
        for word in result_vector:
            if word != "" and word[0] != "'":
                final_string = final_string + word + " " 
                
        return final_string