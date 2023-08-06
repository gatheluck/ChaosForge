"""

Links:
- https://distill.pub/2016/misread-tsne/

"""
import os
import pathlib
import streamlit as st
import numpy as np

from enum import Enum
from typing import Final, List, Set


class VisualizationMethod(str, Enum):
    T_SNE = "T_SNE"
    UMAP = "UMAP"





def load_npz_files(globed_npz_paths: List[pathlib.Path]) -> None:
    faces_list = list()
    fakeness_list = list()
    features_list = list()

    for data_path in globed_npz_paths:
        data = np.load(data_path)
        faces_list.append(data["faces"])
        fakeness_list.append(data["fakeness"])
        features_list.append(data["features"])

    st.session_state["faces_list"] = faces_list
    st.session_state["fakeness_list"] = fakeness_list
    st.session_state["features_list"] = features_list

def load_data() -> None:
    """ """
    _directory_path = pathlib.Path(st.session_state["input_directory_path"])
    _globed_npz_paths = list(_directory_path.glob("**/*.npz"))
    load_npz_files(_globed_npz_paths)
    print(_globed_npz_paths)

def transform_data():
    if not st.session_state["faces_list"]:
        return

    if st.session_state["visualization_method"] == VisualizationMethod.T_SNE:
        st.session_state["transformed_data"] = transform_tsne(
            data = data,
            perplexity = st.session_state["perplexity"],
            n_components = 2,
        )
    elif st.session_state["visualization_method"] == VisualizationMethod.UMAP:
        pass

if __name__ == "__main__":
    DEFAULT_INPUT_DIRECTORY = f"{os.getcwd()}/data/"

    # Layout (Sidebar)
    st.sidebar.markdown("## Settings")

    st.sidebar.text_input(
        "Input Directory Path",
        value=DEFAULT_INPUT_DIRECTORY,
        key="input_directory_path",
        label_visibility="visible",
    )
    st.sidebar.button(
        "Load Data",
        on_click=load_data,
    )

    st.sidebar.selectbox(
        "Visualization Method",
        [e.value for e in VisualizationMethod],
        format_func=lambda x: x.lower(),
        key="visualization_method",
    )

    if st.session_state["visualization_method"] == VisualizationMethod.UMAP:
        pass
    elif st.session_state["visualization_method"] == VisualizationMethod.T_SNE:
        st.sidebar.slider(
            "perplexity",
            min_value=1,
            max_value=300,
            value=30,
            key="perplexity",
            help="Parameter to balance attention between local and global aspects of the data",
            on_change=None,  # <- This will be used for call back
            args=None,  # <- args for call back
            kwargs=None,  # <- kwargs for call back
            label_visibility="visible",
        )
    else:
        pass

    