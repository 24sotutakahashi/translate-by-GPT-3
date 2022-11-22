import json
import time

import deepl
import requests
from django.http import HttpResponse
from django.template import loader

from .forms import TranslationForm


# 朝日APIの設定
endpoint = "https://clapi.asahi.com/abstract"

# 朝日新聞APIの認証コード
api_key = "q5DfnnSvgk2CdL195wc8d4ZqdQT90OEY4bvCS44H"

# 何文字ずつ区切って要約するか。200〜2000の整数。デフォルトは500。
length = 200

# 自動的に段落分けをするか否か
auto_paragraph = True


# deepLの認証コード
auth_key = "a0d905ea-e7d5-0dbb-2d5c-59746d2186ec:fx"
translator = deepl.Translator(auth_key)


def Translation_and_Summary(request):

    # 翻訳結果
    translation_results = ""

    if request.method == "POST":
        # 「要約と英訳！」ボタンを押したときの、フォームの内容を取得
        form = TranslationForm(request.POST)

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
                       "x-api-key": api_key}

            # リクエスト送信
            response = requests.post(endpoint, input_json, headers=headers)

            # 負荷軽減のために2秒スリープ
            time.sleep(2)

            # エンドポイントからレスポンスあったら結果を表示
            if response.status_code == 200:
                result = response.json()["result"]
                for i in result:
                    # EN-USに翻訳
                    translation_results = translator.translate_text(
                        i, target_lang="EN-US")
            else:
                pass
    else:
        form = TranslationForm()

    template = loader.get_template('translation/index.html')
    context = {
        'form': form,
        'translation_results': translation_results
    }
    return HttpResponse(template.render(context, request))
