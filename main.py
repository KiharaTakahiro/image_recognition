from common.search import  ImageSearcher


def main():
  searcher = ImageSearcher()
  searcher.scraping("堀江由衣")
  searcher.scraping("田村ゆかり")
  searcher.scraping("水樹奈々")

if __name__ == "__main__":
  main()