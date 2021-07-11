from common.search import  ImageSearcher
from common.learn import LearnImage

def crawling():
  searcher = ImageSearcher()
  searcher.scraping("堀江由衣")
  searcher.scraping("田村ゆかり")
  searcher.scraping("水樹奈々")

def learn():
  learnmodel = LearnImage()
  learnmodel.learn()

if __name__ == "__main__":
  # crawling()
  learn()