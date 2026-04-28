from flask import Blueprint, render_template, request, redirect, url_for, abort

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

@budget_bp.route('/<int:id>')
def view_budget(id):
    """
    檢視預算頁面
    - 顯示特定行程的各項預估花費與總計
    - 輸出：渲染 budget_view.html
    """
    pass

@budget_bp.route('/<int:id>/add', methods=['POST'])
def add_budget_item(id):
    """
    新增預算項目
    - 接收表單，新增一筆預算，重導向回預算頁
    """
    pass

@budget_bp.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_budget_item(item_id):
    """
    刪除預算項目
    - 刪除單一預算項目，重導向回所屬預算頁
    """
    pass
