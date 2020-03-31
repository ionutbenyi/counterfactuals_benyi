import spacy
import json


if __name__ == '__main__':
    articles =[]
    count_facts_total = 0
    count_facts_found = 0
    count_counterfacts_total = 0
    count_counterfacts_found = 0
    fake_truths = 0
    fake_fakes = 0

    nlp = spacy.load("en_core_web_lg")

    with open('data/articles.txt') as inp_data:
        articles = json.load(inp_data)
    for headline in articles:
        total_sites_nr = 0
        good_sites_nr = 0
        total_similarity = 0
        for article_text in headline["texts"]:
            total_sites_nr += 1
            similarity_value = 0
            if len(article_text["content"]) < 1000000:
                doc1 = nlp(headline["sentence"])
                doc2 = nlp(article_text["content"])
                if doc2.vector_norm:
                    similarity_value = doc1.similarity(doc2)
            
        
            if similarity_value >= 0.95:
                good_sites_nr += 1
            if headline["sentence"] in article_text["content"]:
                good_sites_nr = 10
                similarity_value = 1.0

            print("SIMILARITY = "+str(similarity_value)+" - "+str(article_text["source"]))
            total_similarity += similarity_value
            
        avg_sim = 0.0
        if total_sites_nr !=0:
            avg_sim = total_similarity/total_sites_nr
        

        if headline["truth_flag"] == "0":
            count_counterfacts_total += 1
        else:
            count_facts_total += 1

        if good_sites_nr >= (total_sites_nr/2):
        #if avg_sim > 0.94:
            print(headline["sentence"]+" is FACT - "+str(headline["truth_flag"]))
            count_facts_found += 1
            if str(headline["truth_flag"]) == "0":
                fake_truths += 1
                count_facts_found -= 1
            
        else:
            print(headline["sentence"]+" is COUNTERFACT - "+str(headline["truth_flag"]))
            count_counterfacts_found += 1
            if str(headline["truth_flag"]) == "1":
                fake_fakes += 1
                count_counterfacts_found -= 1
        # print("AVG SIMILARITY = "+str(avg_sim))        
    print("Counterfacts: total="+str(count_counterfacts_total)+", found="+str(count_counterfacts_found))
    print("Facts: total="+str(count_facts_total)+", found="+str(count_facts_found))
    print("Fake truths: "+str(fake_truths)+", fake fakes: "+str(fake_fakes))