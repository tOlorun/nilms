from flask import Blueprint, render_template, redirect
from nilms.session_utils import login_required
from nilms.theme_utils import get_theme_templates


bp = Blueprint(
    __name__,
    __name__,
    template_folder='templates',
    url_prefix='/admin'
)


@bp.route('/')
@login_required
def show():
    return redirect('/admin/dashboard')


@bp.route('/dashboard')
@login_required
def show_dashboard():
    return render_template('admin/dashboard.html')


@bp.route('/pages')
@login_required
def show_pages():
    return render_template('admin/pages.html')


@bp.route('/page')
@login_required
def show_page():
    templates = get_theme_templates()

    return render_template('admin/page.html', templates=templates)


@bp.route('/settings')
@login_required
def show_settings():
    return render_template('admin/settings.html')
