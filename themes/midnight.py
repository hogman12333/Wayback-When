from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#0a0a0f"
# window_text = "#c0c0d0"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#0a0a0f"
# group_border_color = "#151520"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#b0b0c0"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#12121a"
# input_text = "#c0c0d0"
# input_border_color = "#252535"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#303045"
# input_selection_text = "white"
# input_placeholder = "#707080"

# --- Buttons ---
# button_bg = "#1a1a25"
# button_text = "#c0c0d0"
# button_border_color = "#252535"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#252535"
# button_hover_border = "#5060ff"
# button_pressed_bg = "#0a0a0f"
# button_pressed_border = "#5060ff"
# button_disabled_bg = "#12121a"
# button_disabled_text = "#505060"
# button_disabled_border = "#252535"

# --- Menu Bar ---
# menubar_bg = "#0f0f15"
# menubar_text = "#c0c0d0"
# menubar_border = "#252535"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#252535"
# menubar_item_bg_selected = "#252535"
# menubar_item_text = "#c0c0d0"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#12121a"
# menu_border = "#252535"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#252535"
# menu_item_bg_selected = "#252535"
# menu_item_text = "#c0c0d0"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#252535"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#12121a"
# scrollbar_border = "#252535"
# scrollbar_handle_bg = "#252535"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#353545"
# scrollbar_handle_pressed_bg = "#454555"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#12121a"
# progressbar_border = "#252535"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#5060ff"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#12121a"
# tooltip_text = "#c0c0d0"
# tooltip_border = "#252535"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#12121a"
# checkbox_border = "#252535"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#5060ff"
# checkbox_checked_border = "#5060ff"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#12121a"
# slider_groove_border = "#252535"
# slider_handle_bg = "#5060ff"
# slider_handle_border = "#4050e0"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 15))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(192, 192, 208))
    palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 26))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(26, 26, 37))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(192, 192, 208))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(192, 192, 208))
    palette.setColor(QPalette.ColorRole.Text, QColor(192, 192, 208))
    palette.setColor(QPalette.ColorRole.Button, QColor(26, 26, 37))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(192, 192, 208))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(80, 96, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 96, 255))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(112, 112, 128))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #c0c0d0;
    background-color: #0a0a0f;
}

QGroupBox { 
    border: 2px solid #151520;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #0a0a0f;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #b0b0c0;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #12121a;
    color: #c0c0d0;
    border: 1px solid #252535;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #303045;
    selection-color: white;
}

QPushButton {
    background-color: #1a1a25;
    color: #c0c0d0;
    border: 1px solid #252535;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #252535;
    border-color: #5060ff;
}

QPushButton:pressed {
    background-color: #0a0a0f;
}

QPushButton:disabled {
    color: #505060;
    background-color: #12121a;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #0f0f15;
    color: #c0c0d0;
    border-bottom: 1px solid #252535;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #252535;
}

QMenu {
    background-color: #12121a;
    color: #c0c0d0;
    border: 1px solid #252535;
}

QMenu::item:selected {
    background-color: #252535;
}

QScrollBar:vertical {
    border: 1px solid #252535;
    background: #12121a;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #252535;
    background: #12121a;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #252535;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #252535;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #252535;
    border-radius: 4px;
    text-align: center;
    background-color: #12121a;
}

QProgressBar::chunk {
    background-color: #5060ff;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)