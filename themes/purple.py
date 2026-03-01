from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# ===== CUSTOMISABLE VARIABLES =====
# Uncomment and modify any of these variables to customise the theme and layout

# --- Main Window ---
# window_bg = "#1f1d2e"
# window_text = "#e0def4"
# window_font_family = '"Segoe UI", Arial, sans-serif'
# window_font_size = "11pt"
# window_font_weight = "normal"

# --- Group Box ---
# group_bg = "#1f1d2e"
# group_border_color = "#26233a"
# group_border_width = "2px"
# group_border_radius = "8px"
# group_margin_top = "1em"
# group_padding_top = "15px"
# group_title_color = "#e0def4"
# group_title_bg = "transparent"
# group_title_padding = "0 8px 0 8px"
# group_title_left = "10px"
# group_title_font_weight = "bold"

# --- Input Elements ---
# input_bg = "#26233a"
# input_text = "#e0def4"
# input_border_color = "#403d52"
# input_border_width = "1px"
# input_border_radius = "4px"
# input_padding = "0px"
# input_selection_bg = "#31748f"
# input_selection_text = "#e0def4"
# input_placeholder = "#a0a0a0"

# --- Buttons ---
# button_bg = "#26233a"
# button_text = "#e0def4"
# button_border_color = "#403d52"
# button_border_width = "1px"
# button_border_radius = "4px"
# button_padding = "8px 16px"
# button_min_width = "120px"
# button_min_height = "40px"
# button_font_weight = "bold"

# Button States
# button_hover_bg = "#403d52"
# button_hover_border = "#c4a7e7"
# button_pressed_bg = "#191724"
# button_pressed_border = "#c4a7e7"
# button_disabled_bg = "#26233a"
# button_disabled_text = "#6e6a86"
# button_disabled_border = "#403d52"

# --- Menu Bar ---
# menubar_bg = "#191724"
# menubar_text = "#e0def4"
# menubar_border = "#403d52"
# menubar_border_width = "1px"
# menubar_item_padding = "4px 8px"
# menubar_item_spacing = "2px"
# menubar_corner_radius = "2px"

# Menu Bar Items
# menubar_item_bg = "transparent"
# menubar_item_bg_hover = "#44415a"
# menubar_item_bg_selected = "#44415a"
# menubar_item_text = "#e0def4"
# menubar_item_text_hover = "#ffffff"
# menubar_item_text_selected = "#ffffff"

# --- Dropdown Menus ---
# menu_bg = "#26233a"
# menu_border = "#403d52"
# menu_border_radius = "4px"
# menu_padding = "2px"
# menu_margin = "0px"

# Menu Items
# menu_item_padding = "4px 24px 4px 8px"
# menu_item_bg_hover = "#44415a"
# menu_item_bg_selected = "#44415a"
# menu_item_text = "#e0def4"
# menu_item_text_hover = "#ffffff"
# menu_item_text_selected = "#ffffff"
# menu_separator_color = "#403d52"

# --- Scroll Bars ---
# scrollbar_width = "15px"
# scrollbar_height = "15px"
# scrollbar_bg = "#26233a"
# scrollbar_border = "#403d52"
# scrollbar_handle_bg = "#44415a"
# scrollbar_handle_border_radius = "7px"
# scrollbar_handle_min_height = "20px"
# scrollbar_handle_min_width = "20px"
# scrollbar_handle_hover_bg = "#56526e"
# scrollbar_handle_pressed_bg = "#676382"
# scrollbar_add_line = "none"
# scrollbar_sub_line = "none"

# --- Progress Bar ---
# progressbar_bg = "#26233a"
# progressbar_border = "#403d52"
# progressbar_border_radius = "4px"
# progressbar_chunk_bg = "#433D68"
# progressbar_chunk_border_radius = "0px"
# progressbar_text_align = "center"

# --- Tooltips ---
# tooltip_bg = "#26233a"
# tooltip_text = "#e0def4"
# tooltip_border = "#403d52"
# tooltip_border_radius = "4px"
# tooltip_padding = "4px 8px"

# --- Special Widgets ---
# control_container_bg = "transparent"

# --- Checkboxes/Radios ---
# checkbox_bg = "#26233a"
# checkbox_border = "#403d52"
# checkbox_border_radius = "3px"
# checkbox_checked_bg = "#433D68"
# checkbox_checked_border = "#433D68"
# checkbox_size = "16px"

# --- Sliders ---
# slider_groove_bg = "#26233a"
# slider_groove_border = "#403d52"
# slider_handle_bg = "#433D68"
# slider_handle_border = "#352f4f"
# slider_handle_radius = "8px"
# slider_handle_width = "16px"
# slider_handle_height = "16px"

# ===== END OF CUSTOMISABLE VARIABLES =====

def apply(app, widget):
    # --- Palette ---
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(31, 29, 46))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 23, 36))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(38, 35, 58))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Text, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.Button, QColor(64, 61, 82))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(235, 111, 146))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(49, 116, 143))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(224, 222, 244))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(144, 140, 170))

    app.setPalette(palette)

    # --- Stylesheet ---
    widget.setStyleSheet("""
    QWidget {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        color: #e0def4;
        background-color: #1f1d2e;
    }

    QGroupBox { 
        border: 2px solid #26233a;
        border-radius: 8px;
        margin-top: 1em;
        padding-top: 15px;
        background-color: #1f1d2e;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 8px 0 8px;
        color: #e0def4;
        font-weight: bold;
    }

    QListWidget, QTextEdit, QLineEdit {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
        border-radius: 4px;
        padding: 0px;
        selection-background-color: #31748f;
        selection-color: #e0def4;
    }

    QPushButton {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        min-width: 120px;
        max-width: 120px;
        min-height: 40px;
        max-height: 40px;
    }

    QPushButton:hover {
        background-color: #403d52;
        border-color: #c4a7e7;
    }

    QPushButton:pressed {
        background-color: #191724;
    }

    QPushButton:disabled {
        color: #6e6a86;
        background-color: #26233a;
    }

    #control_container {
        background-color: transparent;
    }

    QMenuBar {
        background-color: #191724;
        color: #e0def4;
        border-bottom: 1px solid #403d52;
    }

    QMenuBar::item {
        background-color: transparent;
        padding: 4px 8px;
    }

    QMenuBar::item:selected {
        background-color: #44415a;
    }

    QMenu {
        background-color: #26233a;
        color: #e0def4;
        border: 1px solid #403d52;
    }

    QMenu::item:selected {
        background-color: #44415a;
    }

    QScrollBar:vertical {
        border: 1px solid #403d52;
        background: #26233a;
        width: 15px;
        margin: 0;
    }

    QScrollBar:horizontal {
        border: 1px solid #403d52;
        background: #26233a;
        height: 15px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #44415a;
        min-height: 20px;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background: #44415a;
        min-width: 20px;
        border-radius: 7px;
    }

    QScrollBar::add-line, QScrollBar::sub-line {
        height: 0;
        width: 0;
    }

    QProgressBar {
        border: 1px solid #403d52;
        border-radius: 4px;
        text-align: center;
        background-color: #26233a;
    }

    QProgressBar::chunk {
        border-radius: 0px;
        background-color: #433D68;
    }
    """)

    # transparency
    widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
    widget.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)