from pathlib import Path
from time import sleep

import plotly.express as px
from clearml import Task
from clearml.backend_api.session.client import APIClient

dataframes = [
    (px.data.iris(), {"x": "sepal_width", "y": "sepal_length", "color": "species", "size": "petal_length"}),
    (px.data.wind(), {"x": "direction", "y": "strength", "color": "frequency", "size": "frequency"}),
    (px.data.election(), {"x": "district", "y": "total", "color": "winner", "size": "total"}),
    (px.data.carshare(), {"x": "centroid_lat", "y": "centroid_lon", "color": "peak_hour", "size": "car_hours"}),
]

task = Task.init(
    project_name="DevOps",
    task_name="Simple App",
    task_type=Task.TaskTypes.service,
    reuse_last_task_id=False,
)

logger = task.get_logger()


# args for the running task
args = {
    "a_number": 1.0,
    "a_string": "foo",
    "a_boolean": True,
    "a_project_id": ""
}

args = task.connect(args)

text_file = task.connect_configuration('file.txt', name='text_blob')

task.set_parameter(name='General/text_length', value=str(len(Path(text_file).read_text())))

client = APIClient(session=task.session)

project_id = args["a_project_id"]

i = 0

while True:
    print("Doing some work...")

    project_name = client.projects.get_by_id(project=project_id).name
    task.set_parameter(name='General/project_name', value=project_name)

    tasks = client.tasks.get_all(only_fields=["id"], project=[args["a_project_id"]])
    task.set_parameter(name='General/tasks_count', value=str(len(tasks)))

    df, kwargs = dataframes[i % len(dataframes)]
    i += 1
    fig = px.scatter(df, **kwargs)
    logger.report_plotly(title="Plots", series="plot", figure=fig)

    sleep(60)
