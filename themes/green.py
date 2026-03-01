from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#1a2824"
# window_text = "#d0e8e0"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#1a2824"
# group_border_color = "#253530"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#c0d8d0"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#253530"
# input_text = "#d0e8e0"
# input_border_color = "#354540"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#455550"
# input_selection_text = "white"
# input_placeholder = "#809088"

# --- Buttons ---
# button_bg = "#2d3d38"
# button_text = "#d0e8e0"
# button_border_color = "#354540"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#354540"
# button_hover_border = "#2ec4b6"
# button_pressed_bg = "#1a2824"
# button_pressed_border = "#2ec4b6"
# button_disabled_bg = "#253530"
# button_disabled_text = "#708078"
# button_disabled_border = "#354540"

# --- Menu Bar ---
# menubar_bg = "#203028"
# menubar_text = "#d0e8e0"
# menubar_border = "#354540"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#354540"
# menubar_item_bg_selected = "#354540"
# menubar_item_text = "#d0e8e0"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#253530"
# menu_border = "#354540"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#354540"
# menu_item_bg_selected = "#354540"
# menu_item_text = "#d0e8e0"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#354540"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#253530"
# scrollbar_border = "#354540"
# scrollbar_handle_bg = "#354540"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#455550"
# scrollbar_handle_pressed_bg = "#556560"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#253530"
# progressbar_border = "#354540"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#2ec4b6"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#253530"
# tooltip_text = "#d0e8e0"
# tooltip_border = "#354540"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#253530"
# checkbox_border = "#354540"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#2ec4b6"
# checkbox_checked_border = "#2ec4b6"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#253530"
# slider_groove_border = "#354540"
# slider_handle_bg = "#2ec4b6"
# slider_handle_border = "#1ea89a"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 40, 36))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(208, 232, 224))
    palette.setColor(QPalette.ColorRole.Base, QColor(37, 53, 48))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 61, 56))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(208, 232, 224))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(208, 232, 224))
    palette.setColor(QPalette.ColorRole.Text, QColor(208, 232, 224))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 61, 56))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(208, 232, 224))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(46, 196, 182))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(46, 196, 182))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 144, 136))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #d0e8e0;
    background-color: #1a2824;
}

QGroupBox { 
    border: 2px solid #253530;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #1a2824;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #c0d8d0;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #253530;
    color: #d0e8e0;
    border: 1px solid #354540;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #455550;
    selection-color: white;
}

QPushButton {
    background-color: #2d3d38;
    color: #d0e8e0;
    border: 1px solid #354540;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #354540;
    border-color: #2ec4b6;
}

QPushButton:pressed {
    background-color: #1a2824;
}

QPushButton:disabled {
    color: #708078;
    background-color: #253530;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #203028;
    color: #d0e8e0;
    border-bottom: 1px solid #354540;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #354540;
}

QMenu {
    background-color: #253530;
    color: #d0e8e0;
    border: 1px solid #354540;
}

QMenu::item:selected {
    background-color: #354540;
}

QScrollBar:vertical {
    border: 1px solid #354540;
    background: #253530;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #354540;
    background: #253530;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #354540;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #354540;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #354540;
    border-radius: 4px;
    text-align: center;
    background-color: #253530;
}

QProgressBar::chunk {
    background-color: #2ec4b6;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)