from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#f0f0f0"
# window_text = "#313030"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "11pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#fafafa"
# group_border_color = "#c0c0c0"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#1E1F20"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "white"
# input_text = "#242424"
# input_border_color = "#c0c0c0"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "6px"
# input_selection_bg = "#777777"
# input_selection_text = "white"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#f0f0f0"
# button_text = "#242424"
# button_border_color = "#c0c0c0"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "120px"
# button_min_height = "40px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#e0e0e0"
# button_hover_border = "#A1A1A1"
# button_pressed_bg = "#d0d0d0"
# button_pressed_border = "#A1A1A1"
# button_disabled_bg = "#f8f8f8"
# button_disabled_text = "#a0a0a0"
# button_disabled_border = "#c0c0c0"

# --- Menu Bar ---
# menubar_bg = "#f0f0f0"
# menubar_text = "#313030"
# menubar_border = "#c0c0c0"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#e0e0e0"
# menubar_item_bg_selected = "#e0e0e0"
# menubar_item_text = "#313030"
# menubar_item_text_hover = "#000000"
# menubar_item_text_selected = "#000000"

# --- Dropdown Menus ---
# menu_bg = "white"
# menu_border = "#c0c0c0"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#e0e0e0"
# menu_item_bg_selected = "#e0e0e0"
# menu_item_text = "#242424"
# menu_item_text_hover = "#000000"
# menu_item_text_selected = "#000000"
# menu_separator_color = "#c0c0c0"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "15px"
# scrollbar_bg = "#f0f0f0"
# scrollbar_border = "#c0c0c0"
# scrollbar_handle_bg = "#c0c0c0"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "20px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#b0b0b0"
# scrollbar_handle_pressed_bg = "#a0a0a0"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#f0f0f0"
# progressbar_border = "#c0c0c0"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#0078d4"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "white"
# tooltip_text = "#242424"
# tooltip_border = "#c0c0c0"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "white"
# checkbox_border = "#c0c0c0"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#0078d4"
# checkbox_checked_border = "#0078d4"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#f0f0f0"
# slider_groove_border = "#c0c0c0"
# slider_handle_bg = "#0078d4"
# slider_handle_border = "#0066b8"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====

def apply(app, widget):
    app.setPalette(QApplication.style().standardPalette())

    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #313030;
        background-color: #f0f0f0;
    }

    QGroupBox {
        border: 2px solid #c0c0c0;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #fafafa;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #1E1F20;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
        color: #242424;
        selection-background-color: #777777;
        selection-color: white;
    }

    QPushButton {
        padding: 8px 16px;
        border-radius: 4px;
        border: 1px solid #c0c0c0;
        background-color: #f0f0f0;
        font-weight: bold;
        min-width: 120px;
        max-width: 120px;
        min-height: 40px;
        max-height: 40px;
    }

    QPushButton:hover {
        background-color: #e0e0e0;
        border-color: #A1A1A1;
    }

    QPushButton:pressed {
        background-color: #d0d0d0;
    }

    QPushButton:disabled {
        color: #a0a0a0;
        background-color: #f8f8f8;
    }

    #control_container {
        background-color: transparent;
    }

    QMenuBar {
        background-color: #f0f0f0;
        border-bottom: 1px solid #c0c0c0;
    }

    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }

    QScrollBar:vertical,
    QScrollBar:horizontal {
        border: 1px solid #c0c0c0;
        background: #f0f0f0;
        margin: 0;
    }

    QScrollBar:vertical {
        width: 15px;
    }

    QScrollBar:horizontal {
        height: 15px;
    }

    QScrollBar::handle:vertical,
    QScrollBar::handle:horizontal {
        background: #c0c0c0;
        border-radius: 7px;
        min-height: 20px;
        min-width: 20px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        text-align: center;
        background-color: #f0f0f0;
    }

    QProgressBar::chunk {
        background-color: #0078d4;
    }
    """)

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)