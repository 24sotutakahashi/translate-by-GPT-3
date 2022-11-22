import json
import time

import deepl
import requests
from django.http import HttpResponse
from django.template import loader

from .forms import TranslationForm

# Create your views here.

# 朝日APIの設定
endpoint = "https://clapi.asahi.com/abstract"

length = 200  # 何文字ずつ区切って要約するか。200〜2000の整数。デフォルトは500。
auto_paragraph = True  # 自動的に段落分けをするか否か

auth_key = "a0d905ea-e7d5-0dbb-2d5c-59746d2186ec:fx"
# deepLの認証コード
translator = deepl.Translator(auth_key)


def index(request):
    """
    翻訳画面
    """

    # 翻訳結果
    translation_results = ""

    if request.method == "POST":
        # 翻訳ボタン押下時

        form = TranslationForm(request.POST)

        # バリデーションチェック
        if form.is_valid():

            # 翻訳文を取得
            sentence = form.cleaned_data['sentence']

            # sentenceを、朝日新聞APIのためにJSON に変換
            input_json = json.dumps(
                {"text": sentence, "length": length, "auto_paragraph": auto_paragraph})

            # リクエストの書式と認証方式を指定
            headers = {"accept": "application/json",
                       "Content-Type": "application/json",
                       "x-api-key": "q5DfnnSvgk2CdL195wc8d4ZqdQT90OEY4bvCS44H"}

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
