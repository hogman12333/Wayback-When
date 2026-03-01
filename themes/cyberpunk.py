from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#0a0a0f"
# window_text = "#00ff9f"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#0f0f1a"
# group_border_color = "#ff005580"
# group_border_width = "2px"
# group_border_radius = "4px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#ff0055"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#151525"
# input_text = "#00ff9f"
# input_border_color = "#00ff9f80"
# input_border_width = "1px"
# input_border_radius = "2px"
# input_padding = "0px"
# input_selection_bg = "#00ff9f40"
# input_selection_text = "#000000"
# input_placeholder = "#00ff9f60"

# --- Buttons ---
# button_bg = "#1a1a30"
# button_text = "#00ff9f"
# button_border_color = "#ff0055"
# button_border_width = "2px"
# button_border_radius = "2px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#252540"
# button_hover_border = "#00ff9f"
# button_pressed_bg = "#0a0a0f"
# button_pressed_border = "#00ff9f"
# button_disabled_bg = "#151525"
# button_disabled_text = "#00ff9f40"
# button_disabled_border = "#ff005540"

# --- Menu Bar ---
# menubar_bg = "#0d0d15"
# menubar_text = "#00ff9f"
# menubar_border = "#ff005580"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#ff005530"
# menubar_item_bg_selected = "#ff005540"
# menubar_item_text = "#00ff9f"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#151525"
# menu_border = "#ff005580"
# menu_border_radius = "2px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#ff005530"
# menu_item_bg_selected = "#ff005540"
# menu_item_text = "#00ff9f"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#ff005580"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#151525"
# scrollbar_border = "#ff005580"
# scrollbar_handle_bg = "#ff005560"
# scrollbar_handle_border_radius = "2px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#ff005580"
# scrollbar_handle_pressed_bg = "#ff0055"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#151525"
# progressbar_border = "#ff005580"
# progressbar_border_radius = "2px"
# progressbar_chunk_bg = "#00ff9f"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#151525"
# tooltip_text = "#00ff9f"
# tooltip_border = "#ff0055"
# tooltip_border_radius = "2px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#151525"
# checkbox_border = "#ff005580"
# checkbox_border_radius = "2px"
# checkbox_checked_bg = "#00ff9f"
# checkbox_checked_border = "#00ff9f"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#151525"
# slider_groove_border = "#ff005580"
# slider_handle_bg = "#ff0055"
# slider_handle_border = "#ff0055"
# slider_handle_radius = "4px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 15))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 159))
    palette.setColor(QPalette.ColorRole.Base, QColor(21, 21, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(26, 26, 48))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(21, 21, 37))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 255, 159))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 159))
    palette.setColor(QPalette.ColorRole.Button, QColor(26, 26, 48))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 255, 159))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 85))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 0, 85, 128))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(0, 255, 159, 96))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #00ff9f;
    background-color: #0a0a0f;
}

QGroupBox { 
    border: 2px solid rgba(255, 0, 85, 128);
    border-radius: 4px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #0f0f1a;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #ff0055;
    background-color: transparent;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #151525;
    color: #00ff9f;
    border: 1px solid rgba(0, 255, 159, 128);
    border-radius: 2px;
    padding: 0px;
    selection-background-color: rgba(0, 255, 159, 64);
    selection-color: #000000;
}

QPushButton {
    background-color: #1a1a30;
    color: #00ff9f;
    border: 2px solid #ff0055;
    border-radius: 2px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #252540;
    border-color: #00ff9f;
}

QPushButton:pressed {
    background-color: #0a0a0f;
    border-color: #00ff9f;
}

QPushButton:disabled {
    color: rgba(0, 255, 159, 64);
    background-color: #151525;
    border-color: rgba(255, 0, 85, 64);
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #0d0d15;
    color: #00ff9f;
    border-bottom: 1px solid rgba(255, 0, 85, 128);
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: rgba(255, 0, 85, 64);
    color: #ffffff;
}

QMenu {
    background-color: #151525;
    color: #00ff9f;
    border: 1px solid rgba(255, 0, 85, 128);
    border-radius: 2px;
}

QMenu::item {
    padding: 4px 24px 4px 8px;
}

QMenu::item:selected {
    background-color: rgba(255, 0, 85, 64);
    color: #ffffff;
}

QScrollBar:vertical {
    border: 1px solid rgba(255, 0, 85, 128);
    background: #151525;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid rgba(255, 0, 85, 128);
    background: #151525;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: rgba(255, 0, 85, 96);
    min-height: 40px;
    border-radius: 2px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 0, 85, 96);
    min-width: 20px;
    border-radius: 2px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid rgba(255, 0, 85, 128);
    border-radius: 2px;
    text-align: center;
    background-color: #151525;
}

QProgressBar::chunk {
    background-color: #00ff9f;
    border-radius: 0px;
}

QToolTip {
    background-color: #151525;
    color: #00ff9f;
    border: 1px solid #ff0055;
    border-radius: 2px;
    padding: 4px 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 2px;
    border: 1px solid rgba(255, 0, 85, 128);
    background-color: #151525;
}

QCheckBox::indicator:checked {
    background-color: #00ff9f;
    border: 1px solid #00ff9f;
}

QSlider::groove:horizontal {
    border: 1px solid rgba(255, 0, 85, 128);
    background: #151525;
    height: 16px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #ff0055;
    border: 1px solid #ff0055;
    width: 16px;
    height: 16px;
    border-radius: 4px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)