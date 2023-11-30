from flask.views import View

from canoe.post import bp
from canoe.post.models import Post


class PostList(View):
    db = get_db()
    db.cur.execute(
        SQL('SELECT * FROM {table} ORDER BY created DESC;').format(
            table=Identifier('work')
        )
    )
    works = db.cur.fetchall()
    return render_template('gallery/index.html', works=works)


bp.add_url_for()
