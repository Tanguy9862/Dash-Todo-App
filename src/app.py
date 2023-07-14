import dash
from dash import Input, Output, State, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = 'https://github.com/tanguy9862'
LINKEDIN = 'https://fr.linkedin.com/in/tanguy-surowiec-69aa79222'
CONTACT_ICON_WIDTH = 30
HIDE = {'display': 'none'}


def make_new_task(n, task):
    return dmc.Group(
        [
            dmc.Checkbox(label=task, value=task),
            dmc.ActionIcon(
                DashIconify(icon='iwwa:delete'),
                id={'type': 'dynamic-btn', 'index': n}
            )
        ], position='apart'
    )


app = dash.Dash(__name__, title='TODO App')
server = app.server

app.layout = dmc.MantineProvider(
    id='general-theme',
    theme={
        'components': {
            'Title': {
                'styles': {'root': {'fontFamily': 'system-ui'}}
            }
        }
    },
    withGlobalStyles={'minHeight': '100vh'},
    children=[
        dmc.Paper(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.Container(
                                    [
                                        dmc.Group(children=[
                                            dmc.Title('TODO Dash App', order=1),
                                            dmc.Switch(
                                                id='switch-theme',
                                                offLabel=DashIconify(icon="radix-icons:moon", width=20),
                                                onLabel=DashIconify(icon="radix-icons:sun", width=20),
                                                size="lg",
                                                color='teal',
                                                checked=False,
                                                persistence=True
                                            )
                                        ], position='apart'),
                                        dmc.Space(h=100),
                                        dmc.Group(
                                            [
                                                dmc.TextInput(id='add-task', placeholder='Add a new task..', size='md',
                                                              w=350, icon=DashIconify(icon='mdi-light:note')),
                                                dmc.Button('Add', id='add-btn', color='violet', size='md')
                                            ],
                                            position='center'
                                        ),
                                        dmc.Divider(label='TO-DO', mt=25, mb=10),
                                        dmc.CheckboxGroup(id='task-container', orientation='vertical', p=10,
                                                          children=[]),
                                        dmc.Group(
                                            position='right',
                                            mt=35,
                                            children=[
                                                dmc.Button(
                                                    'CLEAR',
                                                    id='del-btn',
                                                    color='red',
                                                    rightIcon=DashIconify(icon='fluent:delete-20-regular'),
                                                    variant='outline',
                                                    style=HIDE
                                                )
                                            ]
                                        ),
                                        dmc.Footer(
                                            height=60,
                                            fixed=True,
                                            withBorder=False,
                                            children=[
                                                dmc.Group(
                                                    children=[
                                                        dmc.Anchor(
                                                            children=[DashIconify(
                                                                icon='mdi:github', width=CONTACT_ICON_WIDTH)
                                                            ],
                                                            href=GITHUB
                                                        ),
                                                        dmc.Anchor(
                                                            children=[
                                                                DashIconify(
                                                                    icon='ri:linkedin-fill', width=CONTACT_ICON_WIDTH)
                                                            ],
                                                            href=LINKEDIN
                                                        )
                                                    ], position='center'
                                                )
                                            ]
                                        )
                                    ],
                                    mt=20,
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output('general-theme', 'theme'),
    Input('switch-theme', 'checked')
)
def update_theme(checked):
    if checked:
        return {'colorScheme': 'dark'}


@app.callback(
    Output('task-container', 'children'),
    Output('del-btn', 'style'),
    Input('add-btn', 'n_clicks'),
    Input('del-btn', 'n_clicks'),
    Input({'type': 'dynamic-btn', 'index': ALL}, 'n_clicks'),
    State('add-task', 'value'),
    State('task-container', 'children'),
    prevent_initial_call=True
)
def update_tasks(n, _1, _2, new_task, all_tasks):
    if ctx.triggered_id == 'add-btn':
        all_tasks.append(make_new_task(n, new_task))
    elif ctx.triggered_id == 'del-btn':
        return [], HIDE
    else:
        n_del = ctx.triggered_id['index']
        all_tasks = [task for task in all_tasks if f"'index': {n_del}" not in str(task)]

    style = (all_tasks and {'style': ''}) or HIDE
    return all_tasks, style


if __name__ == '__main__':
    app.run_server()
