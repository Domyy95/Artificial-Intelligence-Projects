import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    model = {}   

    linked_pages = corpus[page]
    
    prob_linked = damping_factor / len(linked_pages) if len(linked_pages) > 0 else 0
    prob_all = (1-damping_factor) / len(corpus)

    for page in corpus:
        if page in linked_pages:
            model[page] = prob_linked + prob_all
        else:
            model[page] = prob_all

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_ranks = {}

    for page in corpus:
        page_ranks[page] = 0

    actual_page = random.sample(list(corpus),1)
    page_ranks[actual_page[0]] += 1
    for i in range(0,n-1):
        tranx = transition_model(corpus,actual_page[0],damping_factor)
        sample = random.choices(list(tranx.keys()),k=1,weights = list(tranx.values()))
        actual_page = sample
        page_ranks[actual_page[0]] += 1

    page_ranks.update((x, y/n) for x, y in page_ranks.items())
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_ranks = {}
    N = len(corpus.keys())

    for page in corpus.keys():
        page_ranks[page] = float(1/N)


    stop = False
    const_term = float((1 - damping_factor ) / N)

    while not stop:
        stop = True
        topr = {}

        for i in page_ranks.keys():
        	temp = page_ranks[i]

        	topr[i] = const_term
        	for page,link in corpus.items():
        		if i in link:
        			topr[i] += float(damping_factor*page_ranks[page] / len(link))

        	if abs(temp - topr[i]) > 0.001:
        		stop = False

        for i in page_ranks.keys():
        	page_ranks[i] = topr[i]

    return page_ranks


if __name__ == "__main__":
    main()
