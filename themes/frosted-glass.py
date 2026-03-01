from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#20304060"
# window_text = "#e0f0ff"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "8pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#25354560"
# group_border_color = "#40608080"
# group_border_width = "1px"
# group_border_radius = "12px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#c0d0e0"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#30405060"
# input_text = "#e0f0ff"
# input_border_color = "#50709080"
# input_border_width = "1px"
# input_border_radius = "8px"
# input_padding = "0px"
# input_selection_bg = "#40608080"
# input_selection_text = "white"
# input_placeholder = "#8090a0"

# --- Buttons ---
# button_bg = "#35455560"
# button_text = "#ffffff"
# button_border_color = "#6080a080"
# button_border_width = "1px"
# button_border_radius = "8px"
# button_padding = "8px 16px"
# button_min_width = "80px"
# button_min_height = "30px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#40506080"
# button_hover_border = "#00d4ff80"
# button_pressed_bg = "#20304060"
# button_pressed_border = "#00d4ff"
# button_disabled_bg = "#30405040"
# button_disabled_text = "#607080"
# button_disabled_border = "#50709060"

# --- Menu Bar ---
# menubar_bg = "#28384860"
# menubar_text = "#e0f0ff"
# menubar_border = "#50709080"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#40608060"
# menubar_item_bg_selected = "#40608080"
# menubar_item_text = "#e0f0ff"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#30405080"
# menu_border = "#50709080"
# menu_border_radius = "8px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#40608060"
# menu_item_bg_selected = "#40608080"
# menu_item_text = "#e0f0ff"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#50709080"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#30405060"
# scrollbar_border = "#50709080"
# scrollbar_handle_bg = "#40608080"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#50709080"
# scrollbar_handle_pressed_bg = "#6080a080"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#30405060"
# progressbar_border = "#50709080"
# progressbar_border_radius = "8px"
# progressbar_chunk_bg = "#00d4ff80"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#30405080"
# tooltip_text = "#e0f0ff"
# tooltip_border = "#50709080"
# tooltip_border_radius = "8px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#30405060"
# checkbox_border = "#50709080"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#00d4ff80"
# checkbox_checked_border = "#00d4ff"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#30405060"
# slider_groove_border = "#50709080"
# slider_handle_bg = "#00d4ff80"
# slider_handle_border = "#00d4ff"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(32, 48, 64, 96))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 240, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(48, 64, 80, 96))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(37, 53, 69, 96))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(48, 64, 80, 128))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 240, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(224, 240, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 69, 85, 96))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 212, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 212, 255, 128))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(128, 144, 160))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 8pt;
    color: #e0f0ff;
    background-color: rgba(32, 48, 64, 96);
    border-radius: 12px;
}

QGroupBox { 
    border: 1px solid rgba(64, 96, 128, 128);
    border-radius: 12px;
    margin-top: 1em;
    padding-top: 15px;
    background-color: rgba(37, 53, 69, 96);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #c0d0e0;
    background-color: transparent;
    font-weight: bold;
}

QListWidget, QTextEdit, QLineEdit {
    background-color: rgba(48, 64, 80, 96);
    color: #e0f0ff;
    border: 1px solid rgba(80, 112, 144, 128);
    border-radius: 8px;
    padding: 0px;
    selection-background-color: rgba(64, 96, 128, 128);
    selection-color: white;
}

QPushButton {
    background-color: rgba(53, 69, 85, 96);
    color: #ffffff;
    border: 1px solid rgba(96, 128, 160, 128);
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
    max-width: 80px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton:hover {
    background-color: rgba(64, 80, 96, 128);
    border-color: rgba(0, 212, 255, 128);
}

QPushButton:pressed {
    background-color: rgba(32, 48, 64, 96);
    border-color: #00d4ff;
}

QPushButton:disabled {
    color: #607080;
    background-color: rgba(48, 64, 80, 64);
    border-color: rgba(80, 112, 144, 96);
}

#control_container {
    background-color: transparent;
}

QMenuBar {
    background-color: rgba(40, 56, 72, 96);
    color: #e0f0ff;
    border-bottom: 1px solid rgba(80, 112, 144, 128);
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: rgba(64, 96, 128, 128);
    color: #ffffff;
}

QMenu {
    background-color: rgba(48, 64, 80, 128);
    color: #e0f0ff;
    border: 1px solid rgba(80, 112, 144, 128);
    border-radius: 8px;
}

QMenu::item {
    padding: 4px 24px 4px 8px;
}

QMenu::item:selected {
    background-color: rgba(64, 96, 128, 128);
    color: #ffffff;
}

QScrollBar:vertical {
    border: 1px solid rgba(80, 112, 144, 128);
    background: rgba(48, 64, 80, 96);
    width: 15px;
    margin: 0;
    border-radius: 7px;
}

QScrollBar:horizontal {
    border: 1px solid rgba(80, 112, 144, 128);
    background: rgba(48, 64, 80, 96);
    height: 30px;
    margin: 0;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background: rgba(64, 96, 128, 128);
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:horizontal {
    background: rgba(64, 96, 128, 128);
    min-width: 20px;
    border-radius: 7px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

QProgressBar {
    border: 1px solid rgba(80, 112, 144, 128);
    border-radius: 8px;
    text-align: center;
    background-color: rgba(48, 64, 80, 96);
}

QProgressBar::chunk {
    background-color: rgba(0, 212, 255, 128);
    border-radius: 0px;
}

QToolTip {
    background-color: rgba(48, 64, 80, 128);
    color: #e0f0ff;
    border: 1px solid rgba(80, 112, 144, 128);
    border-radius: 8px;
    padding: 4px 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid rgba(80, 112, 144, 128);
    background-color: rgba(48, 64, 80, 96);
}

QCheckBox::indicator:checked {
    background-color: rgba(0, 212, 255, 128);
    border: 1px solid #00d4ff;
}

QSlider::groove:horizontal {
    border: 1px solid rgba(80, 112, 144, 128);
    background: rgba(48, 64, 80, 96);
    height: 16px;
    border-radius: 8px;
}

QSlider::handle:horizontal {
    background: rgba(0, 212, 255, 128);
    border: 1px solid #00d4ff;
    width: 16px;
    height: 16px;
    border-radius: 8px;
}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)