from search import get_all_links, add_page_to_index, get_page, make_hashtable

def crawl_web(seed):
    to_crawl = set([seed])
    crawled = set()
    depth = 0
    next_depth = []
    index = {}
    graph = {}
    while to_crawl:
        page = to_crawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page]=outlinks
            to_crawl.union(outlinks)
            crawled.add(page)
    return index, graph
def compute_ranks(graph):
    d = 0.8
    numloops = 10
    npages = len(graph)
    ranks = {}
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

if __name__ == '__main__':
    import pickle

    corpus = crawl_web("https://books.toscrape.com/index.html")
    fname = 'corpus.pkl'

    try:
        with open(fname, 'wb') as fout:
            pickle.dump(corpus, fout)
            print("Successfully wrote pickle into " + fname)
    except IOError as e:
        print("Cannot write into corpus:" + str(e))
