# pylint: disable=too-few-public-methods, missing-class-docstring
"""Query graph models."""
from typing import List, Union

from pydantic import BaseModel, Field

from models.basics import BiolinkEntity, BiolinkRelation


class QNode(BaseModel):
    """Query node."""

    id: str = Field(
        ...,
        title='id',
    )
    curie: Union[BiolinkEntity, List[BiolinkEntity]] = Field(
        None,
        title='CURIE',
    )
    type: Union[str, List[str]] = Field(
        None,
        title='type',
    )

    class Config:
        title = 'query-graph node'


class QEdge(BaseModel):
    """Query edge."""

    id: str = Field(
        ...,
        title='id',
    )
    source_id: str = Field(
        ...,
        title='source node id',
    )
    target_id: str = Field(
        ...,
        title='target node id',
    )
    type: Union[BiolinkRelation, List[BiolinkRelation]] = Field(
        None,
        title='type',
    )

    class Config:
        title = 'query-graph edge'


class QueryGraph(BaseModel):
    """Query graph."""

    nodes: List[QNode] = Field(
        ...,
        title='list of nodes',
    )
    edges: List[QEdge] = Field(
        ...,
        title='list of edges',
    )

    class Config:
        title = 'simple query graph'
