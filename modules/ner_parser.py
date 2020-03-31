from allennlp.predictors import Predictor 
from allennlp.models.archival import load_archive

class NERParser:
    def __init__(self, output_file, print_to_console_flag):
        self.predictor = Predictor.from_path(r"E:\Facultate\An 4\Licenta\benyi_coin_nlp\ner parsing resources\ner-model-2018.12.18.tar.gz")
        self.output_file = output_file
        self.print_to_console_flag = print_to_console_flag

    def _run_predictor_sentence(self, sentence):
        value = self.predictor.predict(sentence)
        return value
    
    def _run_predictor_batch(self, batch_data):
        if(len(batch_data) == 1):
            result = self.predictor.predict_json(batch_data[0])
            results = [result]
        else:
            results = self.predictor.predict_batch_json(batch_data)
        return results
        

    def parse_sentence(self, sentence):
        return self._run_predictor_sentence(sentence)

    def parse_batch(self, batch):
        return self._run_predictor_batch(batch)