"""

Links:
- https://distill.pub/2016/misread-tsne/

"""
import os
import pathlib
from enum import Enum
from typing import Final, List, Set


class VisualizationMethod(str, Enum):
    UMAP = "UMAP"
    T_SNE = "T_SNE"


TARGET_EXTENSIONS: Final[Set[str]] = {
    ".png",
    ".PNG",
    ".jpg",
    ".JPG",
    ".jpeg",
    ".JPEG",
}


def glob_image_paths(
    target_directry_path: pathlib.Path,
    target_extensions: Set[str],
) -> List[pathlib.Path]:
    """ """
    globed_paths = list()
    for _globed_paths in input_dir.glob(glob_target):
        globed_paths.extend(_globed_paths)

    return globed_paths


if __name__ == "__main__":
    import pandas as pd

    import plotly.figure_factory as ff
    import plotly.graph_objects as go
    import streamlit as st

    st.set_page_config(layout="wide")

    # Data
    df = pd.read_csv("data/plotly/data_sample.csv")
    vars_cat = [var for var in df.columns if var.startswith("cat")]
    vars_cont = [var for var in df.columns if var.startswith("cont")]

    # Graph (Pie Chart in Sidebar)
    df_target = df[["id", "target"]].groupby("target").count() / len(df)
    fig_target = go.Figure(
        data=[go.Pie(labels=df_target.index, values=df_target["id"], hole=0.3)]
    )
    fig_target.update_layout(
        showlegend=False, height=200, margin={"l": 20, "r": 60, "t": 0, "b": 0}
    )
    fig_target.update_traces(textposition="inside", textinfo="label+percent")

    # Layout (Sidebar)
    st.sidebar.markdown("## Settings")

    _target_directry_path = st.sidebar.text_input(
        "Input Path",
        value=f"{os.getcwd()}/data/",
        on_change=None,  # <- This will be used for call back
        args=None,
        kwargs=None,
        label_visibility="visible",
    )
    _target_extensions = st.sidebar.multiselect(
        "Target Extentions",
        TARGET_EXTENSIONS,
        default=TARGET_EXTENSIONS,
        on_change=None,  # <- This will be used for call back
        args=None,
        kwargs=None,
        label_visibility="visible",
    )

    # st.button(
    #     label,
    #     on_click=glob_image_paths,
    #     kwargs={
    #         target_directry_path = input_directory_path,
    #         target_extensions =,
    #         = input_directory_path,
    #     },
    # )

    visualization_method_selected = st.sidebar.selectbox(
        "Visualization Method",
        [e.value for e in VisualizationMethod],
        format_func=lambda x: x.lower(),
    )

    if visualization_method_selected == VisualizationMethod.UMAP:
        pass
    elif visualization_method_selected == VisualizationMethod.T_SNE:
        st.sidebar.slider(
            "perplexity",
            min_value=1,
            max_value=300,
            value=30,
            help="Parameter to balance attention between local and global aspects of the data",
            on_change=None,  # <- This will be used for call back
            args=None,  # <- args for call back
            kwargs=None,  # <- kwargs for call back
            label_visibility="visible",
        )
    else:
        pass

    cat_selected = st.sidebar.selectbox("Categorical Variables", vars_cat)
    cont_selected = st.sidebar.selectbox("Continuous Variables", vars_cont)
    cont_multi_selected = st.sidebar.multiselect(
        "Correlation Matrix", vars_cont, default=vars_cont
    )
    st.sidebar.markdown("## Target Variables")
    st.sidebar.plotly_chart(fig_target, use_container_width=True)

    # Categorical Variable Bar Chart in Content
    df_cat = df.groupby([cat_selected, "target"]).count()[["id"]].reset_index()

    cat0 = df_cat[df_cat["target"] == 0]
    cat1 = df_cat[df_cat["target"] == 1]

    fig_cat = go.Figure(
        data=[
            go.Bar(name="target=0", x=cat0[cat_selected], y=cat0["id"]),
            go.Bar(name="target=1", x=cat1[cat_selected], y=cat1["id"]),
        ]
    )

    fig_cat.update_layout(
        height=300,
        width=500,
        margin={"l": 20, "r": 20, "t": 0, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        barmode="stack",
    )
    fig_cat.update_xaxes(title_text=None)
    fig_cat.update_yaxes(title_text="# of samples")

    # Continuous Variable Distribution in Content
    li_cont0 = df[df["target"] == 0][cont_selected].values.tolist()
    li_cont1 = df[df["target"] == 1][cont_selected].values.tolist()

    cont_data = [li_cont0, li_cont1]
    group_labels = ["target=0", "target=1"]

    fig_cont = ff.create_distplot(
        cont_data, group_labels, show_hist=False, show_rug=False
    )
    fig_cont.update_layout(
        height=300,
        width=500,
        margin={"l": 20, "r": 20, "t": 0, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Correlation Matrix in Content
    df_corr = df[cont_multi_selected].corr()
    fig_corr = go.Figure(
        [go.Heatmap(z=df_corr.values, x=df_corr.index.values, y=df_corr.columns.values)]
    )
    fig_corr.update_layout(
        height=300, width=1000, margin={"l": 20, "r": 20, "t": 0, "b": 0}
    )

    # Layout (Content)
    st.plotly_chart(
        figure_or_data,
        use_container_width=False,
        sharing="streamlit",
        theme="streamlit",
    )

    # left_column, right_column = st.columns(2)
    # left_column.subheader("Categorical Variable Distribution: " + cat_selected)
    # right_column.subheader("Continuous Variable Distribution: " + cont_selected)
    # left_column.plotly_chart(fig_cat)
    # right_column.plotly_chart(fig_cont)
    # st.subheader("Correlation Matrix")
    # st.plotly_chart(fig_corr)
