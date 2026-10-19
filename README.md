# TFDA 食品邊境不合格監測 V2
1. 建立 GitHub Public Repository。
2. 上傳本資料夾全部檔案。
3. Settings → Pages → Deploy from a branch → main → /root。
4. Actions → Daily TFDA Sync → Run workflow，先手動執行一次。
5. GitHub Pages 網站即可讀取 data.json。
6. Workflow 每日 UTC 00:15（台灣約 08:15）自動檢查。
TFDA 資料集目前標示更新頻率為每7日，因此每日更新是每日檢查，不代表每天必有新案件。
