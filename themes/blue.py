from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#141e28"
# window_text = "#dce6f0"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "11pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#141e28"
# group_border_color = "#0d141a"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#c8d8e8"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#1d2d3d"
# input_text = "#dce6f0"
# input_border_color = "#304050"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#3a5a7a"
# input_selection_text = "white"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#253545"
# button_text = "#dce6f0"
# button_border_color = "#304050"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "120px"
# button_min_height = "40px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#2d3d4d"
# button_hover_border = "#00bfff"
# button_pressed_bg = "#141e28"
# button_pressed_border = "#00bfff"
# button_disabled_bg = "#1d2d3d"
# button_disabled_text = "#6a7a8a"
# button_disabled_border = "#304050"

# --- Menu Bar ---
# menubar_bg = "#1a2632"
# menubar_text = "#dce6f0"
# menubar_border = "#304050"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#2d3d4d"
# menubar_item_bg_selected = "#2d3d4d"
# menubar_item_text = "#dce6f0"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#1d2d3d"
# menu_border = "#304050"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#2d3d4d"
# menu_item_bg_selected = "#2d3d4d"
# menu_item_text = "#dce6f0"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#304050"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "30px"
# scrollbar_bg = "#1d2d3d"
# scrollbar_border = "#2a4a6a"
# scrollbar_handle_bg = "#2d3d4d"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "40px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#3a4d5d"
# scrollbar_handle_pressed_bg = "#4a5d6d"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#1d2d3d"
# progressbar_border = "#304050"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#0096dc"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#1d2d3d"
# tooltip_text = "#dce6f0"
# tooltip_border = "#304050"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#1d2d3d"
# checkbox_border = "#304050"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#0096dc"
# checkbox_checked_border = "#0096dc"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#1d2d3d"
# slider_groove_border = "#304050"
# slider_handle_bg = "#2d3d4d"
# slider_handle_border = "#00bfff"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(20, 30, 40))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(15, 25, 35))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(25, 35, 45))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(35, 45, 55))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 230, 240))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.cyan)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 150, 220))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 147, 167))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #dce6f0;
        background-color: #141e28;
    }

    QGroupBox { 
        border: 2px solid #0d141a;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #141e28;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #c8d8e8;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #1d2d3d;
        color: #dce6f0;
        border: 1px solid #304050;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #3a5a7a;
        selection-color: white;
    }

    QPushButton {
        background-color: #253545;
        color: #dce6f0;
        border: 1px solid #304050;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        min-width: 120px;
        max-width: 120px;
        min-height: 40px;
        max-height: 40px;
    }

    QPushButton:hover {
        background-color: #2d3d4d;
        border-color: #00bfff;
    }

    QPushButton:pressed {
        background-color: #141e28;
    }

    QPushButton:disabled {
        color: #6a7a8a;
        background-color: #1d2d3d;
    }

    #control_container {
        background-color: transparent;
    }

    QMenuBar {
        background-color: #1a2632;
        color: #dce6f0;
        border-bottom: 1px solid #304050;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #2d3d4d;
    }

    QMenu {
        background-color: #1d2d3d;
        color: #dce6f0;
        border: 1px solid #304050;
    }

    QMenu::item:selected {
        background-color: #2d3d4d;
    }

    QScrollBar:vertical {
        border: 1px solid #2a4a6a;
        background: #1d2d3d;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #304050;
        background: #1d2d3d;
        height: 30px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #2d3d4d;
        min-height: 40px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #2d3d4d;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #304050;
        border-radius: 4px;
        text-align: center;
        background-color: #1d2d3d;
    }

    QProgressBar::chunk {
        background-color: #0096dc;
        border-radius: 0px;
    }
    """)

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)