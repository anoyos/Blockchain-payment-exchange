from bullflag_commons.flask.setup import do_setup_flask_container

from app.containers import Container

container = Container()
do_setup_flask_container(container)

app = container.app()
container.routes_registrator()
