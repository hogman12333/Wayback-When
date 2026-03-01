from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#28141e"
# window_text = "#f0dce6"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#28141e"
# group_border_color = "#1a0d14"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#e8c8d8"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#3d1d2d"
# input_text = "#f0dce6"
# input_border_color = "#503040"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#7a3a5a"
# input_selection_text = "white"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#452535"
# button_text = "#f0dce6"
# button_border_color = "#503040"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#4d2d3d"
# button_hover_border = "#ff00bf"
# button_pressed_bg = "#28141e"
# button_pressed_border = "#ff00bf"
# button_disabled_bg = "#3d1d2d"
# button_disabled_text = "#8a6a7a"
# button_disabled_border = "#503040"

# --- Menu Bar ---
# menubar_bg = "#321a26"
# menubar_text = "#f0dce6"
# menubar_border = "#503040"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#4d2d3d"
# menubar_item_bg_selected = "#4d2d3d"
# menubar_item_text = "#f0dce6"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#3d1d2d"
# menu_border = "#503040"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#4d2d3d"
# menu_item_bg_selected = "#4d2d3d"
# menu_item_text = "#f0dce6"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#503040"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#3d1d2d"
# scrollbar_border = "#6a2a4a"
# scrollbar_handle_bg = "#4d2d3d"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#5d3d4d"
# scrollbar_handle_pressed_bg = "#6d4d5d"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#3d1d2d"
# progressbar_border = "#503040"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#dc0096"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#3d1d2d"
# tooltip_text = "#f0dce6"
# tooltip_border = "#503040"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#3d1d2d"
# checkbox_border = "#503040"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#dc0096"
# checkbox_checked_border = "#dc0096"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#3d1d2d"
# slider_groove_border = "#503040"
# slider_handle_bg = "#dc0096"
# slider_handle_border = "#b00078"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(40, 20, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Base, QColor(35, 15, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 25, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Text, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.Button, QColor(55, 35, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 220, 230))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.magenta)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(220, 0, 150))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(167, 127, 147))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #f0dce6;
    background-color: #28141e;
}

QGroupBox { 
    border: 2px solid #1a0d14;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #28141e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #e8c8d8;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #3d1d2d;
    color: #f0dce6;
    border: 1px solid #503040;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #7a3a5a;
    selection-color: white;
}

QPushButton {
    background-color: #452535;
    color: #f0dce6;
    border: 1px solid #503040;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #4d2d3d;
    border-color: #ff00bf;
}

QPushButton:pressed {
    background-color: #28141e;
}

QPushButton:disabled {
    color: #8a6a7a;
    background-color: #3d1d2d;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #321a26;
    color: #f0dce6;
    border-bottom: 1px solid #503040;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #4d2d3d;
}

QMenu {
    background-color: #3d1d2d;
    color: #f0dce6;
    border: 1px solid #503040;
}

QMenu::item:selected {
    background-color: #4d2d3d;
}

QScrollBar:vertical {
    border: 1px solid #6a2a4a;
    background: #3d1d2d;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #503040;
    background: #3d1d2d;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #4d2d3d;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #4d2d3d;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #503040;
    border-radius: 4px;
    text-align: center;
    background-color: #3d1d2d;
}

QProgressBar::chunk {
    background-color: #dc0096;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)