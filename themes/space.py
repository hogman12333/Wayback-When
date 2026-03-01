from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
window_bg = "#050510"
window_text = "#a0a0ff"
window_font_family = '"Segoe UI", Arial, sans-serif'
window_font_size = "8pt"
window_font_weight = "normal"

# --- Group Box ---
group_bg = "#0a0a18"
group_border_color = "#6060ff40"
group_border_width = "2px"
group_border_radius = "8px"
group_margin_top = "1em"
group_padding_top = "15px"
group_title_color = "#8080ff"
group_title_bg = "transparent"
group_title_padding = "0 8px 0 8px"
group_title_left = "10px"
group_title_font_weight = "bold"

# --- Input Elements ---
input_bg = "#101020"
input_text = "#a0a0ff"
input_border_color = "#6060ff60"
input_border_width = "1px"
input_border_radius = "6px"
input_padding = "0px"
input_selection_bg = "#6060ff30"
input_selection_text = "#ffffff"
input_placeholder = "#505080"

# --- Buttons ---
button_bg = "#151528"
button_text = "#a0a0ff"
button_border_color = "#6060ff80"
button_border_width = "2px"
button_border_radius = "8px"
button_padding = "8px 16px"
button_min_width = "80px"
button_min_height = "30px"
button_font_weight = "bold"

# Button States
button_hover_bg = "#1a1a30"
button_hover_border = "#8080ff"
button_pressed_bg = "#050510"
button_pressed_border = "#8080ff"
button_disabled_bg = "#101020"
button_disabled_text = "#404060"
button_disabled_border = "#6060ff40"

# --- Menu Bar ---
menubar_bg = "#080815"
menubar_text = "#a0a0ff"
menubar_border = "#6060ff60"
menubar_border_width = "1px"
menubar_item_padding = "4px 8px"
menubar_item_spacing = "2px"
menubar_corner_radius = "2px"

# Menu Bar Items
menubar_item_bg = "transparent"
menubar_item_bg_hover = "#6060ff20"
menubar_item_bg_selected = "#6060ff30"
menubar_item_text = "#a0a0ff"
menubar_item_text_hover = "#ffffff"
menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
menu_bg = "#101020"
menu_border = "#6060ff60"
menu_border_radius = "8px"
menu_padding = "2px"
menu_margin = "0px"

# Menu Items
menu_item_padding = "4px 24px 4px 8px"
menu_item_bg_hover = "#6060ff20"
menu_item_bg_selected = "#6060ff30"
menu_item_text = "#a0a0ff"
menu_item_text_hover = "#ffffff"
menu_item_text_selected = "#ffffff"
menu_separator_color = "#6060ff60"

# --- Scroll Bars ---
scrollbar_width = "15px"
scrollbar_height = "30px"
scrollbar_bg = "#101020"
scrollbar_border = "#6060ff60"
scrollbar_handle_bg = "#6060ff40"
scrollbar_handle_border_radius = "7px"
scrollbar_handle_min_height = "40px"
scrollbar_handle_min_width = "20px"
scrollbar_handle_hover_bg = "#6060ff60"
scrollbar_handle_pressed_bg = "#6060ff80"
scrollbar_add_line = "none"
scrollbar_sub_line = "none"

# --- Progress Bar ---
progressbar_bg = "#101020"
progressbar_border = "#6060ff60"
progressbar_border_radius = "8px"
progressbar_chunk_bg = "#8080ff"
progressbar_chunk_border_radius = "0px"
progressbar_text_align = "center"

# --- Tooltips ---
tooltip_bg = "#101020"
tooltip_text = "#a0a0ff"
tooltip_border = "#6060ff80"
tooltip_border_radius = "8px"
tooltip_padding = "4px 8px"

# --- Special Widgets ---
control_container_bg = "transparent"

# --- Checkboxes/Radios ---
checkbox_bg = "#101020"
checkbox_border = "#6060ff60"
checkbox_border_radius = "3px"
checkbox_checked_bg = "#8080ff"
checkbox_checked_border = "#8080ff"
checkbox_size = "16px"

# --- Sliders ---
slider_groove_bg = "#101020"
slider_groove_border = "#6060ff60"
slider_handle_bg = "#8080ff"
slider_handle_border = "#8080ff"
slider_handle_radius = "8px"
slider_handle_width = "16px"
slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(5, 5, 16))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(160, 160, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(16, 16, 32))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(21, 21, 40))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(16, 16, 32))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(160, 160, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(160, 160, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(21, 21, 40))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(160, 160, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(128, 128, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(128, 128, 255, 128))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(80, 80, 128))
    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet(f"""
QWidget {{
    font-family: {window_font_family};
    font-size: {window_font_size};
    color: {window_text};
    background-color: {window_bg};
}}

QGroupBox {{ 
    border: {group_border_width} solid {group_border_color};
    border-radius: {group_border_radius};
    margin-top: {group_margin_top};
    padding-top: {group_padding_top};
    background-color: {group_bg};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: {group_title_left};
    padding: {group_title_padding};
    color: {group_title_color};
    background-color: {group_title_bg};
    font-weight: {group_title_font_weight};
}}

QListWidget, QTextEdit, QLineEdit {{
    background-color: {input_bg};
    color: {input_text};
    border: {input_border_width} solid {input_border_color};
    border-radius: {input_border_radius};
    padding: {input_padding};
    selection-background-color: {input_selection_bg};
    selection-color: {input_selection_text};
}}

QPushButton {{
    background-color: {button_bg};
    color: {button_text};
    border: {button_border_width} solid {button_border_color};
    border-radius: {button_border_radius};
    padding: {button_padding};
    font-weight: {button_font_weight};
    min-width: {button_min_width};
    max-width: {button_min_width};
    min-height: {button_min_height};
    max-height: {button_min_height};
}}

QPushButton:hover {{
    background-color: {button_hover_bg};
    border-color: {button_hover_border};
}}

QPushButton:pressed {{
    background-color: {button_pressed_bg};
    border-color: {button_pressed_border};
}}

QPushButton:disabled {{
    color: {button_disabled_text};
    background-color: {button_disabled_bg};
    border-color: {button_disabled_border};
}}

#control_container {{
    background-color: {control_container_bg};
}}

QMenuBar {{
    background-color: {menubar_bg};
    color: {menubar_text};
    border-bottom: {menubar_border_width} solid {menubar_border};
}}

QMenuBar::item {{
    background-color: {menubar_item_bg};
    padding: {menubar_item_padding};
}}

QMenuBar::item:selected {{
    background-color: {menubar_item_bg_selected};
    color: {menubar_item_text_selected};
}}

QMenu {{
    background-color: {menu_bg};
    color: {menu_item_text};
    border: {menubar_border_width} solid {menu_border};
    border-radius: {menu_border_radius};
}}

QMenu::item {{
    padding: {menu_item_padding};
}}

QMenu::item:selected {{
    background-color: {menu_item_bg_selected};
    color: {menu_item_text_selected};
}}

QScrollBar:vertical {{
    border: {input_border_width} solid {scrollbar_border};
    background: {scrollbar_bg};
    width: {scrollbar_width};
    margin: 0;
}}

QScrollBar:horizontal {{
    border: {input_border_width} solid {scrollbar_border};
    background: {scrollbar_bg};
    height: {scrollbar_height};
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {scrollbar_handle_bg};
    min-height: {scrollbar_handle_min_height};
    border-radius: {scrollbar_handle_border_radius};
}}

QScrollBar::handle:horizontal {{
    background: {scrollbar_handle_bg};
    min-width: {scrollbar_handle_min_width};
    border-radius: {scrollbar_handle_border_radius};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    {scrollbar_add_line};
}}

QProgressBar {{
    border: {input_border_width} solid {progressbar_border};
    border-radius: {progressbar_border_radius};
    text-align: {progressbar_text_align};
    background-color: {progressbar_bg};
}}

QProgressBar::chunk {{
    background-color: {progressbar_chunk_bg};
    border-radius: {progressbar_chunk_border_radius};
}}
""")

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)