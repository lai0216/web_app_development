from flask import Blueprint, render_template, request, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁 (行程列表)
    - 輸入：無
    - 處理邏輯：呼叫 Itinerary.get_all() 取得列表
    - 輸出：渲染 index.html
    """
    pass
