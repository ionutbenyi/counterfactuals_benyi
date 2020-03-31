from allennlp.predictors import Predictor 
from allennlp.models.archival import load_archive

class ConstituencyParser:
    def __init__(self, output_file, print_to_console_flag):
        self.predictor = Predictor.from_path(r"E:\Facultate\An 4\Licenta\Common Inference NLP\constituency parsing resources\elmo-constituency-parser-2018.03.14.tar.gz")
        self.output_file = output_file
        self.print_to_console_flag = print_to_console_flag

    def _run_predictor_sentence(self, sentence):
        value = self.predictor.predict(sentence)
        r = value
        newR = {
                'tokens': r.get('tokens'), 
                'pos_tags': r.get('pos_tags'), 
                'hierplane_tree': {
                    'text': r.get('hierplane_tree').get('text'),
                    'root': r.get('hierplane_tree').get('root'),
                    'trees': r.get('hierplane_tree').get('trees')
                }
            }
        return newR
    
    def _run_predictor_batch(self, batch_data):
        if(len(batch_data) == 1):
            result = self.predictor.predict_json(batch_data[0])
            results = [result]
        else:
            results = self.predictor.predict_batch_json(batch_data)

        compressedRes = []
        for r in results:
            newR = {
                'tokens': r.get('tokens'), 
                'pos_tags': r.get('pos_tags'), 
                'hierplane_tree': {
                    'text': r.get('hierplane_tree').get('text'),
                    'root': r.get('hierplane_tree').get('root'),
                    'trees': r.get('hierplane_tree').get('trees')
                }
            }
            compressedRes.append(newR)

        return compressedRes

    def parse_sentence(self, sentence):
        return self._run_predictor_sentence(sentence)

    def parse_batch(self, batch):
        return self._run_predictor_batch(batch)