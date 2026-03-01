from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#fffadc"
# window_text = "#464232"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#fffadc"
# group_border_color = "#e0d8b0"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#8c7d32"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#fffef0"
# input_text = "#464232"
# input_border_color = "#d8d0a0"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#ffe89c"
# input_selection_text = "#464232"
# input_placeholder = "#a09a82"

# --- Buttons ---
# button_bg = "#fff5c8"
# button_text = "#464232"
# button_border_color = "#d8d0a0"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#fff0b4"
# button_hover_border = "#c0b070"
# button_pressed_bg = "#e8e0b0"
# button_pressed_border = "#c0b070"
# button_disabled_bg = "#f0ead8"
# button_disabled_text = "#a09a82"
# button_disabled_border = "#d8d0a0"

# --- Menu Bar ---
# menubar_bg = "#fff5c8"
# menubar_text = "#464232"
# menubar_border = "#d8d0a0"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#ffe89c"
# menubar_item_bg_selected = "#ffe89c"
# menubar_item_text = "#464232"
# menubar_item_text_hover = "#464232"
# menubar_item_text_selected = "#464232"

# --- Dropdown Menus ---
# menu_bg = "#fffef0"
# menu_border = "#d8d0a0"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#ffe89c"
# menu_item_bg_selected = "#ffe89c"
# menu_item_text = "#464232"
# menu_item_text_hover = "#464232"
# menu_item_text_selected = "#464232"
# menu_separator_color = "#d8d0a0"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#fffef0"
# scrollbar_border = "#d8d0a0"
# scrollbar_handle_bg = "#e8e0b0"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#d0c8a0"
# scrollbar_handle_pressed_bg = "#c0b890"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#fffef0"
# progressbar_border = "#d8d0a0"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#ffdb58"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#fffef0"
# tooltip_text = "#464232"
# tooltip_border = "#d8d0a0"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#fffef0"
# checkbox_border = "#d8d0a0"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#ffdb58"
# checkbox_checked_border = "#d8d0a0"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#fffef0"
# slider_groove_border = "#d8d0a0"
# slider_handle_bg = "#e8e0b0"
# slider_handle_border = "#c0b070"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 250, 220))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(70, 65, 50))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 253, 240))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(250, 245, 220))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 253, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(70, 65, 50))
    palette.setColor(QPalette.ColorRole.Text, QColor(60, 55, 40))
    palette.setColor(QPalette.ColorRole.Button, QColor(255, 245, 200))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(80, 75, 60))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.darkYellow)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 230, 150))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(50, 45, 30))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(180, 175, 150))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #464232;
    background-color: #fffadc;
}

QGroupBox { 
    border: 2px solid #e0d8b0;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #fffadc;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #8c7d32;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #fffef0;
    color: #464232;
    border: 1px solid #d8d0a0;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #ffe89c;
    selection-color: #464232;
}

QPushButton {
    background-color: #fff5c8;
    color: #464232;
    border: 1px solid #d8d0a0;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #fff0b4;
    border-color: #c0b070;
}

QPushButton:pressed {
    background-color: #e8e0b0;
}

QPushButton:disabled {
    color: #a09a82;
    background-color: #f0ead8;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #fff5c8;
    color: #464232;
    border-bottom: 1px solid #d8d0a0;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #ffe89c;
}

QMenu {
    background-color: #fffef0;
    color: #464232;
    border: 1px solid #d8d0a0;
}

QMenu::item:selected {
    background-color: #ffe89c;
}

QScrollBar:vertical {
    border: 1px solid #d8d0a0;
    background: #fffef0;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #d8d0a0;
    background: #fffef0;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #e8e0b0;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #e8e0b0;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #d8d0a0;
    border-radius: 4px;
    text-align: center;
    background-color: #fffef0;
}

QProgressBar::chunk {
    background-color: #ffdb58;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)