from modules.ner_parser import NERParser
from modules.web_scraper import WebScraper
from modules.oie_parser import OIEParser
from allennlp.interpret.saliency_interpreters.simple_gradient import SimpleGradient
from allennlp.interpret.saliency_interpreters.saliency_interpreter import SaliencyInterpreter

from allennlp.predictors import Predictor 

if __name__ == '__main__':

    output_file = None
    print_to_console = True

    nerParser = NERParser(output_file, print_to_console)
    print("--------------------------Dependency parsing - batch--------------------------")
    batch_data =  [
        {'sentence': 'If you snore loudly and feel tired even after a full night\'s sleep, you might have sleep apnea.'},
        {'sentence': 'Goodfellow\'s theory has been questioned, however, because the plane made two other sharp turns that would\'ve been impossible if the pilots were unconscious.'},
        {'sentence': 'In addition, the computer users often continued to work without taking breaks, but in other circumstance, if the users took the breaks it would have relieved the additional tension and reduced the risk of developing repetitive strain injury.'},
        {'sentence': 'Unable to stay completely quiet on the issue, Merkel said last week Britain would lose out if it left the EU.'},
        {'sentence': 'The leak could have been stopped the same hour it was discovered if the well had a working shut-off valve.'},
        {'sentence': 'Ceramides can also kill cells if their levels become high and can bring on inflammatory responses.'},
        {'sentence': 'If the original electronic calculators were only able to multiply single digit numbers, nobody would have bought anything from Texas Instruments in those early days.'}
    ]

    #NER
    pred = Predictor.from_path(r"E:\Facultate\An 4\Licenta\benyi_coin_nlp\ner parsing resources\ner-model-2018.12.18.tar.gz")
    simple_gradient = SimpleGradient(pred)

    print("From raw sentences, simple NER gradient: ")
    print('\n')
    for i in range( len(batch_data) ):
        print(batch_data[i]['sentence'])
        d = batch_data[i]
        d_gradient = simple_gradient.saliency_interpret_from_json(d)
        print(d_gradient)

    print('\n')

    #OIE
    oie_parser = OIEParser(output_file, print_to_console)
    oie_batch = oie_parser.parse_batch(batch_data)
    print('OIE parsing')
    for i in range( len(oie_batch) ):
        print(batch_data[i]['sentence'])
        print(oie_batch[i])

    print('\n')
    
