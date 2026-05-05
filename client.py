import socket
import threading
import json
import os
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox
import subprocess
import sys
from PIL import Image, ImageTk
import io

from utils.protocol import encode_message, decode_message
from utils.crypto import (
    generate_rsa_keys,
    decrypt_aes_key,
    encrypt_message,
    decrypt_message,
    generate_hash,
    sign_message
)
from utils.database import init_db, save_message, load_messages
from utils.blockchain import calculate_hash

HOST = '127.0.0.1'
PORT = 5051

SAVE_DIR = os.path.join(os.path.expanduser("~"), "ChainSecureX_Downloads")
os.makedirs(SAVE_DIR, exist_ok=True)

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.flac'}

# ── Palette ──────────────────────────────────────────────
BG_DARK    = "#0d1117"
BG_PANEL   = "#161b22"
BG_SIDEBAR = "#0d1117"
BG_INPUT   = "#21262d"
BG_BUBBLE_ME    = "#238636"
BG_BUBBLE_OTHER = "#1c2128"
ACCENT     = "#58a6ff"
ACCENT2    = "#3fb950"
TEXT_PRI   = "#e6edf3"
TEXT_SEC   = "#8b949e"
BORDER     = "#30363d"
DANGER     = "#f85149"

def recv_fixed(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

def open_file(path):
    """Open file with the system default application."""
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file:\n{e}")

# ─────────────────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────────────────
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("ChainSecureX")
        # Compact login — doesn't hog the screen alongside VS Code
        self.root.geometry("400x480+880+180")
        self.root.resizable(True, True)
        self.root.minsize(340, 400)
        self.root.configure(fg_color=BG_DARK)

        # Header glow canvas
        canvas = ctk.CTkCanvas(root, width=480, height=180,
                                bg=BG_DARK, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(-60, -60, 540, 200, fill="#0e2a1a", outline="")
        canvas.create_text(240, 90, text="⬡", font=("Courier", 48), fill=ACCENT2)

        frame = ctk.CTkFrame(root, fg_color=BG_PANEL,
                              corner_radius=16,
                              border_width=1, border_color=BORDER)
        frame.pack(padx=40, pady=10, fill="x")

        ctk.CTkLabel(frame, text="ChainSecureX",
                     font=("Courier New", 26, "bold"),
                     text_color=TEXT_PRI).pack(pady=(28, 4))

        ctk.CTkLabel(frame, text="End-to-end encrypted · Blockchain verified",
                     font=("Courier New", 11),
                     text_color=TEXT_SEC).pack(pady=(0, 20))

        self.entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter username",
            width=300, height=42,
            font=("Courier New", 14),
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRI,
            placeholder_text_color=TEXT_SEC,
            corner_radius=10
        )
        self.entry.pack(pady=8)
        self.entry.bind("<Return>", lambda e: self.start_chat())

        self.host_entry = ctk.CTkEntry(
            frame,
            placeholder_text=f"Server host (default: {HOST})",
            width=300, height=38,
            font=("Courier New", 12),
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRI,
            placeholder_text_color=TEXT_SEC,
            corner_radius=10
        )
        self.host_entry.pack(pady=4)

        self.status = ctk.CTkLabel(frame, text="", font=("Courier New", 11),
                                   text_color=DANGER)
        self.status.pack(pady=4)

        ctk.CTkButton(
            frame, text="Connect  →", width=300, height=44,
            font=("Courier New", 14, "bold"),
            fg_color=ACCENT2, hover_color="#2ea043",
            text_color="#000000",
            corner_radius=10,
            command=self.start_chat
        ).pack(pady=(4, 28))

    def start_chat(self):
        username = self.entry.get().strip()
        host = self.host_entry.get().strip() or HOST
        if not username:
            self.status.configure(text="⚠  Username required")
            return
        self.status.configure(text="Connecting…", text_color=ACCENT)
        self.root.update()
        for w in self.root.winfo_children():
            w.destroy()
        try:
            ChatApp(self.root, username, host)
        except Exception as e:
            # Re-show login on connection failure
            LoginScreen(self.root)

# ─────────────────────────────────────────────────────────
#  CHAT APP
# ─────────────────────────────────────────────────────────
class ChatApp:
    def __init__(self, root, username, host=HOST):
        self.root = root
        self.root.title(f"ChainSecureX  ·  {username}")
        self.root.configure(fg_color=BG_DARK)

        # ── Smart window sizing ───────────────────────────
        # Detect screen size and snap to right ~40% so VS Code can sit left
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        win_w = max(420, sw // 3)       # ~1/3 screen width, min 420px
        win_h = max(500, int(sh * 0.85)) # tall but not full height
        win_x = sw - win_w - 8          # flush to right edge with 8px gap
        win_y = 40                       # below taskbar
        self.root.geometry(f"{win_w}x{win_h}+{win_x}+{win_y}")
        self.root.minsize(380, 400)      # can shrink down to a narrow panel
        self.root.resizable(True, True)

        self.username = username
        self.last_seen_label = None
        self.seen_ids = set()
        self._file_cache = {}   # msg_id → (filename, bytes) for preview

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, PORT))

        self.private_key, self.public_key = generate_rsa_keys()

        u = self.username.encode()
        self.client.send(len(u).to_bytes(4, 'big'))
        self.client.send(u)

        key = self.public_key.export_key()
        self.client.send(len(key).to_bytes(4, 'big'))
        self.client.send(key)

        l = int.from_bytes(self.client.recv(4), 'big')
        enc = recv_fixed(self.client, l)
        self.aes_key = decrypt_aes_key(enc, self.private_key)

        init_db()
        self._build_ui()
        self._load_history()
        threading.Thread(target=self._recv_loop, daemon=True).start()

    # ── UI BUILD ─────────────────────────────────────────
    def _build_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self._sidebar_expanded = True

        # ── Sidebar ──────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self.root, width=170,
                                    fg_color=BG_SIDEBAR,
                                    corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo + toggle button
        logo = ctk.CTkFrame(self.sidebar, fg_color=BG_PANEL,
                             corner_radius=0, height=52)
        logo.pack(fill="x")
        logo.pack_propagate(False)
        self._logo_label = ctk.CTkLabel(logo, text="⬡ CSX",
                     font=("Courier New", 13, "bold"),
                     text_color=ACCENT2)
        self._logo_label.pack(side="left", padx=10, pady=14)
        ctk.CTkButton(
            logo, text="◀", width=26, height=26,
            font=("Courier New", 10),
            fg_color="transparent", hover_color=BORDER,
            text_color=TEXT_SEC, corner_radius=6,
            command=self._toggle_sidebar
        ).pack(side="right", padx=6)

        # Me badge
        me_frame = ctk.CTkFrame(self.sidebar, fg_color=BG_INPUT, corner_radius=10)
        me_frame.pack(fill="x", padx=6, pady=(8, 4))
        self._avatar = ctk.CTkLabel(me_frame,
                     text=self.username[0].upper(),
                     width=28, height=28, corner_radius=14,
                     fg_color=ACCENT2, text_color="#000",
                     font=("Courier New", 12, "bold"))
        self._avatar.pack(side="left", padx=6, pady=6)
        self._me_info = ctk.CTkFrame(me_frame, fg_color="transparent")
        self._me_info.pack(side="left")
        ctk.CTkLabel(self._me_info, text=self.username[:12],
                     font=("Courier New", 10, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w")
        ctk.CTkLabel(self._me_info, text="● Online",
                     font=("Courier New", 9),
                     text_color=ACCENT2).pack(anchor="w")

        self._users_header = ctk.CTkLabel(self.sidebar, text="USERS",
                     font=("Courier New", 9, "bold"), text_color=TEXT_SEC)
        self._users_header.pack(anchor="w", padx=10, pady=(8, 2))

        self.users_frame = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent", corner_radius=0)
        self.users_frame.pack(fill="both", expand=True, padx=4)

        self._dl_btn = ctk.CTkButton(
            self.sidebar, text="📁 Downloads",
            font=("Courier New", 10),
            fg_color=BG_INPUT, hover_color=BORDER,
            text_color=TEXT_SEC, corner_radius=8, height=28,
            command=lambda: open_file(SAVE_DIR)
        )
        self._dl_btn.pack(fill="x", padx=6, pady=(0, 8))

        # Auto-collapse sidebar when window gets narrow
        self.root.bind("<Configure>", self._on_resize)

        # ── Main Chat Area ────────────────────────────────
        main = ctk.CTkFrame(self.root, fg_color=BG_DARK, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(main, fg_color=BG_PANEL,
                               corner_radius=0, height=64,
                               border_width=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(header, text="🔒  Secure Chat",
                     font=("Courier New", 15, "bold"),
                     text_color=TEXT_PRI).pack(side="left", padx=20, pady=18)

        self.conn_dot = ctk.CTkLabel(header, text="● Connected",
                                      font=("Courier New", 11),
                                      text_color=ACCENT2)
        self.conn_dot.pack(side="right", padx=20)

        # Messages area
        self.chat_frame = ctk.CTkScrollableFrame(
            main, fg_color=BG_DARK, corner_radius=0)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Input bar
        input_bar = ctk.CTkFrame(main, fg_color=BG_PANEL,
                                  corner_radius=0, height=72)
        input_bar.grid(row=2, column=0, sticky="ew")
        input_bar.grid_propagate(False)
        input_bar.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            input_bar,
            placeholder_text="Type a message…",
            font=("Courier New", 13),
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRI,
            placeholder_text_color=TEXT_SEC,
            corner_radius=10,
            height=42
        )
        self.entry.grid(row=0, column=0, padx=(16, 8), pady=15, sticky="ew")
        self.entry.bind("<Return>", lambda e: self._send_message())

        ctk.CTkButton(
            input_bar, text="📎", width=42, height=42,
            font=("Courier New", 16),
            fg_color=BG_INPUT, hover_color=BORDER,
            text_color=TEXT_PRI, corner_radius=10,
            command=self._send_file
        ).grid(row=0, column=1, padx=4, pady=15)

        ctk.CTkButton(
            input_bar, text="➤", width=52, height=42,
            font=("Courier New", 15, "bold"),
            fg_color=ACCENT, hover_color="#1f6feb",
            text_color="#ffffff", corner_radius=10,
            command=self._send_message
        ).grid(row=0, column=2, padx=(4, 16), pady=15)

    # ── SIDEBAR TOGGLE & RESPONSIVE RESIZE ──────────────
    def _toggle_sidebar(self):
        if self._sidebar_expanded:
            self.sidebar.configure(width=46)
            self._logo_label.configure(text="⬡")
            self._me_info.pack_forget()
            self._users_header.pack_forget()
            self._dl_btn.pack_forget()
            self._sidebar_expanded = False
        else:
            self.sidebar.configure(width=170)
            self._logo_label.configure(text="⬡ CSX")
            self._me_info.pack(side="left")
            self._users_header.pack(anchor="w", padx=10, pady=(8, 2))
            self._dl_btn.pack(fill="x", padx=6, pady=(0, 8))
            self._sidebar_expanded = True

    def _on_resize(self, event):
        """Auto-collapse sidebar when window width < 520px."""
        if event.widget != self.root:
            return
        w = event.width
        if w < 520 and self._sidebar_expanded:
            self._toggle_sidebar()
        elif w >= 520 and not self._sidebar_expanded:
            self._toggle_sidebar()

    # ── USER LIST ─────────────────────────────────────────
    def _update_users(self, users):
        for w in self.users_frame.winfo_children():
            w.destroy()
        for user in users:
            row = ctk.CTkFrame(self.users_frame, fg_color="transparent",
                                cursor="hand2")
            row.pack(fill="x", pady=2)

            color = ACCENT2 if user == self.username else "#444c56"
            ctk.CTkLabel(row,
                         text=user[0].upper(),
                         width=30, height=30, corner_radius=15,
                         fg_color=color,
                         text_color="#000" if user == self.username else TEXT_PRI,
                         font=("Courier New", 13, "bold")).pack(side="left", padx=6, pady=4)

            name = user + ("  (you)" if user == self.username else "")
            ctk.CTkLabel(row, text=name,
                         font=("Courier New", 12),
                         text_color=TEXT_PRI if user == self.username else TEXT_SEC
                         ).pack(side="left")

    # ── ADD MESSAGE BUBBLE ────────────────────────────────
    def _add_message(self, message, sender="other", timestamp=None, file_info=None):
        """
        file_info = {"name": str, "path": str, "ext": str, "data": bytes | None}
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M")

        is_me = (sender == "me")

        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.pack(fill="x", pady=3, padx=10)

        bubble_color = BG_BUBBLE_ME if is_me else BG_BUBBLE_OTHER
        anchor = "e" if is_me else "w"

        bubble = ctk.CTkFrame(outer, fg_color=bubble_color,
                               corner_radius=14,
                               border_width=1,
                               border_color="#238636" if is_me else BORDER)
        bubble.pack(anchor=anchor, padx=6)

        if file_info:
            self._render_file_bubble(bubble, file_info, is_me)
        else:
            ctk.CTkLabel(bubble, text=message,
                         font=("Courier New", 13),
                         text_color=TEXT_PRI,
                         wraplength=420,
                         justify="left").pack(padx=14, pady=(10, 4), anchor="w")

        # Timestamp + status row
        ts_row = ctk.CTkFrame(bubble, fg_color="transparent")
        ts_row.pack(anchor="e", padx=10, pady=(0, 6))

        ctk.CTkLabel(ts_row, text=timestamp,
                     font=("Courier New", 9),
                     text_color=TEXT_SEC).pack(side="left")

        if is_me:
            self.last_seen_label = ctk.CTkLabel(
                ts_row, text=" ✓",
                font=("Courier New", 9),
                text_color=TEXT_SEC)
            self.last_seen_label.pack(side="left")

        # Auto-scroll
        self.root.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _render_file_bubble(self, parent, file_info, is_me):
        """Render image preview or file card with Open & Save buttons."""
        name = file_info["name"]
        path = file_info.get("path")
        ext  = file_info.get("ext", "").lower()
        data = file_info.get("data")

        # ── Image preview ──────────────────────────────────
        if ext in IMAGE_EXTS and data:
            try:
                img = Image.open(io.BytesIO(data))
                img.thumbnail((280, 200))
                photo = ImageTk.PhotoImage(img)

                img_label = ctk.CTkLabel(parent, image=photo, text="")
                img_label.image = photo  # keep reference
                img_label.pack(padx=10, pady=(10, 4))
            except Exception:
                pass  # fall through to file card if image fails

        # ── File card ──────────────────────────────────────
        icon = _file_icon(ext)
        card = ctk.CTkFrame(parent, fg_color=BG_INPUT, corner_radius=10)
        card.pack(padx=10, pady=(4, 6), fill="x")

        ctk.CTkLabel(card, text=icon,
                     font=("Courier New", 22)).pack(side="left", padx=10, pady=8)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(info, text=name,
                     font=("Courier New", 11, "bold"),
                     text_color=TEXT_PRI,
                     wraplength=180).pack(anchor="w")

        size_text = f"{len(data) // 1024} KB" if data else "?"
        ctk.CTkLabel(info, text=size_text,
                     font=("Courier New", 9),
                     text_color=TEXT_SEC).pack(anchor="w")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(side="right", padx=8)

        if path and os.path.exists(path):
            ctk.CTkButton(
                btn_row, text="Open",
                width=58, height=28,
                font=("Courier New", 11),
                fg_color=ACCENT, hover_color="#1f6feb",
                text_color="#fff", corner_radius=8,
                command=lambda p=path: open_file(p)
            ).pack(pady=2)

            ctk.CTkButton(
                btn_row, text="Save As",
                width=58, height=28,
                font=("Courier New", 11),
                fg_color=BG_PANEL, hover_color=BORDER,
                text_color=TEXT_PRI, corner_radius=8,
                command=lambda p=path, n=name: self._save_as(p, n)
            ).pack(pady=2)
        else:
            ctk.CTkLabel(btn_row, text="Saved ✓",
                         font=("Courier New", 10),
                         text_color=ACCENT2).pack(padx=8)

    # ── HISTORY ───────────────────────────────────────────
    def _load_history(self):
        seen = set()
        for user, msg, time in load_messages():
            key = f"{user}:{msg}:{time}"
            if key in seen:
                continue
            seen.add(key)
            sender = "me" if user == self.username else "other"
            display = msg if sender == "me" else f"{user}: {msg}"
            self._add_message(display, sender, time)

    # ── SEND MESSAGE ──────────────────────────────────────
    def _send_message(self):
        msg = self.entry.get().strip()
        if not msg:
            return

        timestamp = datetime.now().strftime("%H:%M")
        msg_bytes = msg.encode()
        msg_hash = generate_hash(msg_bytes)
        signature = sign_message(msg_bytes, self.private_key)
        data = encode_message(self.username, msg, msg_hash, signature)

        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            enc = encrypt_message(data, self.aes_key)
            enc_bytes = enc if isinstance(enc, bytes) else enc.encode('utf-8')
            self.client.send(len(enc_bytes).to_bytes(4, 'big'))
            self.client.send(enc_bytes)
        except Exception as e:
            self._add_message(f"⚠ Failed to send: {e}", "other")
            return

        save_message(self.username, msg, timestamp, "", "")
        self._add_message(msg, "me", timestamp)
        self.entry.delete(0, "end")

    # ── SEND FILE ─────────────────────────────────────────
    def _send_file(self):
        path = filedialog.askopenfilename(title="Send File")
        if not path:
            return

        with open(path, "rb") as f:
            data = f.read()

        name = os.path.basename(path)
        payload = {"type": "file", "name": name, "data": data.hex()}

        try:
            enc = encrypt_message(json.dumps(payload).encode('utf-8'), self.aes_key)
            enc_bytes = enc if isinstance(enc, bytes) else enc.encode('utf-8')
            self.client.send(len(enc_bytes).to_bytes(4, 'big'))
            self.client.send(enc_bytes)
        except Exception as e:
            self._add_message(f"⚠ File send failed: {e}", "other")
            return

        ext = os.path.splitext(name)[1].lower()
        self._add_message("", "me", file_info={
            "name": name, "path": path, "ext": ext, "data": data
        })

    # ── RECEIVE LOOP ──────────────────────────────────────
    def _recv_loop(self):
        while True:
            try:
                header = recv_fixed(self.client, 4)
                if not header:
                    break

                l = int.from_bytes(header, 'big')
                packet = recv_fixed(self.client, l)
                if not packet:
                    continue

                # Try plain JSON first (server control messages)
                try:
                    data = json.loads(packet.decode())
                except Exception:
                    # Try decrypt then JSON
                    try:
                        dec = decrypt_message(packet, self.aes_key)
                        data = json.loads(dec.decode('utf-8'))
                    except Exception as e:
                        print(f"[Parse Error] {e}")
                        continue

                if data.get("type") == "users":
                    self.root.after(0, lambda u=data["users"]: self._update_users(u))
                    continue

                if data.get("type") == "seen":
                    if self.last_seen_label:
                        self.root.after(0, lambda: self.last_seen_label.configure(
                            text=" ✓✓ Seen", text_color=ACCENT))
                    continue

                if data.get("type") == "chat":
                    msg_id = data["id"]
                    if msg_id in self.seen_ids:
                        continue
                    self.seen_ids.add(msg_id)

                    raw = bytes.fromhex(data["data"])

                    # Decrypt
                    try:
                        dec = decrypt_message(raw, self.aes_key)
                    except Exception as e:
                        print(f"[Decrypt Error] {e}")
                        continue

                    # Parse payload
                    decoded = None
                    try:
                        decoded = json.loads(dec.decode('utf-8'))
                    except Exception:
                        pass

                    if decoded is None:
                        try:
                            decoded = decode_message(dec)
                        except Exception as e:
                            print(f"[Decode Error] {e}")
                            continue

                    # ── File payload ──────────────────────
                    if isinstance(decoded, dict) and decoded.get("type") == "file":
                        fname = decoded["name"]
                        fdata = bytes.fromhex(decoded["data"])
                        fpath = os.path.join(SAVE_DIR, fname)

                        # Auto-save to downloads folder
                        try:
                            with open(fpath, "wb") as f:
                                f.write(fdata)
                            print(f"[File Saved] {fpath}")
                        except Exception as e:
                            print(f"[File Save Error] {e}")
                            fpath = None

                        ext = os.path.splitext(fname)[1].lower()
                        self.root.after(0, lambda fn=fname, fp=fpath,
                                        ex=ext, fd=fdata:
                                        self._add_message("", "other", file_info={
                                            "name": fn, "path": fp,
                                            "ext": ex, "data": fd
                                        }))
                        continue

                    # ── Text message ──────────────────────
                    try:
                        msg    = decoded["msg"]
                        sender = decoded["user"]
                    except (KeyError, TypeError) as e:
                        print(f"[Message Error] {e}")
                        continue

                    if sender == self.username:
                        continue

                    ts = datetime.now().strftime("%H:%M")
                    display = f"{sender}: {msg}"
                    save_message(sender, msg, ts, "", "")
                    self.root.after(0, lambda d=display, t=ts:
                                    self._add_message(d, "other", t))

            except Exception as e:
                print(f"[Receive Loop Error] {e}")
                break

        self.root.after(0, lambda: self.conn_dot.configure(
            text="● Disconnected", text_color=DANGER))

    # ── SAVE AS ───────────────────────────────────────────
    def _save_as(self, src_path, name):
        dest = filedialog.asksaveasfilename(initialfile=name)
        if dest:
            import shutil
            shutil.copy2(src_path, dest)
            messagebox.showinfo("Saved", f"File saved to:\n{dest}")

# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────
def _file_icon(ext):
    if ext in IMAGE_EXTS:  return "🖼"
    if ext in VIDEO_EXTS:  return "🎬"
    if ext in AUDIO_EXTS:  return "🎵"
    if ext == ".pdf":      return "📄"
    if ext in {".zip", ".rar", ".7z", ".tar", ".gz"}: return "🗜"
    if ext in {".py", ".js", ".ts", ".html", ".css", ".json"}: return "💻"
    if ext in {".doc", ".docx", ".txt", ".md"}: return "📝"
    return "📁"

# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.iconbitmap(default="") if sys.platform == "win32" else None
    LoginScreen(root)
    root.mainloop()
