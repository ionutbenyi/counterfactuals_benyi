import argparse
from contextlib import ExitStack
from modules.dependency_parser import DependencyParser
from modules.semantic_parser import SemanticParser
from modules.constituency_parser import ConstituencyParser
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-file', type = argparse.FileType('w'), help='path to output file')
    parser.add_argument('--batch-size', type=int, default=1, help="The batch size to use for processing")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    output_file = None
    print_to_console = False
    
    # dependency parsing
    print_to_console = True
    dependencyParser = DependencyParser(output_file, print_to_console)
    #dependencyParsingResult = dependencyParser.parse_sentence("And if you're depressed, you may have a greater chance of developing Type 2 diabetes.")
    dependencyParsingResult = dependencyParser.parse_sentence("A provider may not disclose such information if the patient objects and is not incapacitated.")
    print("--------------------------Dependency parsing - sentence--------------------------")
    print("\n")
    print(dependencyParsingResult)
    #print(json.dumps(dependencyParsingResult, sort_keys=False, indent=4))
    print("\n")

    # batch_data =  [{'sentence': 'Yesterday, James ate some cheese.'},{'sentence': 'She decided not to take the house she had viewed yesterday.'},{'sentence': 'The proportion of PepsiCo’s revenue coming from healthier food and beverages has risen.'}]
    print("--------------------------Dependency parsing - batch--------------------------")
    batch_data =  [{'sentence': 'If you snore loudly and feel tired even after a full night\'s sleep, you might have sleep apnea.'}]
    dpBatch = dependencyParser.parse_batch(batch_data)

    print(dpBatch)
    #print(json.dumps(dpBatch, sort_keys=False, indent=4))
    print("\n")

    #semantic role labelling
    print_to_console = True
    semanticParser = SemanticParser(output_file, print_to_console)
    srlResult = semanticParser.parse_sentence("The quick brown fox jumps over the lazy dog")

    print("--------------------------Semantic role labelling - sentence--------------------------")
    print("\n")
    print(srlResult)
    #print(json.dumps(srlResult, sort_keys=False, indent=4))

    print("\n")

    #constituency parsing
    constParser = ConstituencyParser(output_file, print_to_console)
    constParsingResult = constParser.parse_sentence('In addition, the computer users often continued to work without taking breaks, but in other circumstance, if the users took the breaks itt would have relieved the additional tension and reduced the risk of developing repetitive strain injury.')
    print("--------------------------Consituency parsing - sentence--------------------------")
    print("\n")
    print(constParsingResult)
    print("\n")
    
