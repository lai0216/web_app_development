from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')
api_bp = Blueprint('api', __name__, url_prefix='/api')

@planner_bp.route('/new', methods=['GET', 'POST'])
def new_planner():
    """
    建立新行程
    - GET: 顯示建立新行程的表單 (planner_new.html)
    - POST: 接收表單，存入 DB，重導向至行程規劃頁
    """
    pass

@planner_bp.route('/<int:id>')
def view_planner(id):
    """
    檢視行程規劃頁面
    - 取得特定行程詳情，包含天數與景點列表
    - 輸出：渲染 planner_view.html
    """
    pass

@planner_bp.route('/<int:id>/add_place', methods=['POST'])
def add_place(id):
    """
    新增景點
    - 接收表單，新增景點至特定天數，重導向回規劃頁
    """
    pass

@planner_bp.route('/destination/<int:dest_id>/delete', methods=['POST'])
def delete_destination(dest_id):
    """
    刪除單一景點
    - 刪除後重導向回所屬的規劃頁
    """
    pass

@planner_bp.route('/<int:id>/delete', methods=['POST'])
def delete_itinerary(id):
    """
    刪除整個行程
    - 刪除行程及關聯景點、預算，重導向回首頁
    """
    pass

@api_bp.route('/planner/update_order', methods=['POST'])
def update_order():
    """
    更新景點排序 (AJAX)
    - 接收 JSON，更新 DB 中的 order_index 與 day_number
    - 輸出 JSON {status: 'success'} 或錯誤訊息
    """
    pass

@planner_bp.route('/export/<int:id>/pdf')
def export_pdf(id):
    """
    匯出行程 (PDF)
    - 未來進階功能預留
    """
    pass
