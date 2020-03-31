import argparse
from contextlib import ExitStack
from modules.dependency_parser import DependencyParser
from modules.constituency_parser import ConstituencyParser
from modules.ner_parser import NERParser
from modules.web_scraper import WebScraper

good_node_types = [
    'root', 'nsubjpass', 'auxpass', 'advcl', 'poss', 'nsubj', 'dobj', 
    'rcmod', 'num', 'amod', 'ccomp', 'pobj', 'tmod', 'prt', 'advmod', 'dep'
]
bad_node_types = ['aux', 'punct', 'mark', 'det', 'cop', 'prep', 'possesive', 'xcomp']

keywordsRes = []

def find_keywords(element):
    if element.get('children'):
        for child in element.get('children'):
            if child.get('nodeType') in good_node_types:
                keywordsRes.append(child.get('word'))
            find_keywords(child)


def remove_adj_phrases(element, sent2):
    if element.get('nodeType') == 'S':
        for c in element.get('children'):   
            if c.get('nodeType') == 'S':
                remove_adj_phrases(c, sent2)
            elif c.get('nodeType') == 'ADJP':
                sent2=""
            else:
                sent2 += " " + c.get('word')
        return sent2
    else:
        return element.get('word')

if __name__ == '__main__':

    output_file = None
    print_to_console = True
    dependencyParser = DependencyParser(output_file, print_to_console)
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

    new_batch_data = []
    #delete ADJPs
    const_parser = ConstituencyParser(output_file, print_to_console)
    for bd in batch_data:
        sentence = bd.get('sentence')
        const_parsing_result = const_parser.parse_sentence(sentence)
        const_tree_start_element = const_parsing_result.get('hierplane_tree').get('root')
        
        #sentence without ADJPs:
        #new_sentence=remove_adj_phrases(const_tree_start_element,"")
        new_batch_data.append({'sentence': sentence})

    dpBatch = dependencyParser.parse_batch(new_batch_data)

    for i in range( len(dpBatch) ):
        d = dpBatch[i]
        d1 = batch_data[i]
        keywordsRes = []
        if d.get('hierplane_tree').get('text') != d1.get('sentence'):
            print(d1.get('sentence'))
            print(d.get('hierplane_tree').get('text'))
        else: 
            print(d.get('hierplane_tree').get('text'))

        root = d.get('hierplane_tree').get('root')

        if root.get('nodeType') in good_node_types:
            keywordsRes.append(root.get('word'))

        find_keywords(root)
        print(keywordsRes)

        scraper = WebScraper()
        url_list = scraper.search_for_link(keywordsRes)
        print(url_list)
        print("\n")
        print(d.get('hierplane_tree'))
        print("\n")
        