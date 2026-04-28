# 旅遊規劃系統 路由與頁面設計 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (行程列表)** | GET | `/` | `index.html` | 顯示所有已建立的旅遊行程 |
| **建立新行程頁面** | GET | `/planner/new` | `planner_new.html` | 顯示建立新行程的表單 |
| **建立行程操作** | POST | `/planner/new` | — | 接收表單，存入 DB，重導向至行程規劃頁 |
| **檢視行程規劃頁面** | GET | `/planner/<int:id>` | `planner_view.html` | 顯示特定行程詳情，包含天數與景點列表 |
| **新增景點** | POST | `/planner/<int:id>/add_place` | — | 接收表單，新增景點至特定天數，重導向回規劃頁 |
| **刪除景點** | POST | `/planner/destination/<int:dest_id>/delete` | — | 刪除單一景點，重導向回規劃頁 |
| **更新景點排序 (AJAX)**| POST | `/api/planner/update_order` | — | 接收 JSON 陣列，更新 DB 中的 `order_index` |
| **檢視預算頁面** | GET | `/budget/<int:id>` | `budget_view.html` | 顯示特定行程的各項預估花費與總計 |
| **新增預算項目** | POST | `/budget/<int:id>/add` | — | 接收表單，新增一筆預算，重導向回預算頁 |
| **刪除預算項目** | POST | `/budget/item/<int:item_id>/delete` | — | 刪除單一預算項目，重導向回預算頁 |
| **刪除整個行程** | POST | `/planner/<int:id>/delete` | — | 刪除行程(及關聯景點、預算)，重導向回首頁 |
| **匯出行程 (PDF)** | GET | `/export/<int:id>/pdf` | — | 產生該行程的 PDF (暫為未來進階功能預留) |

## 2. 每個路由的詳細說明

### 首頁 (`/`)
- **輸入**：無
- **處理邏輯**：呼叫 `Itinerary.get_all()` 取得列表。
- **輸出**：渲染 `index.html`，傳遞 `itineraries` 資料。

### 建立新行程頁面 (`GET /planner/new`)
- **輸出**：渲染 `planner_new.html` 顯示表單。

### 建立行程操作 (`POST /planner/new`)
- **輸入**：表單欄位 `title`, `start_date`, `end_date`。
- **處理邏輯**：呼叫 `Itinerary.create()`。
- **輸出**：成功後重導向至 `GET /planner/<id>`。

### 檢視行程規劃頁面 (`GET /planner/<int:id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Itinerary.get_by_id(id)`，若不存在則回傳 404。同時呼叫 `Destination.get_by_itinerary_and_day(...)` 取出各天景點。
- **輸出**：渲染 `planner_view.html`，傳遞 `itinerary` 與 `destinations` 資料。

### 新增景點 (`POST /planner/<int:id>/add_place`)
- **輸入**：URL 參數 `id`，表單欄位 `name`, `day_number`, `notes`。
- **處理邏輯**：呼叫 `Destination.create()`。
- **輸出**：重導向至 `GET /planner/<id>`。

### 更新景點排序 (`POST /api/planner/update_order`)
- **輸入**：JSON 陣列（包含各 `destination_id` 與新的 `order_index` 及 `day_number`）。
- **處理邏輯**：迴圈呼叫 `Destination.update_order()` 更新順序。
- **輸出**：回傳 JSON `{"status": "success"}`，若失敗則回傳 400 錯誤。

### 檢視預算頁面 (`GET /budget/<int:id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Itinerary.get_by_id(id)`，並呼叫 `Budget.get_by_itinerary(id)` 取得該行程所有預算項目並加總。
- **輸出**：渲染 `budget_view.html`，傳遞 `itinerary`, `budgets`, `total_amount`。

### 新增預算項目 (`POST /budget/<int:id>/add`)
- **輸入**：URL 參數 `id`，表單欄位 `category`, `amount`, `notes`。
- **處理邏輯**：驗證 `amount` 為數字後，呼叫 `Budget.create()`。
- **輸出**：重導向至 `GET /budget/<id>`。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 中。

1. **`base.html`**：全站共用母版，包含 Header (導覽列)、Footer 與基礎的 CSS 引入。
2. **`index.html`**：首頁，繼承自 `base.html`，顯示行程卡片列表。
3. **`planner_new.html`**：繼承自 `base.html`，顯示「新增旅遊行程」的表單。
4. **`planner_view.html`**：繼承自 `base.html`，顯示單一行程的每日路線，包含新增景點表單，並引入拖曳排序的 JS。
5. **`budget_view.html`**：繼承自 `base.html`，顯示預算清單表格、總計，以及新增預算項目的表單。
