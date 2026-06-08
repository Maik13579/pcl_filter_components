# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

from python_qt_binding.QtCore import Qt
from python_qt_binding.QtGui import QPainter
from python_qt_binding.QtWidgets import QGraphicsScene, QGraphicsView, QMenu

from filter_component_editor.items import EdgeHandleItem, EdgeItem, NodeItem


class PipelineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, editor: "PipelineEditor") -> None:
        super().__init__(scene)
        self.editor = editor
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self._panning = False
        self._last_pan_pos = None

    def mouseDoubleClickEvent(self, event) -> None:
        item = self.itemAt(event.pos())
        if self.editor.create_topic_from_port(item):
            return
        while item is not None and not isinstance(item, (NodeItem, EdgeItem, EdgeHandleItem)):
            item = item.parentItem()
        if isinstance(item, NodeItem):
            item.setSelected(True)
            self.editor.edit_node(item)
            return
        if isinstance(item, EdgeHandleItem):
            item.setSelected(True)
            self.editor.begin_edge_rewire(item.edge_item, self.mapToScene(event.pos()))
            return
        if isinstance(item, EdgeItem):
            item.setSelected(True)
            self.editor.begin_edge_rewire(item, self.mapToScene(event.pos()))
            return
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        if event.button() == Qt.LeftButton and self.editor.begin_connection_drag(
            self.itemAt(event.pos()),
            self.mapToScene(event.pos()),
            bool(event.modifiers() & Qt.ShiftModifier),
        ):
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._panning and self._last_pan_pos is not None:
            delta = event.pos() - self._last_pan_pos
            self._last_pan_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return
        if self.editor.update_connection_drag(self.mapToScene(event.pos())):
            return
        if self.editor.update_edge_rewire(self.mapToScene(event.pos())):
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton and self._panning:
            self._panning = False
            self._last_pan_pos = None
            self.unsetCursor()
            event.accept()
            return
        if event.button() == Qt.LeftButton and self.editor.finish_connection_drag(
            self.itemAt(event.pos()),
            self.mapToScene(event.pos()),
        ):
            return
        if event.button() == Qt.LeftButton and self.editor.finish_edge_rewire(self.itemAt(event.pos())):
            return
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            self.editor.zoom_canvas(1.15)
        else:
            self.editor.zoom_canvas(1.0 / 1.15)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Delete:
            self.editor.delete_selected()
            return
        if event.key() == Qt.Key_C:
            self.editor.connect_selected()
            return
        super().keyPressEvent(event)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        connect_action = menu.addAction("Connect selected")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(event.globalPos())
        if action == edit_action:
            self.editor.edit_selected()
        elif action == connect_action:
            self.editor.connect_selected()
        elif action == delete_action:
            self.editor.delete_selected()
