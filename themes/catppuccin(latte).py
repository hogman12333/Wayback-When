from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#eff1f5"
# window_text = "#4c4f69"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "11pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#e6e9ef"
# group_border_color = "#dce0e8"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#5c5f77"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#ffffff"
# input_text = "#4c4f69"
# input_border_color = "#9ca0b0"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#dfe1e8"
# input_selection_text = "#4c4f69"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#e6e9ef"
# button_text = "#4c4f69"
# button_border_color = "#ccd0da"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "120px"
# button_min_height = "40px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#dfe1e8"
# button_hover_border = "#1e66f5"
# button_pressed_bg = "#dce0e8"
# button_pressed_border = "#1e66f5"
# button_disabled_bg = "#eff1f5"
# button_disabled_text = "#9ca0b0"
# button_disabled_border = "#ccd0da"

# --- Menu Bar ---
# menubar_bg = "#e6e9ef"
# menubar_text = "#4c4f69"
# menubar_border = "#dce0e8"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#dfe1e8"
# menubar_item_bg_selected = "#dfe1e8"
# menubar_item_text = "#4c4f69"
# menubar_item_text_hover = "#1e1f20"
# menubar_item_text_selected = "#1e1f20"

# --- Dropdown Menus ---
# menu_bg = "#ffffff"
# menu_border = "#dce0e8"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#dfe1e8"
# menu_item_bg_selected = "#dfe1e8"
# menu_item_text = "#4c4f69"
# menu_item_text_hover = "#1e1f20"
# menu_item_text_selected = "#1e1f20"
# menu_separator_color = "#dce0e8"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "15px"
# scrollbar_bg = "#e6e9ef"
# scrollbar_border = "#dce0e8"
# scrollbar_handle_bg = "#acb0be"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "20px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#b9bcc9"
# scrollbar_handle_pressed_bg = "#c7cad4"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#e6e9ef"
# progressbar_border = "#dce0e8"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#1e66f5"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#ffffff"
# tooltip_text = "#4c4f69"
# tooltip_border = "#dce0e8"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#ffffff"
# checkbox_border = "#9ca0b0"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#1e66f5"
# checkbox_checked_border = "#1e66f5"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#e6e9ef"
# slider_groove_border = "#9ca0b0"
# slider_handle_bg = "#1e66f5"
# slider_handle_border = "#1e4ec4"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====

def apply(app, widget):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(239, 241, 245))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Base, QColor(239, 241, 245))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Text, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.Button, QColor(220, 224, 232))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(76, 79, 105))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(64, 160, 43))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(30, 102, 245))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(230, 233, 239))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(152, 157, 180))
    
    app.setPalette(palette)
    
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #4c4f69;
        background-color: #eff1f5;
    }
    
    QGroupBox {
        border: 2px solid #dce0e8;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #e6e9ef;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #5c5f77;
        font-weight: bold;
    }
    
    QListWidget, QTextEdit, QLineEdit {
        background-color: #ffffff;
        color: #4c4f69;
        border: 1px solid #9ca0b0;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #dfe1e8;
        selection-color: #4c4f69;
    }
    
    QPushButton {
        background-color: #e6e9ef;
        color: #4c4f69;
        border: 1px solid #ccd0da;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        min-width: 120px;
        max-width: 120px;
        min-height: 40px;
        max-height: 40px;
    }
    
    QPushButton:hover {
        background-color: #dfe1e8;
        border-color: #1e66f5;
    }
    
    QPushButton:pressed {
        background-color: #dce0e8;
    }
    
    QPushButton:disabled {
        color: #9ca0b0;
        background-color: #eff1f5;
    }
    
    #control_container {
        background-color: transparent;
    }
    
    QMenuBar {
        background-color: #e6e9ef;
        color: #4c4f69;
        border-bottom: 1px solid #dce0e8;
    }
    
    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }
    
    QMenuBar::item:selected {
        background-color: #dfe1e8;
    }
    
    QMenu {
        background-color: #ffffff;
        color: #4c4f69;
        border: 1px solid #dce0e8;
    }
    
    QMenu::item:selected {
        background-color: #dfe1e8;
    }
    
    QScrollBar:vertical {
        border: 1px solid #dce0e8;
        background: #e6e9ef;
        width: 15px;
        margin: 0;
    }
    
    QScrollBar:horizontal {
        border: 1px solid #dce0e8;
        background: #e6e9ef;
        height: 15px;
        margin: 0;
    }
    
    QScrollBar::handle:vertical {
        background: #acb0be;
        min-height: 20px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:horizontal {
        background: #acb0be;
        min-width: 20px;
        border-radius: 7px;
    }
    
    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }
    
    QProgressBar {
        border: 1px solid #dce0e8;
        border-radius: 4px;
        text-align: center;
        background-color: #e6e9ef;
    }
    
    QProgressBar::chunk {
        background-color: #1e66f5;
        border-radius: 0px;
    }
    """)
    
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)