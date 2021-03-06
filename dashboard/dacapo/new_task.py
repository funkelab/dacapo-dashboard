from flask import (
    render_template,
    request,
    json,
    jsonify,
    url_for,
    redirect,
    current_app,
)

from .blue_print import bp
from dacapo.store.converter import converter

from .helpers import get_config_names
from .configs import CONFIGURABLES, CONFIGURABLE_FIELDS


@bp.route("/new_task", methods=["GET", "POST"])
def new_task():
    if request.method == "POST":
        try:
            data = request.json
            current_app.config["stores"].config.store_task_config(data)
            return jsonify({"success": True})
        except Exception as e:
            raise (e)
            return jsonify({"success": False, "error": str(e)})

    config_names = get_config_names("Task")
    config_fields = {name: CONFIGURABLE_FIELDS[name] for name in config_names}
    return render_template(
        "dacapo/forms/task.html",
        fields=config_fields,
        id_prefix="task",
        all_names=json.dumps(
            current_app.config["stores"].config.retrieve_task_config_names()
        ),
    )


@bp.route("/new_task/<state>", methods=["GET"])
def new_task_from_existing(state):
    state = state.replace("%2F", "/")
    config_names = get_config_names("Task")
    config_fields = {name: CONFIGURABLE_FIELDS[name] for name in config_names}
    return render_template(
        "dacapo/forms/task.html",
        fields=config_fields,
        id_prefix="task",
        all_names=json.dumps(
            current_app.config["stores"].config.retrieve_task_config_names()
        ),
        value=state,
    )


@bp.route("/load_task/<name>", methods=["GET"])
def load_task(name):
    config = current_app.config["stores"].config.retrieve_task_config(name)
    state_dict = converter.unstructure(config)
    state = json.dumps(state_dict).replace("/", "%2F")

    return redirect(url_for("dacapo.new_task_from_existing", state=state))
