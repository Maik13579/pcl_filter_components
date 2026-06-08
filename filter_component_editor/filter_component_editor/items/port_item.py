# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

from python_qt_binding.QtCore import Qt
from python_qt_binding.QtGui import QColor
from python_qt_binding.QtWidgets import QGraphicsEllipseItem


class PortItem(QGraphicsEllipseItem):
    def __init__(self, label: str, diameter: float, label_color: QColor, parent) -> None:
        super().__init__(0, 0, diameter, diameter, parent)
        self.label = label
        self.label_color = label_color

    def paint(self, painter, option, widget=None) -> None:
        super().paint(painter, option, widget)
        font = painter.font()
        font.setBold(True)
        font.setPointSize(max(7, font.pointSize() - 1))
        painter.setFont(font)
        painter.setPen(self.label_color)
        painter.drawText(self.rect(), Qt.AlignCenter, self.label)
