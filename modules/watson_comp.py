import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, RelationsOptions

if __name__ == '__main__':
    authenticator = IAMAuthenticator('U2czwsAjyWiIbO9YKidTQZYm2iNRxGAIjniDWFWoihEA')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2869ca74-f6c0-46f8-812d-f44c0cdc2a7a')

    # response = natural_language_understanding.analyze(
    #     url='www.ibm.com',
    #     features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()

    # print(json.dumps(response, indent=2))

    # keywords
    response = natural_language_understanding.analyze(
    url='https://www.theguardian.com/world/2017/may/28/merkel-says-eu-cannot-completely-rely-on-us-and-britain-any-more-g7-talks',
    features=Features(
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=2))).get_result()

    print('keywords extract')
    print('\n')
    print(json.dumps(response, indent=2))
    print('\n')

    #concepts
    # response = natural_language_understanding.analyze(
    # text='Goodfellow\'s theory has been questioned, however, because the plane made two other sharp turns that would\'ve been impossible if the pilots were unconscious.',
    # features=Features(concepts=ConceptsOptions(limit=3))).get_result()
    # print('concepts extract')
    # print('\n')
    # print(json.dumps(response, indent=2))
    # print('\n')

