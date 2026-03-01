from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#2e1a1e"
# window_text = "#f0d0d8"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#2e1a1e"
# group_border_color = "#3d2528"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#e8c0c8"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#3d2528"
# input_text = "#f0d0d8"
# input_border_color = "#503538"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#604548"
# input_selection_text = "white"
# input_placeholder = "#a08088"

# --- Buttons ---
# button_bg = "#453035"
# button_text = "#f0d0d8"
# button_border_color = "#503538"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#554045"
# button_hover_border = "#dc143c"
# button_pressed_bg = "#2e1a1e"
# button_pressed_border = "#dc143c"
# button_disabled_bg = "#3d2528"
# button_disabled_text = "#806068"
# button_disabled_border = "#503538"

# --- Menu Bar ---
# menubar_bg = "#352025"
# menubar_text = "#f0d0d8"
# menubar_border = "#503538"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#554045"
# menubar_item_bg_selected = "#554045"
# menubar_item_text = "#f0d0d8"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#3d2528"
# menu_border = "#503538"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#554045"
# menu_item_bg_selected = "#554045"
# menu_item_text = "#f0d0d8"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#503538"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#3d2528"
# scrollbar_border = "#503538"
# scrollbar_handle_bg = "#554045"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#655055"
# scrollbar_handle_pressed_bg = "#756065"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#3d2528"
# progressbar_border = "#503538"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#dc143c"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#3d2528"
# tooltip_text = "#f0d0d8"
# tooltip_border = "#503538"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#3d2528"
# checkbox_border = "#503538"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#dc143c"
# checkbox_checked_border = "#dc143c"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#3d2528"
# slider_groove_border = "#503538"
# slider_handle_bg = "#dc143c"
# slider_handle_border = "#bc042c"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(46, 26, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 208, 216))
    palette.setColor(QPalette.ColorRole.Base, QColor(61, 37, 40))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(69, 48, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(240, 208, 216))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 208, 216))
    palette.setColor(QPalette.ColorRole.Text, QColor(240, 208, 216))
    palette.setColor(QPalette.ColorRole.Button, QColor(69, 48, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 208, 216))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(220, 20, 60))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(220, 20, 60))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(160, 128, 136))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #f0d0d8;
    background-color: #2e1a1e;
}

QGroupBox { 
    border: 2px solid #3d2528;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #2e1a1e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #e8c0c8;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #3d2528;
    color: #f0d0d8;
    border: 1px solid #503538;
    border-radius: 4px;
    padding: 0px;
    selection-background-color: #604548;
    selection-color: white;
}

QPushButton {
    background-color: #453035;
    color: #f0d0d8;
    border: 1px solid #503538;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #554045;
    border-color: #dc143c;
}

QPushButton:pressed {
    background-color: #2e1a1e;
}

QPushButton:disabled {
    color: #806068;
    background-color: #3d2528;
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #352025;
    color: #f0d0d8;
    border-bottom: 1px solid #503538;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #554045;
}

QMenu {
    background-color: #3d2528;
    color: #f0d0d8;
    border: 1px solid #503538;
}

QMenu::item:selected {
    background-color: #554045;
}

QScrollBar:vertical {
    border: 1px solid #503538;
    background: #3d2528;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid #503538;
    background: #3d2528;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #554045;
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: #554045;
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid #503538;
    border-radius: 4px;
    text-align: center;
    background-color: #3d2528;
}

QProgressBar::chunk {
    background-color: #dc143c;
    border-radius: 0px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)