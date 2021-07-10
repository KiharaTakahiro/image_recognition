import requests
import urllib.request
import time
import json
import os

class ImageSearcher():
  """ 画像検索のためのクラス
  """
  def __init__(self, dest_path="./img" ,max_page_num=20, img_num_per_page=20, sleep_sec=3, time_out=5):
    """ コンストラクタ

    Args:
        dest_path (str): 画像の保存先. Defaults to "./img".
        max_page_num (int): クローリングするページ数. Defaults to 20.
        img_num_per_page (int): 1ページ内の検索数. Defaults to 20.
        sleep_sec (int): 検索間隔(あまり早く設定すると高負荷になるかも自己責任でお願いします。). Defaults to 3.
        time_out (int): 取得できない時に何秒でタイムアウトにするか. Defaults to 5.
    """
    self.__max_page_num = max_page_num
    self.__img_num_per_page = img_num_per_page
    self.__sleep_sec = sleep_sec
    self.__all_img_src_list = []
    self.__dest_path = dest_path
    self.__time_out = time_out

  def scraping(self, search_word):
    """ スクレイピングを行う処理

    Args:
        search_word (str): 検索キーワード
    """

    url = f"https://search.yahoo.co.jp/image/search?p={search_word}&ei=UTF-8&b="
    self.__search_word = search_word
    print('ページ検索')
    for page in range(self.__max_page_num):
      try:
        print(f'search_word: {search_word} page: {page}')
        img_src_list = self.__get_img_src_list(f'{url}{page*self.__img_num_per_page+1}')
        self.__all_img_src_list.extend(img_src_list)
      except:pass
    self.__download_img()

  def __download_img(self):
    """ 画像をダウンロードする処理
    """
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
    """ ページから画像を選択して取得する

    Args:
        url (string): 対象url

    Returns:
        list: 画像情報リスト
    """
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