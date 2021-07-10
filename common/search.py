import requests
import urllib.request
import time
import json
import os

class ImageSearcher():
  """ 画像検索のためのクラス
  """
  def __init__(self, dest_path="./img" ,max_page_num=20, img_num_per_page=20, sleep_sec=3, time_out=5):
    self.__max_page_num = max_page_num
    self.__img_num_per_page = img_num_per_page
    self.__sleep_sec = sleep_sec
    self.__all_img_src_list = []
    self.__dest_path = dest_path
    self.__time_out = time_out

  def scraping(self, search_word):
    url = f"https://search.yahoo.co.jp/image/search?p={search_word}&ei=UTF-8&b="
    self.__search_word = search_word
    page_list = [f'{url}{page*self.__img_num_per_page+1}' for page in range(self.__max_page_num)]
    # HACK: ここはきれいに書けそう上のリスト内包表記が冗長のため
    print('ページ検索')
    for page in page_list:
      try:
        print(f'search_word: {search_word} page: {page}')
        img_src_list = self.__get_img_src_list(page)
        self.__all_img_src_list.extend(img_src_list)
      except:pass
    self.__download_img()

  def __download_img(self):
    save_dir = f'{self.__dest_path}/{self.__search_word}'
    if not os.path.exists(save_dir):
       print('ディレクトリ作成')
       print(f'save_dir: {save_dir}')
       os.makedirs(save_dir)
    print('ダウンロード')
    for i, src in enumerate(self.__all_img_src_list):
      dist_path = f'{save_dir}/image_{i}.jpg'
      print(f'dist_path: {dist_path} src: {src}')
      time.sleep(self.__sleep_sec)
      try:
        with urllib.request.urlopen(src, timeout=self.__time_out) as data:
            img = data.read()
            with open(dist_path, 'wb') as f:
                f.write(img)
                print('書き込み成功')
      except: print(f'書き込み失敗: src: {src}')
    # ダウンロードが完了した時点でクリア
    self.__all_img_src_list = []

  def __get_img_src_list(self, url):
      response = requests.get(url)
      webtext = response.text

      start_word='<script>__NEXT_DATA__ = '
      start_num = webtext.find(start_word)
      webtext_start = webtext[start_num + len(start_word):]
      end_word = ';__NEXT_LOADED_PAGES__='

      end_num = webtext_start.find(end_word)
      webtext_all = webtext_start[:end_num]
      web_dic = json.loads(webtext_all)
      img_src_list = [img['original']['url'] for img in web_dic["props"]["initialProps"]["pageProps"]["algos"]]

      return img_src_list