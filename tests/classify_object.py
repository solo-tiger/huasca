
import huasca

assert 'golden_retriever' in [x[1] for x in huasca.classify.object('tests/images/dog01.jpg',verbose=False)] , "misclassified dog"
