from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#1e1e1e"
# window_text = "#e0e0e0"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#1e1e1e"
# group_border_color = "#141414"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#D8D8D8"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#2d2d30"
# input_text = "#e0e0e0"
# input_border_color = "#404040"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#5F5F5F"
# input_selection_text = "white"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#333337"
# button_text = "#e0e0e0"
# button_border_color = "#404040"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#3a3a3d"
# button_hover_border = "#00ccff"
# button_pressed_bg = "#1e1e1e"
# button_pressed_border = "#00ccff"
# button_disabled_bg = "#2d2d30"
# button_disabled_text = "#777"
# button_disabled_border = "#404040"

# --- Menu Bar ---
# menubar_bg = "#252526"
# menubar_text = "#e0e0e0"
# menubar_border = "#404040"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#3e3e40"
# menubar_item_bg_selected = "#3e3e40"
# menubar_item_text = "#e0e0e0"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#2d2d30"
# menu_border = "#404040"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#3e3e40"
# menu_item_bg_selected = "#3e3e40"
# menu_item_text = "#e0e0e0"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#404040"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#2d2d30"
# scrollbar_border = "#573D3D"
# scrollbar_handle_bg = "#3e3e40"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#4f4f4f"
# scrollbar_handle_pressed_bg = "#5f5f5f"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#2d2d30"
# progressbar_border = "#404040"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#0078d4"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#2d2d30"
# tooltip_text = "#e0e0e0"
# tooltip_border = "#404040"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#2d2d30"
# checkbox_border = "#404040"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#0078d4"
# checkbox_checked_border = "#0078d4"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#2d2d30"
# slider_groove_border = "#404040"
# slider_handle_bg = "#0078d4"
# slider_handle_border = "#0066b8"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 127, 127))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #e0e0e0;
    background-color: #1e1e1e;
}

QGroupBox { 
    border: 2px solid #141414;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #1e1e1e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #D8D8D8;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #2d2d30;
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #5F5F5F;
    selection-color: white;
}

QPushButton {
    background-color: #333337;
    color: #e0e0e0;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #3a3a3d;
    border-color: #00ccff;
}

QPushButton:pressed {
    background-color: #1e1e1e;
}

QPushButton:disabled {
    color: #777;
    background-color: #2d2d30;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #252526;
    color: #e0e0e0;
    border-bottom: 1px solid #404040;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #3e3e40;
}

QMenu {
    background-color: #2d2d30;
    color: #e0e0e0;
    border: 1px solid #404040;
}

QMenu::item:selected {
    background-color: #3e3e40;
}

QScrollBar:vertical {
    border: 1px solid #573D3D;
    background: #2d2d30;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #404040;
    background: #2d2d30;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #3e3e40;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #3e3e40;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #404040;
    border-radius: 4px;
    text-align: center;
    background-color: #2d2d30;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)