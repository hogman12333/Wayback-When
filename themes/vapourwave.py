from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
window_bg = "#2d1b4e80"
window_text = "#ff9ff3"
window_font_family = '"Segoe UI", Arial, sans-serif'
window_font_size = "8pt"
window_font_weight = "normal"

# --- Group Box ---
group_bg = "#3d2b5e80"
group_border_color = "#ff9ff360"
group_border_width = "2px"
group_border_radius = "12px"
group_margin_top = "1em"
group_padding_top = "15px"
group_title_color = "#ff9ff3"
group_title_bg = "transparent"
group_title_padding = "0 8px 0 8px"
group_title_left = "10px"
group_title_font_weight = "bold"

# --- Input Elements ---
input_bg = "#48386880"
input_text = "#ff9ff3"
input_border_color = "#ff9ff380"
input_border_width = "1px"
input_border_radius = "8px"
input_padding = "0px"
input_selection_bg = "#ff9ff340"
input_selection_text = "#2d1b4e"
input_placeholder = "#cc88cc"

# --- Buttons ---
button_bg = "#50407080"
button_text = "#ffffff"
button_border_color = "#ff9ff3"
button_border_width = "2px"
button_border_radius = "10px"
button_padding = "8px 16px"
button_min_width = "80px"
button_min_height = "30px"
button_font_weight = "bold"

# Button States
button_hover_bg = "#60508080"
button_hover_border = "#00ffff"
button_pressed_bg = "#2d1b4e80"
button_pressed_border = "#ff9ff3"
button_disabled_bg = "#48386840"
button_disabled_text = "#cc88cc"
button_disabled_border = "#ff9ff340"

# --- Menu Bar ---
menubar_bg = "#35255580"
menubar_text = "#ff9ff3"
menubar_border = "#ff9ff380"
menubar_border_width = "1px"
menubar_item_padding = "4px 8px"
menubar_item_spacing = "2px"
menubar_corner_radius = "2px"

# Menu Bar Items
menubar_item_bg = "transparent"
menubar_item_bg_hover = "#ff9ff330"
menubar_item_bg_selected = "#ff9ff340"
menubar_item_text = "#ff9ff3"
menubar_item_text_hover = "#ffffff"
menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
menu_bg = "#48386880"
menu_border = "#ff9ff380"
menu_border_radius = "10px"
menu_padding = "2px"
menu_margin = "0px"

# Menu Items
menu_item_padding = "4px 24px 4px 8px"
menu_item_bg_hover = "#ff9ff330"
menu_item_bg_selected = "#ff9ff340"
menu_item_text = "#ff9ff3"
menu_item_text_hover = "#ffffff"
menu_item_text_selected = "#ffffff"
menu_separator_color = "#ff9ff380"

# --- Scroll Bars ---
scrollbar_width = "15px"
scrollbar_height = "30px"
scrollbar_bg = "#48386880"
scrollbar_border = "#ff9ff380"
scrollbar_handle_bg = "#ff9ff360"
scrollbar_handle_border_radius = "7px"
scrollbar_handle_min_height = "40px"
scrollbar_handle_min_width = "20px"
scrollbar_handle_hover_bg = "#ff9ff380"
scrollbar_handle_pressed_bg = "#ff9ff3"
scrollbar_add_line = "none"
scrollbar_sub_line = "none"

# --- Progress Bar ---
progressbar_bg = "#48386880"
progressbar_border = "#ff9ff380"
progressbar_border_radius = "10px"
progressbar_chunk_bg = "#00ffff80"
progressbar_chunk_border_radius = "0px"
progressbar_text_align = "center"

# --- Tooltips ---
tooltip_bg = "#48386880"
tooltip_text = "#ff9ff3"
tooltip_border = "#ff9ff3"
tooltip_border_radius = "10px"
tooltip_padding = "4px 8px"

# --- Special Widgets ---
control_container_bg = "transparent"

# --- Checkboxes/Radios ---
checkbox_bg = "#48386880"
checkbox_border = "#ff9ff380"
checkbox_border_radius = "3px"
checkbox_checked_bg = "#ff9ff3"
checkbox_checked_border = "#ff9ff3"
checkbox_size = "16px"

# --- Sliders ---
slider_groove_bg = "#48386880"
slider_groove_border = "#ff9ff380"
slider_handle_bg = "#00ffff80"
slider_handle_border = "#00ffff"
slider_handle_radius = "8px"
slider_handle_width = "16px"
slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====


def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(45, 27, 78, 128))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 159, 243))
    palette.setColor(QPalette.ColorRole.Base, QColor(72, 56, 104, 128))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(61, 43, 94, 128))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(72, 56, 104, 128))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 159, 243))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 159, 243))
    palette.setColor(QPalette.ColorRole.Button, QColor(80, 64, 112, 128))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 255, 255))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 255, 255, 128))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(45, 27, 78))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(204, 136, 204))
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
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)