from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.itinerary import Itinerary
from app.models.budget import Budget

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

@budget_bp.route('/<int:id>')
def view_budget(id):
    """檢視預算頁面"""
    itinerary = Itinerary.get_by_id(id)
    if not itinerary:
        abort(404)
        
    budgets = Budget.get_by_itinerary(id)
    total_amount = sum(b['amount'] for b in budgets) if budgets else 0.0
    
    return render_template('budget_view.html', itinerary=itinerary, budgets=budgets, total_amount=total_amount)

@budget_bp.route('/<int:id>/add', methods=['POST'])
def add_budget_item(id):
    """新增預算項目"""
    category = request.form.get('category')
    amount = request.form.get('amount')
    notes = request.form.get('notes')

    if not category or not amount:
        flash("分類與金額為必填欄位", "danger")
    else:
        try:
            amount = float(amount)
            new_id = Budget.create(id, category, amount, notes)
            if new_id:
                flash("預算項目新增成功！", "success")
            else:
                flash("新增預算失敗", "danger")
        except ValueError:
            flash("金額必須為數字", "danger")

    return redirect(url_for('budget.view_budget', id=id))

@budget_bp.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_budget_item(item_id):
    """刪除預算項目"""
    # 為了能重導向回預算頁面，需要先查出這個項目屬於哪個行程
    budget_item = Budget.get_by_id(item_id)
    if not budget_item:
        abort(404)
        
    itinerary_id = budget_item['itinerary_id']
    if Budget.delete(item_id):
        flash("預算項目已刪除", "success")
    else:
        flash("刪除預算項目失敗", "danger")
        
    return redirect(url_for('budget.view_budget', id=itinerary_id))
