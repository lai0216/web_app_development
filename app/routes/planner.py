from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from app.models.itinerary import Itinerary
from app.models.destination import Destination

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')
api_bp = Blueprint('api', __name__, url_prefix='/api')

@planner_bp.route('/new', methods=['GET', 'POST'])
def new_planner():
    """建立新行程"""
    if request.method == 'POST':
        title = request.form.get('title')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not title:
            flash("行程名稱為必填欄位", "danger")
            return render_template('planner_new.html')

        new_id = Itinerary.create(title, start_date, end_date)
        if new_id:
            flash("成功建立新行程！", "success")
            return redirect(url_for('planner.view_planner', id=new_id))
        else:
            flash("建立失敗，請稍後再試", "danger")

    return render_template('planner_new.html')

@planner_bp.route('/<int:id>')
def view_planner(id):
    """檢視行程規劃頁面"""
    itinerary = Itinerary.get_by_id(id)
    if not itinerary:
        abort(404)
        
    destinations = Destination.get_by_itinerary_and_day(id)
    return render_template('planner_view.html', itinerary=itinerary, destinations=destinations)

@planner_bp.route('/<int:id>/add_place', methods=['POST'])
def add_place(id):
    """新增景點"""
    name = request.form.get('name')
    day_number = request.form.get('day_number')
    notes = request.form.get('notes')

    if not name or not day_number:
        flash("景點名稱與天數為必填欄位", "danger")
    else:
        try:
            day_number = int(day_number)
            new_id = Destination.create(id, name, day_number, notes)
            if new_id:
                flash("景點新增成功！", "success")
            else:
                flash("新增景點失敗", "danger")
        except ValueError:
            flash("天數必須為數字", "danger")

    return redirect(url_for('planner.view_planner', id=id))

@planner_bp.route('/destination/<int:dest_id>/delete', methods=['POST'])
def delete_destination(dest_id):
    """刪除單一景點"""
    # 為了能重導向回行程頁面，需要先查出這個景點屬於哪個行程
    dest = Destination.get_by_id(dest_id)
    if not dest:
        abort(404)
        
    itinerary_id = dest['itinerary_id']
    if Destination.delete(dest_id):
        flash("景點已刪除", "success")
    else:
        flash("刪除景點失敗", "danger")
        
    return redirect(url_for('planner.view_planner', id=itinerary_id))

@planner_bp.route('/<int:id>/delete', methods=['POST'])
def delete_itinerary(id):
    """刪除整個行程"""
    if Itinerary.delete(id):
        flash("行程已成功刪除", "success")
    else:
        flash("刪除行程失敗", "danger")
    return redirect(url_for('main.index'))

@api_bp.route('/planner/update_order', methods=['POST'])
def update_order():
    """更新景點排序 (AJAX)"""
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400
        
    # data 預期格式: [{"id": 1, "order_index": 1, "day_number": 1}, ...]
    success = True
    for item in data:
        dest_id = item.get('id')
        order_index = item.get('order_index')
        day_number = item.get('day_number')
        
        if dest_id is not None and order_index is not None:
            if not Destination.update_order(dest_id, order_index, day_number):
                success = False
                
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Failed to update some records"}), 500

@planner_bp.route('/export/<int:id>/pdf')
def export_pdf(id):
    """匯出行程 (PDF) - 預留"""
    flash("PDF 匯出功能尚未開放", "info")
    return redirect(url_for('planner.view_planner', id=id))
