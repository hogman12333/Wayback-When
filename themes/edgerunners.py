from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#0d0814"
# window_text = "#ff7eb9"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#120a1a"
# group_border_color = "#ff2a6d80"
# group_border_width = "2px"
# group_border_radius = "6px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#ff2a6d"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#1a0f25"
# input_text = "#ff7eb9"
# input_border_color = "#ff7eb980"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#ff7eb940"
# input_selection_text = "#0d0814"
# input_placeholder = "#ff7eb960"

# --- Buttons ---
# button_bg = "#1f1230"
# button_text = "#ff7eb9"
# button_border_color = "#ff2a6d"
# button_border_width = "2px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#2a1840"
# button_hover_border = "#ff7eb9"
# button_pressed_bg = "#0d0814"
# button_pressed_border = "#ff7eb9"
# button_disabled_bg = "#1a0f25"
# button_disabled_text = "#ff7eb940"
# button_disabled_border = "#ff2a6d40"

# --- Menu Bar ---
# menubar_bg = "#100818"
# menubar_text = "#ff7eb9"
# menubar_border = "#ff2a6d80"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#ff2a6d30"
# menubar_item_bg_selected = "#ff2a6d40"
# menubar_item_text = "#ff7eb9"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#1a0f25"
# menu_border = "#ff2a6d80"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#ff2a6d30"
# menu_item_bg_selected = "#ff2a6d40"
# menu_item_text = "#ff7eb9"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#ff2a6d80"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#1a0f25"
# scrollbar_border = "#ff2a6d80"
# scrollbar_handle_bg = "#ff2a6d60"
# scrollbar_handle_border_radius = "4px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#ff2a6d80"
# scrollbar_handle_pressed_bg = "#ff2a6d"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#1a0f25"
# progressbar_border = "#ff2a6d80"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#ff7eb9"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#1a0f25"
# tooltip_text = "#ff7eb9"
# tooltip_border = "#ff2a6d"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#1a0f25"
# checkbox_border = "#ff2a6d80"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#ff7eb9"
# checkbox_checked_border = "#ff7eb9"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#1a0f25"
# slider_groove_border = "#ff2a6d80"
# slider_handle_bg = "#ff7eb9"
# slider_handle_border = "#ff7eb9"
# slider_handle_radius = "6px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(13, 8, 20))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 126, 185))
    palette.setColor(QPalette.ColorRole.Base, QColor(26, 15, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(31, 18, 48))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 15, 37))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 126, 185))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 126, 185))
    palette.setColor(QPalette.ColorRole.Button, QColor(31, 18, 48))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 126, 185))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 42, 109))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 42, 109, 128))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(13, 8, 20))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(255, 126, 185, 96))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #ff7eb9;
    background-color: #0d0814;
}

QGroupBox { 
    border: 2px solid rgba(255, 42, 109, 128);
    border-radius: 6px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: #120a1a;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #ff2a6d;
    background-color: transparent;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: #1a0f25;
    color: #ff7eb9;
    border: 1px solid rgba(255, 126, 185, 128);
    border-radius: 4px;
    padding: 0px;
    selection-background-color: rgba(255, 126, 185, 64);
    selection-color: #0d0814;
}

QPushButton {
    background-color: #1f1230;
    color: #ff7eb9;
    border: 2px solid #ff2a6d;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: #2a1840;
    border-color: #ff7eb9;
}

QPushButton:pressed {
    background-color: #0d0814;
    border-color: #ff7eb9;
}

QPushButton:disabled {
    color: rgba(255, 126, 185, 64);
    background-color: #1a0f25;
    border-color: rgba(255, 42, 109, 64);
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: #100818;
    color: #ff7eb9;
    border-bottom: 1px solid rgba(255, 42, 109, 128);
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: rgba(255, 42, 109, 48);
    color: #ffffff;
}

QMenu {
    background-color: #1a0f25;
    color: #ff7eb9;
    border: 1px solid rgba(255, 42, 109, 128);
    border-radius: 4px;
}

QMenu::item {
    padding: 4px 24px 4px 8px;
}

QMenu::item:selected {
    background-color: rgba(255, 42, 109, 64);
    color: #ffffff;
}

QScrollBar:vertical {
    border: 1px solid rgba(255, 42, 109, 128);
    background: #1a0f25;
    width: 15px;
    margin: 0;
}

QScrollBar:horizontal {
    border: 1px solid rgba(255, 42, 109, 128);
    background: #1a0f25;
    height: 30px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: rgba(255, 42, 109, 96);
    min-height: 40px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 42, 109, 96);
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid rgba(255, 42, 109, 128);
    border-radius: 4px;
    text-align: center;
    background-color: #1a0f25;
}

QProgressBar::chunk {
    background-color: #ff7eb9;
    border-radius: 0px;
}

QToolTip {
    background-color: #1a0f25;
    color: #ff7eb9;
    border: 1px solid #ff2a6d;
    border-radius: 4px;
    padding: 4px 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid rgba(255, 42, 109, 128);
    background-color: #1a0f25;
}

QCheckBox::indicator:checked {
    background-color: #ff7eb9;
    border: 1px solid #ff7eb9;
}

QSlider::groove:horizontal {
    border: 1px solid rgba(255, 42, 109, 128);
    background: #1a0f25;
    height: 16px;
    border-radius: 6px;
}

QSlider::handle:horizontal {
    background: #ff7eb9;
    border: 1px solid #ff7eb9;
    width: 16px;
    height: 16px;
    border-radius: 6px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)