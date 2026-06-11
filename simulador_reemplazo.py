import tkinter as tk
from tkinter import ttk, messagebox
import random

# ─────────────────────────────────────────────
# ALGORITMOS DE REEMPLAZO DE PÁGINAS
# ─────────────────────────────────────────────

def fifo(pages, frames):
    """First In, First Out"""
    memory = []
    order = []
    history = []
    faults = 0

    for page in pages:
        hit = page in memory
        if not hit:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
                order.append(page)
            else:
                evicted = order.pop(0)
                idx = memory.index(evicted)
                memory[idx] = page
                order.append(page)
        history.append((page, list(memory), hit))

    return history, faults


def lru(pages, frames):
    """Least Recently Used"""
    memory = []
    usage = []
    history = []
    faults = 0

    for page in pages:
        hit = page in memory
        if not hit:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
                usage.append(page)
            else:
                lru_page = usage[0]
                idx = memory.index(lru_page)
                memory[idx] = page
                usage.pop(0)
                usage.append(page)
        else:
            usage.remove(page)
            usage.append(page)
        history.append((page, list(memory), hit))

    return history, faults


def optimal(pages, frames):
    """Optimal (OPT) — reemplaza la página que se usará más lejos en el futuro"""
    memory = []
    history = []
    faults = 0

    for i, page in enumerate(pages):
        hit = page in memory
        if not hit:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                future_use = {}
                for p in memory:
                    try:
                        future_use[p] = pages[i+1:].index(p)
                    except ValueError:
                        future_use[p] = float('inf')
                evicted = max(future_use, key=future_use.get)
                memory[memory.index(evicted)] = page
        history.append((page, list(memory), hit))

    return history, faults


def clock(pages, frames):
    """Clock (Segunda Oportunidad)"""
    memory = [None] * frames
    ref_bits = [0] * frames
    pointer = 0
    history = []
    faults = 0

    for page in pages:
        hit = page in memory
        if not hit:
            faults += 1
            while True:
                if memory[pointer] is None:
                    memory[pointer] = page
                    ref_bits[pointer] = 1
                    pointer = (pointer + 1) % frames
                    break
                elif ref_bits[pointer] == 0:
                    memory[pointer] = page
                    ref_bits[pointer] = 1
                    pointer = (pointer + 1) % frames
                    break
                else:
                    ref_bits[pointer] = 0
                    pointer = (pointer + 1) % frames
        else:
            idx = memory.index(page)
            ref_bits[idx] = 1
        history.append((page, [p if p is not None else '-' for p in memory], hit))

    return history, faults


# ─────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Algoritmos de Reemplazo de Páginas")
        self.root.geometry("1050x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        # Colores
        self.BG = "#1a1a2e"
        self.PANEL = "#16213e"
        self.ACCENT = "#0f3460"
        self.BLUE = "#4cc9f0"
        self.GREEN = "#06d6a0"
        self.RED = "#ef233c"
        self.TEXT = "#e0e0e0"
        self.MUTED = "#8d99ae"
        self.GOLD = "#f8961e"

        self._build_ui()

    def _build_ui(self):
        # ── TÍTULO ──
        title_frame = tk.Frame(self.root, bg=self.BG)
        title_frame.pack(fill="x", padx=20, pady=(16, 4))

        tk.Label(title_frame, text="🖥  Simulador de Reemplazo de Páginas",
                 font=("Segoe UI", 17, "bold"), bg=self.BG, fg=self.BLUE).pack(side="left")

        # ── PANEL DE CONFIGURACIÓN ──
        cfg = tk.Frame(self.root, bg=self.PANEL, bd=0, relief="flat")
        cfg.pack(fill="x", padx=20, pady=8)

        inner = tk.Frame(cfg, bg=self.PANEL)
        inner.pack(padx=16, pady=12)

        # Cadena de páginas
        tk.Label(inner, text="Cadena de páginas:", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=(0,8))
        self.pages_var = tk.StringVar(value="7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")
        self.pages_entry = tk.Entry(inner, textvariable=self.pages_var, width=46,
                                    bg="#0d1b2a", fg=self.TEXT, insertbackground=self.BLUE,
                                    font=("Consolas", 10), relief="flat", bd=4)
        self.pages_entry.grid(row=0, column=1, padx=(0,16))

        tk.Button(inner, text="⟳ Aleatorio", command=self._gen_random,
                  bg=self.ACCENT, fg=self.BLUE, font=("Segoe UI", 9), relief="flat",
                  cursor="hand2", padx=8).grid(row=0, column=2, padx=(0,16))

        # Marcos
        tk.Label(inner, text="Marcos de página:", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 10)).grid(row=0, column=3, sticky="w", padx=(0,8))
        self.frames_var = tk.IntVar(value=3)
        tk.Spinbox(inner, from_=1, to=8, textvariable=self.frames_var, width=4,
                   bg="#0d1b2a", fg=self.TEXT, buttonbackground=self.ACCENT,
                   font=("Segoe UI", 11), relief="flat").grid(row=0, column=4, padx=(0,16))

        # Algoritmo
        tk.Label(inner, text="Algoritmo:", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 10)).grid(row=0, column=5, sticky="w", padx=(0,8))
        self.algo_var = tk.StringVar(value="FIFO")
        algo_cb = ttk.Combobox(inner, textvariable=self.algo_var,
                               values=["FIFO", "LRU", "OPT (Óptimo)", "Clock"],
                               state="readonly", width=14, font=("Segoe UI", 10))
        algo_cb.grid(row=0, column=6, padx=(0,16))

        tk.Button(inner, text="▶  Simular", command=self._simulate,
                  bg=self.BLUE, fg="#000", font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2", padx=14, pady=4).grid(row=0, column=7)

        # ── COMPARAR TODOS ──
        cmp_frame = tk.Frame(self.root, bg=self.BG)
        cmp_frame.pack(fill="x", padx=20)
        tk.Button(cmp_frame, text="📊  Comparar todos los algoritmos",
                  command=self._compare_all, bg=self.GOLD, fg="#000",
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  padx=12, pady=3).pack(side="left")

        # ── ÁREA DE RESULTADOS ──
        self.result_outer = tk.Frame(self.root, bg=self.BG)
        self.result_outer.pack(fill="both", expand=True, padx=20, pady=10)

        # Canvas con scroll horizontal
        self.canvas = tk.Canvas(self.result_outer, bg=self.BG, highlightthickness=0)
        self.hscroll = ttk.Scrollbar(self.result_outer, orient="horizontal",
                                     command=self.canvas.xview)
        self.vscroll = ttk.Scrollbar(self.result_outer, orient="vertical",
                                     command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hscroll.set,
                               yscrollcommand=self.vscroll.set)

        self.hscroll.pack(side="bottom", fill="x")
        self.vscroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg=self.BG)
        self.canvas_window = self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

    # ── GENERADOR ALEATORIO ──────────────────────
    def _gen_random(self):
        n = random.randint(15, 25)
        pages = [random.randint(0, 9) for _ in range(n)]
        self.pages_var.set(" ".join(map(str, pages)))

    # ── LEER ENTRADAS ────────────────────────────
    def _parse_input(self):
        try:
            raw = self.pages_var.get().strip()
            pages = list(map(int, raw.split()))
            if not pages:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingresa una cadena de números separados por espacios.")
            return None, None
        frames = self.frames_var.get()
        if frames < 1:
            messagebox.showerror("Error", "El número de marcos debe ser ≥ 1.")
            return None, None
        return pages, frames

    def _run_algo(self, name, pages, frames):
        if "FIFO" in name:
            return fifo(pages, frames)
        elif "LRU" in name:
            return lru(pages, frames)
        elif "OPT" in name:
            return optimal(pages, frames)
        elif "Clock" in name:
            return clock(pages, frames)

    # ── SIMULAR ──────────────────────────────────
    def _simulate(self):
        pages, frames = self._parse_input()
        if pages is None:
            return
        algo = self.algo_var.get()
        history, faults = self._run_algo(algo, pages, frames)
        self._render_table(algo, history, faults, frames, pages)

    # ── COMPARAR TODOS ───────────────────────────
    def _compare_all(self):
        pages, frames = self._parse_input()
        if pages is None:
            return

        for w in self.inner_frame.winfo_children():
            w.destroy()

        algos = ["FIFO", "LRU", "OPT (Óptimo)", "Clock"]
        results = {}
        for a in algos:
            h, f = self._run_algo(a, pages, frames)
            results[a] = (h, f)

        # Resumen de fallos
        summary = tk.Frame(self.inner_frame, bg=self.PANEL)
        summary.pack(fill="x", pady=(0, 12))
        tk.Label(summary, text="Comparación de fallos de página",
                 bg=self.PANEL, fg=self.GOLD,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(8,4))
        row_f = tk.Frame(summary, bg=self.PANEL)
        row_f.pack(padx=12, pady=(0,10))

        best = min(results, key=lambda a: results[a][1])
        for a in algos:
            _, f = results[a]
            color = self.GREEN if a == best else self.TEXT
            box = tk.Frame(row_f, bg=self.ACCENT, bd=0)
            box.pack(side="left", padx=6, ipadx=10, ipady=6)
            tk.Label(box, text=a, bg=self.ACCENT, fg=self.MUTED,
                     font=("Segoe UI", 9)).pack()
            tk.Label(box, text=f"{f} fallos", bg=self.ACCENT, fg=color,
                     font=("Segoe UI", 12, "bold")).pack()
            if a == best:
                tk.Label(box, text="★ mejor", bg=self.ACCENT, fg=self.GOLD,
                         font=("Segoe UI", 8)).pack()

        # Tablas individuales
        for a in algos:
            h, f = results[a]
            self._render_table(a, h, f, frames, pages, container=self.inner_frame)

    # ── RENDERIZAR TABLA ─────────────────────────
    def _render_table(self, algo, history, faults, frames, pages, container=None):
        if container is None:
            for w in self.inner_frame.winfo_children():
                w.destroy()
            container = self.inner_frame

        CELL_W = 44
        CELL_H = 28

        section = tk.Frame(container, bg=self.BG)
        section.pack(fill="x", pady=4)

        # Encabezado
        hdr = tk.Frame(section, bg=self.PANEL)
        hdr.pack(fill="x")
        hits = sum(1 for _, _, h in history if h)
        misses = faults
        tk.Label(hdr, text=f"  {algo}",
                 bg=self.PANEL, fg=self.BLUE, font=("Segoe UI", 11, "bold")).pack(side="left", padx=4, pady=6)
        tk.Label(hdr, text=f"  Fallos: {misses}",
                 bg=self.PANEL, fg=self.RED, font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)
        tk.Label(hdr, text=f"Hits: {hits}",
                 bg=self.PANEL, fg=self.GREEN, font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)
        rate = misses / len(pages) * 100
        tk.Label(hdr, text=f"Tasa de fallos: {rate:.1f}%",
                 bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 9)).pack(side="left", padx=10)

        # Tabla con canvas
        table_canvas = tk.Canvas(section, bg=self.BG, highlightthickness=0)
        table_canvas.pack(fill="x", pady=2)

        cols = len(history)
        total_w = CELL_W * (cols + 1) + 10
        total_h = CELL_H * (frames + 2) + 10
        table_canvas.configure(width=min(total_w, 980), height=total_h)
        table_canvas.configure(scrollregion=(0, 0, total_w, total_h))

        # Fila header: "Marco" + números de referencia
        table_canvas.create_rectangle(2, 2, CELL_W, CELL_H+2,
                                      fill=self.ACCENT, outline="")
        table_canvas.create_text(CELL_W//2 + 2, CELL_H//2 + 2,
                                  text="Frame", fill=self.MUTED,
                                  font=("Segoe UI", 7, "bold"))

        for ci, (page, mem, hit) in enumerate(history):
            x0 = CELL_W + ci * CELL_W + 2
            x1 = x0 + CELL_W
            color = self.GREEN if hit else self.RED
            table_canvas.create_rectangle(x0, 2, x1, CELL_H+2,
                                           fill=self.ACCENT, outline=self.BG, width=1)
            table_canvas.create_text((x0+x1)//2, CELL_H//2 + 2,
                                      text=str(page), fill=color,
                                      font=("Consolas", 10, "bold"))

        # Filas de marcos
        for fi in range(frames):
            y0 = CELL_H * (fi + 1) + 2
            y1 = y0 + CELL_H
            # etiqueta fila
            table_canvas.create_rectangle(2, y0, CELL_W, y1,
                                           fill=self.ACCENT, outline=self.BG)
            table_canvas.create_text(CELL_W//2 + 2, (y0+y1)//2,
                                      text=f"M{fi}", fill=self.MUTED,
                                      font=("Segoe UI", 8, "bold"))
            for ci, (page, mem, hit) in enumerate(history):
                x0 = CELL_W + ci * CELL_W + 2
                x1 = x0 + CELL_W
                val = str(mem[fi]) if fi < len(mem) else ""
                is_new = (not hit) and (fi < len(mem)) and (str(mem[fi]) == str(page))
                bg = "#1b4332" if (is_new and val) else "#0d1b2a"
                fg = self.GREEN if is_new and val else self.TEXT
                table_canvas.create_rectangle(x0, y0, x1, y1,
                                               fill=bg, outline=self.BG, width=1)
                if val:
                    table_canvas.create_text((x0+x1)//2, (y0+y1)//2,
                                              text=val, fill=fg,
                                              font=("Consolas", 9))

        # Fila F/H (fallo / hit)
        y0 = CELL_H * (frames + 1) + 2
        y1 = y0 + CELL_H
        table_canvas.create_rectangle(2, y0, CELL_W, y1,
                                       fill=self.ACCENT, outline=self.BG)
        table_canvas.create_text(CELL_W//2 + 2, (y0+y1)//2,
                                  text="F/H", fill=self.MUTED, font=("Segoe UI", 8, "bold"))
        for ci, (page, mem, hit) in enumerate(history):
            x0 = CELL_W + ci * CELL_W + 2
            x1 = x0 + CELL_W
            label = "H" if hit else "F"
            fg = self.GREEN if hit else self.RED
            bg = "#1b4332" if hit else "#3d0000"
            table_canvas.create_rectangle(x0, y0, x1, y1,
                                           fill=bg, outline=self.BG, width=1)
            table_canvas.create_text((x0+x1)//2, (y0+y1)//2,
                                      text=label, fill=fg,
                                      font=("Consolas", 9, "bold"))


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground="#0d1b2a", background="#0d1b2a",
                    foreground="#e0e0e0", selectbackground="#0f3460")
    app = SimuladorApp(root)
    root.mainloop()
