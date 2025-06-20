from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QTimer
import sys
import random

class PassengerLabel(QLabel):
    def __init__(self, color):
        super().__init__()
        self.color_name = color
        self.setFixedSize(30, 30)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: 15px;
            border: 2px solid white;
        """)

class BusButton(QPushButton):
    def __init__(self, color, capacity, board_callback, move_callback, direction='H'):
        arrow = "←" if direction == 'H' else "↑"  # seta à esquerda
        super().__init__(f"{arrow}\n{color.upper()}\n0/{capacity}")
        self.color = color
        self.capacity = capacity
        self.boarded = 0
        self.direction = direction
        self.board_callback = board_callback
        self.move_callback = move_callback
        self.is_moving = False
        self.is_at_boarding = False

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-weight: bold;
                border-radius: 12px;
                padding: 5px;
                border: 2px solid white;
            }}
            QPushButton:disabled {{
                background-color: gray;
            }}
        """)
        self.setFixedSize(100, 60)

    def mousePressEvent(self, event):
        if not self.is_moving:
            self.move_callback(self)

    def update_text(self):
        arrow = "←" if self.direction == 'H' else "↑"
        self.setText(f"{arrow}\n{self.color.upper()}\n{self.boarded}/{self.capacity}")

class CarJamGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Jam - Embarque com Movimento")
        self.setFixedSize(1000, 700)

        self.grid_size = 8
        self.cell_size = 100

        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.available_colors = ["red", "blue", "yellow", "green"]
        self.passenger_colors = random.choices(self.available_colors, k=20)
        self.passenger_labels = []
        self.bus_buttons = []

        self.main_layout = QVBoxLayout()
        self.passenger_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        self.boarding_area = QLabel("ÁREA DE EMBARQUE\n(TODOS OS CARROS)")
        self.boarding_area.setFixedSize(100, self.grid_size * self.cell_size)
        self.boarding_area.setStyleSheet("""
            background-color: lightgray; 
            border: 3px dashed black;
            font-weight: bold;
            qproperty-alignment: 'AlignCenter';
        """)
        # Embarque agora na **primeira coluna**
        self.grid_layout.addWidget(self.boarding_area, 0, 0, self.grid_size, 1)

        for color in self.passenger_colors:
            label = PassengerLabel(color)
            self.passenger_labels.append(label)
            self.passenger_layout.addWidget(label)

        for row in range(self.grid_size):
            for col in range(1, self.grid_size):
                cell = QLabel()
                cell.setFixedSize(self.cell_size, self.cell_size)
                cell.setStyleSheet("border: 1px solid black;")
                self.grid_layout.addWidget(cell, row, col)

        self.bus_directions = {color: 'H' for color in self.available_colors}
        self.bus_positions = {}

        buses = []
        for color in self.available_colors:
            for _ in range(1):  # 1 autocarro por cor
                buses.append((color, 4))

        row_counter = 0
        for color, capacity in buses:
            bus_button = BusButton(color, capacity, self.board_passengers, self.move_bus, self.bus_directions[color])
            self.bus_buttons.append(bus_button)
            # AGORA começa na última coluna!
            self.grid[row_counter][self.grid_size-1] = color
            self.grid_layout.addWidget(bus_button, row_counter, self.grid_size-1)
            self.bus_positions[bus_button] = (row_counter, self.grid_size-1)
            row_counter += 1

        self.reset_button = QPushButton("Reiniciar Jogo")
        self.reset_button.clicked.connect(self.reset_game)

        self.passenger_count = QLabel(f"Passageiros restantes: {len(self.passenger_labels)}")

        self.main_layout.addWidget(self.passenger_count)
        self.main_layout.addLayout(self.passenger_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.reset_button)
        self.setLayout(self.main_layout)

    def board_passengers(self, bus):
        if bus.boarded >= bus.capacity:
            if self.is_game_stuck():
                self.show_game_stuck_popup()
            return False

        if self.passenger_labels:
            first_label = self.passenger_labels[0]
            if first_label.color_name == bus.color:
                self.passenger_layout.removeWidget(first_label)
                first_label.hide()
                self.passenger_labels.pop(0)

                bus.boarded += 1
                bus.update_text()
                self.passenger_count.setText(f"Passageiros restantes: {len(self.passenger_labels)}")

                if len(self.passenger_labels) == 0:
                    self.show_game_over_popup()

                return True

        if self.is_game_stuck():
            self.show_game_stuck_popup()

        return False

    def is_game_stuck(self):
        if not self.passenger_labels:
            return False

        first = self.passenger_labels[0]
        for bus in self.bus_buttons:
            if bus.color == first.color_name and bus.boarded < bus.capacity:
                return False

        return True

    def show_game_stuck_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Jogo Travado")
        msg.setText("O jogo ficou sem solução.\nNenhum autocarro pode embarcar o primeiro passageiro da fila.\nReinicie o jogo.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def get_bus_by_color(self, color):
        for bus in self.bus_buttons:
            if bus.color == color and bus.boarded < bus.capacity:
                return bus
        return None

    def can_move_to(self, row, col):
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            return False
        return self.grid[row][col] is None

    def move_bus(self, bus_button):
        if bus_button.is_moving:
            return

        self.grid_layout.removeWidget(bus_button)
        bus_button.setParent(self)
        bus_button.raise_()

        def animate_movement():
            current_row, current_col = self.bus_positions[bus_button]

            # MOVIMENTO PRINCIPAL: Direita → Esquerda (coluna-1)
            if current_col == 0:
                if self.board_passengers(bus_button):
                    QTimer.singleShot(1000, lambda: self.return_bus(bus_button))
                else:
                    self.return_bus(bus_button)
                return

            new_row, new_col = current_row, current_col - 1

            if not self.can_move_to(new_row, new_col):
                bus_button.is_moving = False
                return

            self.grid[current_row][current_col] = None
            self.grid[new_row][new_col] = bus_button.color
            self.bus_positions[bus_button] = (new_row, new_col)

            current_pos = bus_button.pos()
            new_pos = QPoint(current_pos.x() - self.cell_size, current_pos.y())

            anim = QPropertyAnimation(bus_button, b"pos", self)
            anim.setDuration(300)
            anim.setEndValue(new_pos)

            def on_animation_finished():
                animate_movement()

            anim.finished.connect(on_animation_finished)
            anim.start()

        bus_button.is_moving = True
        animate_movement()

    def return_bus(self, bus_button):
        def animate_return():
            current_row, current_col = self.bus_positions[bus_button]

            # MOVIMENTO DE RETORNO: Esquerda → Direita (coluna+1)
            if current_col == self.grid_size - 1:
                bus_button.setParent(None)
                self.grid_layout.addWidget(bus_button, current_row, self.grid_size-1)
                self.bus_positions[bus_button] = (current_row, self.grid_size-1)
                self.grid[current_row][self.grid_size-1] = bus_button.color
                bus_button.is_moving = False
                return

            new_row, new_col = current_row, current_col + 1

            self.grid[current_row][current_col] = None
            self.grid[new_row][new_col] = bus_button.color
            self.bus_positions[bus_button] = (new_row, new_col)

            current_pos = bus_button.pos()
            new_pos = QPoint(current_pos.x() + self.cell_size, current_pos.y())

            anim = QPropertyAnimation(bus_button, b"pos", self)
            anim.setDuration(300)
            anim.setEndValue(new_pos)

            def on_animation_finished():
                animate_return()

            anim.finished.connect(on_animation_finished)
            anim.start()

        bus_button.is_moving = True
        animate_return()

    def show_game_over_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Fim de Jogo")
        msg.setText("A fila de passageiros acabou!\nFim de Jogo!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def reset_game(self):
        for label in self.passenger_labels:
            self.passenger_layout.removeWidget(label)
            label.deleteLater()
        self.passenger_labels.clear()

        for bus in self.bus_buttons:
            self.grid_layout.removeWidget(bus)
            bus.deleteLater()
        self.bus_buttons.clear()
        self.bus_positions.clear()
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.passenger_colors = random.choices(self.available_colors, k=20)
        for color in self.passenger_colors:
            label = PassengerLabel(color)
            self.passenger_labels.append(label)
            self.passenger_layout.addWidget(label)

        buses = []
        for color in self.available_colors:
            for _ in range(1):
                buses.append((color, 4))

        row_counter = 0
        for color, capacity in buses:
            bus_button = BusButton(color, capacity, self.board_passengers, self.move_bus, self.bus_directions[color])
            self.bus_buttons.append(bus_button)
            # Começa na última coluna
            self.grid[row_counter][self.grid_size-1] = color
            self.grid_layout.addWidget(bus_button, row_counter, self.grid_size-1)
            self.bus_positions[bus_button] = (row_counter, self.grid_size-1)
            row_counter += 1

        self.passenger_count.setText(f"Passageiros restantes: {len(self.passenger_labels)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarJamGame()
    window.show()
    sys.exit(app.exec())