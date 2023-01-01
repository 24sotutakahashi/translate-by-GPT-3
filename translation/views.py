from base64 import urlsafe_b64decode
import json
import openai

import deepl
import requests
from django.http import HttpResponse
from django.template import loader

from .forms import TranslationForm

from .settings_secret import *

# 朝日APIの認証コードと設定
asahi_api_key = asahi_api_key_from_secret
endpoint = "https://clapi.asahi.com/abstract"

# 何文字ずつ区切って要約するか。200〜2000の整数。デフォルトは500。
length = 200

# 要約の際に、元の文章を自動的に段落分けをするか否か
auto_paragraph = True


# deepLの認証コードと設定
deepL_auth_key = deepL_auth_key_from_secret
translator = deepl.Translator(deepL_auth_key)

# openaiの認証コード
openai.api_key = openai_api_key_from_secret


def Translation_and_Summary(request):

    # 翻訳結果を入れる変数を準備
    translation_results = ""

    # 英訳した要約を入れるリストを準備
    ENG_SUM = []

    # 生成した画像のURLを入れるリストを用意
    result_urls = []

    if request.method == "POST":
        # 「要約と英訳！」ボタンを押したときの、フォームの内容を取得
        form = TranslationForm(request.POST)

        # 英訳した要約を入れるリストの中身をリセット
        ENG_SUM.clear()

        # バリデーションチェック
        if form.is_valid():
            # フォームの内容を取得
            sentence = form.cleaned_data['sentence']

            # フォームの内容を、朝日新聞APIのためにJSON に変換
            input_json = json.dumps(
                {"text": sentence, "length": length, "auto_paragraph": auto_paragraph})

            # リクエストの書式と認証方式を指定
            headers = {"accept": "application/json",
                       "Content-Type": "application/json",
                       "x-api-key": asahi_api_key}

            # リクエスト送信
            response = requests.post(endpoint, input_json, headers=headers)

            # エンドポイントからレスポンスあった時の処理
            if response.status_code == 200:
                # 結果をresultに入れる
                result = response.json()["result"]

                # resultを1つずつ英訳
                for i in result:
                    English_Summary = translator.translate_text(
                        i, target_lang="EN-US")
                    # リストに追加
                    ENG_SUM.append(English_Summary.text)

                # リストにある英訳した要約を、1文にする。
                translation_results = ",".join(ENG_SUM)

                # 英訳した要約を基に、画像生成のURLを取得
                result_urls = Get_Image_URL(translation_results)
            else:
                pass
    else:
        form = TranslationForm()

    template = loader.get_template('translation/index.html')

    context = {
        'form': form,
        'translation_results': translation_results,
        'result_urls': result_urls
    }
    return HttpResponse(template.render(context, request))


# 引数を基に画像を生成し、そのURLのリストを返す
def Get_Image_URL(English_Summary):
    # 戻り値を複数返すためのリストの箱を作る
    URL_List = []
    # リストの中身をリセット
    URL_List.clear()
    # 生成する画像の数を指定
    Number_of_Images = 2

    dalle = openai.Image.create(
        prompt=English_Summary,
        n=Number_of_Images,
        size="1024x1024"
    )
    for i in range(Number_of_Images):
        # dalleAPIからの結果を取得（辞書型）
        IMG_URL_Dict = dalle["data"][i].values()
        # 辞書型からリスト型へ変換
        IMG_URL_List = list(IMG_URL_Dict)
        # 変換したURLの中身を、URL_Listに追加
        URL_List.append(IMG_URL_List[0])

    return URL_List
