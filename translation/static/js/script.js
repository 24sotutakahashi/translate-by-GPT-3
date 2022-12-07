function copyToClipboard() {
    // コピー対象をJavaScript上で変数として定義する
    var copyTarget = document.getElementById("copyTarget");
    // コピー対象のテキストを選択する
    copyTarget.select();
    // 選択しているテキストをクリップボードにコピーする
    document.execCommand("Copy");

    //discordへ飛ぶ
    if (!alert("コピーできました！" + "Discordに移動します!")) {
        window.location = "https://discord.com/"
    }
}
