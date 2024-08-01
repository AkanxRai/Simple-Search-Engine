from crawler import crawl_web, compute_ranks
from search import lucky_search
import pickle
import web

class LuckySearch(object):
    def GET(self, path):
        query = path.lstrip('/')
        if query:
            result = lucky_search(index, ranks, query)
            if result:
                return f"Lucky search result for '{query}': {result}"
            else:
                return f"No results found for '{query}'"
        else:
            return "Please provide a search query."

fname = 'corpus.pkl'
try:
    with open(fname, 'rb') as fin:
        index, graph = pickle.load(fin)
        ranks = compute_ranks(graph)
except IOError as e:
    print("Cannot open web corpus: recrawling...")
    index, graph = crawl_web("https://books.toscrape.com/index.html")
    ranks = compute_ranks(graph)
    with open(fname, 'wb') as fout:
        pickle.dump((index, graph), fout)
        print(f"Successfully wrote pickle into {fname}")

urls = (
    '/(.*)', 'LuckySearch'
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
