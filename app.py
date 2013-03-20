# standard libraries
import os
import sys



sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, render_template, request
from database.models import *
from database.migrations import *
# from services.json import transformers

#Flask implentation
app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yXda R~nbXHHun!jmNea]LWX/,?RT'


from services import guidelines_services, assets_services, login_services
from services.administration import stores_services, store_groups_services, users_services

app.register_blueprint(guidelines_services.mod)
app.register_blueprint(assets_services.mod)
app.register_blueprint(login_services.mod)
app.register_blueprint(stores_services.mod)
app.register_blueprint(store_groups_services.mod)
app.register_blueprint(users_services.mod)

# transformer = transformers.Transformers.getInstance()

#migrations
migrations=[]
migrations.append(Migration001())
migrations.append(Migration002())
migrations.append(Migration003())
migrations.append(Migration004())


session = Session()

schemas = session.query(DatabaseSchema).all()
if len(schemas)==0 :
    schema = DatabaseSchema(0)
    session.add(schema)
    session.commit()
else:
    schema=schemas[0]

#run migrations
for migration in migrations:
    app.logger.debug("Running migration " + str(migration.version))
    if migration.version>schema.version:
        migration.up(engine)
        schema.version=migration.version
        session.commit()


session.close()

@app.route("/ui/<template>")
def render_ui(template):
    return render_template(template)

@app.route("/inject")
def inject():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # injectData(Session())
    return "Import finished"


@app.route("/cleardb")
def cleardb():
    Base.metadata.drop_all(bind=engine)
    return "Database cleared"

