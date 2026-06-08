# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

from python_qt_binding.QtCore import QPointF
from python_qt_binding.QtGui import QBrush, QPen, QPolygonF
from python_qt_binding.QtWidgets import QGraphicsItem, QGraphicsPolygonItem


class EdgeHandleItem(QGraphicsPolygonItem):
    def __init__(self, edge_item: "EdgeItem") -> None:
        size = 9.0
        super().__init__(QPolygonF([
            QPointF(0.0, -size),
            QPointF(size, 0.0),
            QPointF(0.0, size),
            QPointF(-size, 0.0),
        ]))
        self.edge_item = edge_item
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        color = edge_item.source.editor.edge_color(edge_item.edge, selected=True)
        self.setBrush(QBrush(color))
        self.setPen(QPen(color, 1))
        self.setZValue(2)

    def itemChange(self, change, value):
        result = super().itemChange(change, value)
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.edge_item.edge.position = {"x": float(self.pos().x()), "y": float(self.pos().y())}
            self.edge_item.refresh_label()
        return result
