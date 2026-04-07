import sys
import os
import json
from PyQt5.QtCore import QUrl, Qt, QTimer, QEvent
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QShortcut, QCheckBox, QComboBox, QSpinBox
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView


CONFIG_FILE = "internal_web_panel_config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class SettingsDialog(QDialog):
    TRANSLATIONS = {
        "ko": {
            "window_title": "Internal Web Panel 설정",
            "language": "언어:",
            "title": "앱 제목:",
            "url": "접속 주소 (예: http://192.168.0.130:4300):",
            "width": "창 너비(px):",
            "height": "창 높이(px):",
            "pos_x": "창 위치 X(px):",
            "pos_y": "창 위치 Y(px):",
            "zoom": "줌 비율 (% / 100~200):",
            "rotation": "화면 회전:",
            "auto_reload": "자동 리로드 사용 (사이니지 안정화)",
            "auto_reload_minutes": "자동 리로드 주기:",
            "fullscreen": "앱 시작 시 전체화면으로 실행",
            "save": "저장 후 실행",
            "cancel": "취소",
            "minutes_suffix": " 분",
            "rot_0": "회전 없음 (0°)",
            "rot_90": "오른쪽으로 90° (+90°)",
            "rot_n90": "왼쪽으로 90° (-90°)",
            "msg_title": "오류",
            "msg_numbers": "창 크기와 위치는 숫자로 입력해주세요.",
            "msg_zoom_number": "줌 비율은 숫자로 입력해주세요. (예: 100, 150, 200)",
            "msg_zoom_range": "줌 비율은 100 ~ 200 사이로 입력해주세요.",
            "msg_url": "접속 주소(URL)를 입력해주세요.",
        },
        "en": {
            "window_title": "Internal Web Panel Settings",
            "language": "Language:",
            "title": "App Title:",
            "url": "URL (e.g. http://192.168.0.130:4300):",
            "width": "Window Width (px):",
            "height": "Window Height (px):",
            "pos_x": "Window Position X (px):",
            "pos_y": "Window Position Y (px):",
            "zoom": "Zoom (% / 100~200):",
            "rotation": "Rotation:",
            "auto_reload": "Enable auto reload (signage stability)",
            "auto_reload_minutes": "Auto reload interval:",
            "fullscreen": "Start in fullscreen mode",
            "save": "Save & Run",
            "cancel": "Cancel",
            "minutes_suffix": " min",
            "rot_0": "No rotation (0°)",
            "rot_90": "Rotate right 90° (+90°)",
            "rot_n90": "Rotate left 90° (-90°)",
            "msg_title": "Error",
            "msg_numbers": "Window size and position must be numbers.",
            "msg_zoom_number": "Zoom must be a number. (e.g. 100, 150, 200)",
            "msg_zoom_range": "Zoom must be between 100 and 200.",
            "msg_url": "Please enter a URL.",
        },
    }

    def __init__(self, parent=None, config=None):
        super().__init__(parent)

        if config is None:
            config = {
                "language": "ko",
                "title": "TotalScheduler Web Panel",
                "url": "http://192.168.0.134:9999",
                "width": 1280,
                "height": 720,
                "pos_x": 100,
                "pos_y": 100,
                "zoom": 100,
                "start_fullscreen": False,
                "rotation": 0,
                "auto_reload": True,
                "auto_reload_minutes": 30
            }

        self.current_language = config.get("language", "ko")
        if self.current_language not in ("ko", "en"):
            self.current_language = "ko"

        self.title_edit = QLineEdit(config.get("title", "Web Panel"))
        self.url_edit = QLineEdit(config.get("url", "http://127.0.0.1:8000"))
        self.width_edit = QLineEdit(str(config.get("width", 1280)))
        self.height_edit = QLineEdit(str(config.get("height", 720)))
        self.posx_edit = QLineEdit(str(config.get("pos_x", 100)))
        self.posy_edit = QLineEdit(str(config.get("pos_y", 100)))
        self.zoom_edit = QLineEdit(str(config.get("zoom", 100)))

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("한국어", "ko")
        self.lang_combo.addItem("English", "en")
        idx = self.lang_combo.findData(self.current_language)
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)

        self.fullscreen_check = QCheckBox()
        self.fullscreen_check.setChecked(config.get("start_fullscreen", False))

        self.auto_reload_check = QCheckBox()
        self.auto_reload_check.setChecked(bool(config.get("auto_reload", True)))

        self.auto_reload_minutes = QSpinBox()
        self.auto_reload_minutes.setRange(1, 1440)
        self.auto_reload_minutes.setValue(int(config.get("auto_reload_minutes", 30) or 30))

        self.rotation_combo = QComboBox()
        self.rotation_items = [(0, "rot_0"), (90, "rot_90"), (-90, "rot_n90")]
        self.refresh_rotation_items()
        current_rot = int(config.get("rotation", 0) or 0)
        idx = self.rotation_combo.findData(current_rot)
        if idx < 0:
            idx = 0
        self.rotation_combo.setCurrentIndex(idx)

        self.lbl_language = QLabel()
        self.lbl_title = QLabel()
        self.lbl_url = QLabel()
        self.lbl_width = QLabel()
        self.lbl_height = QLabel()
        self.lbl_pos_x = QLabel()
        self.lbl_pos_y = QLabel()
        self.lbl_zoom = QLabel()
        self.lbl_rotation = QLabel()
        self.lbl_auto_reload_minutes = QLabel()

        self.btn_save = QPushButton()
        self.btn_cancel = QPushButton()

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)

        grid = QGridLayout()
        row = 0

        grid.addWidget(self.lbl_language, row, 0)
        grid.addWidget(self.lang_combo, row, 1)
        row += 1

        grid.addWidget(self.lbl_title, row, 0)
        grid.addWidget(self.title_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_url, row, 0)
        grid.addWidget(self.url_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_width, row, 0)
        grid.addWidget(self.width_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_height, row, 0)
        grid.addWidget(self.height_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_pos_x, row, 0)
        grid.addWidget(self.posx_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_pos_y, row, 0)
        grid.addWidget(self.posy_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_zoom, row, 0)
        grid.addWidget(self.zoom_edit, row, 1)
        row += 1

        grid.addWidget(self.lbl_rotation, row, 0)
        grid.addWidget(self.rotation_combo, row, 1)
        row += 1

        grid.addWidget(self.auto_reload_check, row, 0, 1, 2)
        row += 1

        grid.addWidget(self.lbl_auto_reload_minutes, row, 0)
        grid.addWidget(self.auto_reload_minutes, row, 1)
        row += 1

        grid.addWidget(self.fullscreen_check, row, 0, 1, 2)
        row += 1

        grid.addWidget(self.btn_save, row, 0)
        grid.addWidget(self.btn_cancel, row, 1)

        self.setLayout(grid)
        self.setMinimumWidth(520)
        self.apply_language()

    def tr(self, key):
        return self.TRANSLATIONS.get(self.current_language, self.TRANSLATIONS["ko"]).get(key, key)

    def refresh_rotation_items(self):
        current_value = self.rotation_combo.currentData()
        self.rotation_combo.blockSignals(True)
        self.rotation_combo.clear()
        for value, key in self.rotation_items:
            self.rotation_combo.addItem(self.tr(key), value)
        idx = self.rotation_combo.findData(current_value)
        if idx < 0:
            idx = 0
        self.rotation_combo.setCurrentIndex(idx)
        self.rotation_combo.blockSignals(False)

    def apply_language(self):
        self.setWindowTitle(self.tr("window_title"))
        self.lbl_language.setText(self.tr("language"))
        self.lbl_title.setText(self.tr("title"))
        self.lbl_url.setText(self.tr("url"))
        self.lbl_width.setText(self.tr("width"))
        self.lbl_height.setText(self.tr("height"))
        self.lbl_pos_x.setText(self.tr("pos_x"))
        self.lbl_pos_y.setText(self.tr("pos_y"))
        self.lbl_zoom.setText(self.tr("zoom"))
        self.lbl_rotation.setText(self.tr("rotation"))
        self.lbl_auto_reload_minutes.setText(self.tr("auto_reload_minutes"))

        self.auto_reload_check.setText(self.tr("auto_reload"))
        self.fullscreen_check.setText(self.tr("fullscreen"))
        self.btn_save.setText(self.tr("save"))
        self.btn_cancel.setText(self.tr("cancel"))
        self.auto_reload_minutes.setSuffix(self.tr("minutes_suffix"))
        self.refresh_rotation_items()

    def on_language_changed(self):
        self.current_language = self.lang_combo.currentData() or "ko"
        self.apply_language()

    def get_config(self):
        try:
            width = int(self.width_edit.text().strip())
            height = int(self.height_edit.text().strip())
            pos_x = int(self.posx_edit.text().strip())
            pos_y = int(self.posy_edit.text().strip())
        except ValueError:
            QMessageBox.warning(self, self.tr("msg_title"), self.tr("msg_numbers"))
            return None

        try:
            zoom = int(self.zoom_edit.text().strip())
        except ValueError:
            QMessageBox.warning(self, self.tr("msg_title"), self.tr("msg_zoom_number"))
            return None

        if zoom < 100 or zoom > 200:
            QMessageBox.warning(self, self.tr("msg_title"), self.tr("msg_zoom_range"))
            return None

        title = self.title_edit.text().strip() or "Web Panel"
        url = self.url_edit.text().strip()

        if not url:
            QMessageBox.warning(self, self.tr("msg_title"), self.tr("msg_url"))
            return None

        return {
            "language": self.current_language,
            "title": title,
            "url": url,
            "width": width,
            "height": height,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "zoom": zoom,
            "start_fullscreen": self.fullscreen_check.isChecked(),
            "rotation": int(self.rotation_combo.currentData() or 0),
            "auto_reload": self.auto_reload_check.isChecked(),
            "auto_reload_minutes": int(self.auto_reload_minutes.value()),
        }


class WebWindow(QMainWindow):
    def _exit_by_long_press(self):
        QApplication.quit()

    def eventFilter(self, obj, event):
        try:
            et = event.type()

            if et == QEvent.MouseButtonPress and getattr(event, "button", None) and event.button() == Qt.LeftButton:
                gp = event.globalPos()
                lp = self.mapFromGlobal(gp)
                if 0 <= lp.x() <= self._exit_hotspot and 0 <= lp.y() <= self._exit_hotspot:
                    self._exit_pressed = True
                    self._exit_press_timer.start(self._exit_hold_ms)
                    return False

            if et == QEvent.MouseButtonRelease:
                if self._exit_pressed:
                    self._exit_press_timer.stop()
                    self._exit_pressed = False
                return False

            if et == QEvent.TouchBegin:
                pts = event.touchPoints()
                if pts:
                    gp = pts[0].screenPos().toPoint()
                    lp = self.mapFromGlobal(gp)
                    if 0 <= lp.x() <= self._exit_hotspot and 0 <= lp.y() <= self._exit_hotspot:
                        self._exit_pressed = True
                        self._exit_press_timer.start(self._exit_hold_ms)
                return False

            if et in (QEvent.TouchEnd, QEvent.TouchCancel):
                if self._exit_pressed:
                    self._exit_press_timer.stop()
                    self._exit_pressed = False
                return False

        except Exception:
            pass

        return super().eventFilter(obj, event)

    def apply_frameless(self):
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.Window, True)

    def apply_fullscreen_now(self):
        want_fs = bool(self.config.get("start_fullscreen", False))
        self.apply_frameless()

        if want_fs:
            self.showFullScreen()
        else:
            self.showNormal()
            self.apply_config_to_window()

        self.raise_()
        self.activateWindow()

    def __init__(self, config):
        super().__init__()
        self.config = config

        self._exit_hotspot = 80
        self._exit_hold_ms = 4000
        self._exit_pressed = False

        self._exit_press_timer = QTimer(self)
        self._exit_press_timer.setSingleShot(True)
        self._exit_press_timer.timeout.connect(self._exit_by_long_press)

        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        self.apply_config_to_window()
        self.set_zoom_from_config()

        self.view.loadFinished.connect(self.apply_rotation_from_config)
        self.view.setUrl(QUrl(self.config["url"]))

        self.setup_shortcuts()

        self.reload_timer = QTimer(self)
        self.reload_timer.timeout.connect(self.reload_page)
        self.apply_auto_reload_from_config()

        self.apply_frameless()

    def apply_config_to_window(self):
        self.setWindowTitle(self.config.get("title", "Web Panel"))

        width = self.config.get("width", 1280)
        height = self.config.get("height", 720)
        pos_x = self.config.get("pos_x", 100)
        pos_y = self.config.get("pos_y", 100)

        if self.isFullScreen() or bool(self.config.get("start_fullscreen", False)):
            return

        self.resize(width, height)
        self.move(pos_x, pos_y)

    def set_zoom_from_config(self):
        zoom_percent = self.config.get("zoom", 100)
        try:
            zoom_percent = int(zoom_percent)
        except Exception:
            zoom_percent = 100

        if zoom_percent < 10:
            zoom_percent = 10

        factor = zoom_percent / 100.0
        self.view.setZoomFactor(factor)

    def setup_shortcuts(self):
        f11_shortcut = QShortcut(QKeySequence("F11"), self)
        f11_shortcut.activated.connect(self.toggle_fullscreen)

        f5_shortcut = QShortcut(QKeySequence("F5"), self)
        f5_shortcut.activated.connect(self.reload_page)

        f2_shortcut = QShortcut(QKeySequence("F2"), self)
        f2_shortcut.activated.connect(self.open_settings)

    def toggle_fullscreen(self):
        self.apply_frameless()
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        self.raise_()
        self.activateWindow()

    def reload_page(self):
        self.view.reload()

    def apply_auto_reload_from_config(self):
        enabled = bool(self.config.get("auto_reload", True))
        minutes = int(self.config.get("auto_reload_minutes", 30) or 30)

        if minutes < 1:
            minutes = 1

        if enabled:
            self.reload_timer.setInterval(minutes * 60 * 1000)
            if not self.reload_timer.isActive():
                self.reload_timer.start()
        else:
            if self.reload_timer.isActive():
                self.reload_timer.stop()

    def apply_rotation_from_config(self):
        rot = int(self.config.get("rotation", 0) or 0)
        if rot not in (0, 90, -90):
            rot = 0

        js = f"""
        (function(){{
          try{{
            var oldStyle = document.getElementById('ts-rotate-style');
            if(oldStyle) oldStyle.remove();

            var style = document.createElement('style');
            style.id = 'ts-rotate-style';
            style.innerHTML = `
              html, body {{
                margin: 0 !important;
                padding: 0 !important;
                width: 100% !important;
                height: 100% !important;
                overflow: auto !important;
                background: #000;
              }}
              * {{
                scrollbar-width: none !important;
                -ms-overflow-style: none !important;
              }}
              *::-webkit-scrollbar {{
                display: none !important;
                width: 0 !important;
                height: 0 !important;
              }}
              #ts-rotate-wrap {{
                transform-origin: top left;
              }}
            `;
            document.head.appendChild(style);

            var wrap = document.getElementById('ts-rotate-wrap');
            if(!wrap){{
              wrap = document.createElement('div');
              wrap.id = 'ts-rotate-wrap';
              while(document.body.firstChild){{
                wrap.appendChild(document.body.firstChild);
              }}
              document.body.appendChild(wrap);
            }}

            wrap.style.position = '';
            wrap.style.top = '';
            wrap.style.left = '';
            wrap.style.width = '';
            wrap.style.height = '';
            wrap.style.transform = '';

            if({rot} === 90){{
              wrap.style.position = 'fixed';
              wrap.style.top = '0';
              wrap.style.left = '0';
              wrap.style.width = '100vh';
              wrap.style.height = '100vw';
              wrap.style.transform = 'rotate(90deg) translateY(-100%)';
            }} else if({rot} === -90){{
              wrap.style.position = 'fixed';
              wrap.style.top = '0';
              wrap.style.left = '0';
              wrap.style.width = '100vh';
              wrap.style.height = '100vw';
              wrap.style.transform = 'rotate(-90deg) translateX(-100%)';
            }}
          }} catch(e) {{
            console.error(e);
          }}
        }})();
        """
        self.view.page().runJavaScript(js)
        self.view.page().runJavaScript("window.dispatchEvent(new Event('resize'));")

    def open_settings(self):
        dlg = SettingsDialog(self, config=self.config)
        if dlg.exec_() == QDialog.Accepted:
            new_cfg = dlg.get_config()
            if new_cfg:
                old_url = self.view.url().toString()
                self.config = new_cfg
                save_config(self.config)

                self.apply_config_to_window()
                self.set_zoom_from_config()
                self.apply_auto_reload_from_config()

                new_url = self.config.get("url", "")
                if new_url and new_url != old_url:
                    self.view.setUrl(QUrl(new_url))

                QTimer.singleShot(0, self.apply_fullscreen_now)
                QTimer.singleShot(120, self.apply_fullscreen_now)
                QTimer.singleShot(150, self.apply_rotation_from_config)
                QTimer.singleShot(300, self.apply_rotation_from_config)


def main():
    app = QApplication(sys.argv)

    config = load_config()
    if config is None:
        dlg = SettingsDialog()
        if dlg.exec_() != QDialog.Accepted:
            sys.exit(0)
        config = dlg.get_config()
        if config is None:
            sys.exit(0)
        save_config(config)

    defaults = {
        "language": "ko",
        "rotation": 0,
        "auto_reload": True,
        "auto_reload_minutes": 30,
    }
    changed = False
    for k, v in defaults.items():
        if k not in config:
            config[k] = v
            changed = True
    if changed:
        save_config(config)

    window = WebWindow(config)
    window.show()

    if config.get("start_fullscreen", False):
        window.showFullScreen()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
