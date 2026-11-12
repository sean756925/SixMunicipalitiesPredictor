# Supabase 永久瀏覽計數設定

網站只會保存「台北時區日期」與「該日累計次數」，不保存 IP、姓名、Cookie、瀏覽器指紋或其他個人資料。

## 1. 建立 Supabase 專案

1. 登入 https://supabase.com/dashboard
2. 建立一個免費專案。
3. 進入 **SQL Editor**，建立 New query。
4. 貼上並執行 `supabase/page_view_counter.sql` 的完整內容。

執行後，Table Editor 會出現 `page_view_daily`。一般匿名角色沒有直接讀寫資料表的權限，只能執行安全的累加函式。

## 2. 取得連線設定

進入 Supabase 專案的 **Settings → API**（新版介面也可能顯示為 **Connect → App Frameworks**），取得：

- Project URL：`https://xxxxx.supabase.co`
- anon/public key：請使用 anon key，不要使用 `service_role` key

## 3. 設定 Streamlit Secrets

到 Streamlit Community Cloud 的 App 管理畫面：

**App settings → Secrets**

貼上：

```toml
[supabase]
url = "https://xxxxx.supabase.co"
anon_key = "你的 anon public key"
```

儲存後 Streamlit 會重新啟動。第一個新 Session 會顯示永久計數 `1`；之後更新 GitHub 或重新部署，數字不會歸零。

## 4. 驗證

1. 用無痕視窗開啟公開網站，記下累計與今日次數。
2. 在同一分頁操作篩選器，次數不應增加。
3. 開另一個無痕 Session，累計與今日應各增加一次。
4. 在 Supabase Table Editor 查看 `page_view_daily`，每天只會有一列彙總數字。

若 Supabase 暫時無法連線，網站仍會正常載入，只會暫時隱藏瀏覽數。
