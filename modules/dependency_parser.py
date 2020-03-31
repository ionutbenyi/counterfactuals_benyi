from allennlp.predictors import Predictor 
from allennlp.models.archival import load_archive

class DependencyParser:
    def __init__(self, output_file, print_to_console_flag):
        self.predictor = Predictor.from_path(r"E:\Facultate\An 4\Licenta\Common Inference NLP\dependency parsing resources\biaffine-dependency-parser-ptb-2018.08.23.tar.gz")
        self.output_file = output_file
        self.print_to_console_flag = print_to_console_flag

    def _run_predictor_sentence(self, sentence):
        value = self.predictor.predict(sentence)
        r = value
        newR = {
                'words': r.get('words'), 
                'pos': r.get('pos'), 
                'predicted_dependencies': r.get('predicted_dependencies'), 
                'predicted_heads': r.get('predicted_heads'),
                'hierplane_tree': {
                    'text': r.get('hierplane_tree').get('text'),
                    'root': r.get('hierplane_tree').get('root')
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
                'words': r.get('words'), 
                'pos': r.get('pos'), 
                'predicted_dependencies': r.get('predicted_dependencies'), 
                'predicted_heads': r.get('predicted_heads'),
                'hierplane_tree': {
                    'text': r.get('hierplane_tree').get('text'),
                    'root': r.get('hierplane_tree').get('root')
                }
            }
            compressedRes.append(newR)

        return compressedRes
        # for model_input, output in zip(batch_data, results):
        #     string_output = self.predictor.dump_line(output)
        #     if self.print_to_console_flag:
        #         print("input: ", model_input)
        #         print("batch data prediction: ", string_output)
        #         return string_output
        #     if self.output_file:
        #         self.output_file.write(string_output)
        #         return "Written in " + self.output_file

    def parse_sentence(self, sentence):
        return self._run_predictor_sentence(sentence)

    def parse_batch(self, batch):
        return self._run_predictor_batch(batch)