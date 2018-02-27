from flask import Blueprint, render_template, redirect, request
from bson.objectid import ObjectId
from nilms.session_utils import login_required
from nilms.asset_utils import upload_file
from nilms.theme_utils import (
    get_theme_templates,
    get_theme_db,
    set_theme_db,
    get_template_config
)
from nilms.facades.page_facade import PageFacade
from nilms.facades.post_facade import PostFacade
from nilms.facades.asset_facade import AssetFacade


bp = Blueprint(
    __name__,
    __name__,
    template_folder='templates',
    url_prefix='/admin'
)


@bp.route('/')
@login_required
def show():
    return redirect('/admin/pages')


@bp.route('/pages')
@login_required
def show_pages():
    pages = PageFacade.get_all()

    return render_template('admin/pages.html', pages=pages)


@bp.route('/page/<page_id>', methods=['POST', 'GET'])
@bp.route('/page', defaults={'page_id': None}, methods=['POST', 'GET'])
@login_required
def show_page(page_id):
    page = PageFacade.get(id=ObjectId(page_id)) if page_id else None
    templates = get_theme_templates()
    template_config = None

    if page:
        template_config = get_template_config(page.template)

    if request.method == 'POST':
        if request.form.get('delete'):
            page.delete()
            return redirect('/admin/pages')

        if request.form.get('submit'):
            name = request.form.get('page-name')
            template = request.form.get('page-template')
            is_startpage = request.form.get('page-is_startpage') is not None
            template_fields = {} if not page else page.fields

            for k, v in request.files.items():
                if 'template-field' in k:
                    field_file = request.files.get(k)
                    assetname = k
                    filename = upload_file(field_file)
                    asset = AssetFacade.create(
                        name=assetname,
                        filename=filename
                    )

                    template_fields[k] = asset.to_dbref()

            if not page:
                page = PageFacade.create(
                    name=name,
                    template=template,
                    is_startpage=is_startpage,
                    fields=template_fields
                )
                return redirect('/admin/page/{}'.format(str(page.id)))
            else:
                page.update(
                    name=name,
                    template=template,
                    is_startpage=is_startpage,
                    fields=template_fields
                )
                page = PageFacade.get(id=ObjectId(page_id))

    return render_template(
        'admin/page.html',
        template_config=template_config,
        templates=templates,
        page=page
    )


@bp.route('/posts')
@login_required
def show_posts():
    posts = PostFacade.get_all()

    return render_template('admin/posts.html', posts=posts)


@bp.route('/post/<post_id>', methods=['POST', 'GET'])
@bp.route('/post', defaults={'post_id': None}, methods=['POST', 'GET'])
@login_required
def show_post(post_id):
    post = PostFacade.get(id=ObjectId(post_id)) if post_id else None
    templates = get_theme_templates()
    assets = AssetFacade.get_all()

    if request.method == 'POST':
        if request.form.get('delete'):
            post.delete()
            return redirect('/admin/posts')

        if request.form.get('submit'):
            name = request.form.get('post-name')
            content = request.form.get('post-content')
            template = request.form.get('post-template')
            is_published = request.form.get('post-is_published') is not None
            asset_ids = request.form.getlist('post-assets')
            _assets = AssetFacade.get_by_ids(
                [ObjectId(str(_id)) for _id in asset_ids]
            )
            _assets = [ass.to_dbref() for ass in _assets]

            if not post:
                post = PostFacade.create(
                    name=name,
                    content=content,
                    template=template,
                    is_published=is_published,
                    assets=_assets
                )
                return redirect('/admin/post/{}'.format(str(post.id)))
            else:
                post.update(
                    name=name,
                    content=content,
                    template=template,
                    is_published=is_published,
                    assets=_assets
                )
                post = PostFacade.get(id=ObjectId(post_id))

    return render_template(
        'admin/post.html',
        templates=templates,
        assets=assets,
        post=post
    )


@bp.route('/assets')
@login_required
def show_assets():
    assets = AssetFacade.get_all()

    return render_template('admin/assets.html', assets=assets)


@bp.route('/asset/<asset_id>', methods=['POST', 'GET'])
@bp.route('/asset', defaults={'asset_id': None}, methods=['POST', 'GET'])
@login_required
def show_asset(asset_id):
    errors = []
    asset = AssetFacade.get(id=ObjectId(asset_id)) if asset_id else None

    if request.method == 'POST':
        if request.form.get('delete'):
            asset.delete()
            return redirect('/admin/assets')

        if request.form.get('submit'):
            name = request.form.get('asset-name')
            asset_file = request.files.get('asset-file')
            filename = None

            kwargs = {
                'name': name
            }

            if asset_file:
                try:
                    filename = upload_file(asset_file)
                    kwargs['filename'] = filename
                except Exception as e:
                    errors.append(str(e))

            if not len(errors):
                if not asset:
                    asset = AssetFacade.create(
                        **kwargs
                    )
                    return redirect('/admin/asset/{}'.format(str(asset.id)))
                else:
                    asset.update(
                        **kwargs
                    )
                    asset = AssetFacade.get(id=ObjectId(asset_id))

    return render_template('admin/asset.html', asset=asset, errors=errors)


@bp.route('/theme-db', methods=['POST', 'GET'])
@login_required
def show_theme_db():
    db = get_theme_db()

    if request.method == 'POST':
        if request.form.get('submit'):
            for k, v in request.form.items():
                if k == 'submit':
                    continue

                db[k] = v

            set_theme_db(db)

    return render_template('admin/theme_db.html', db=db)


@bp.route('/settings')
@login_required
def show_settings():
    return render_template('admin/settings.html')
