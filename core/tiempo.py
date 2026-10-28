"""Límite de tiempo para cálculos simbólicos (SymPy puede quedarse pensando en casos raros)."""
from __future__ import annotations

import queue
import threading


class Tarda(TimeoutError):
    pass


def con_tiempo(fn, *args, segundos: float = 12, **kwargs):
    """Ejecuta fn(*args) en un hilo «daemon» y lanza Tarda si se pasa del tiempo.
    (El hilo atascado no impide cerrar la app.)"""
    q: queue.Queue = queue.Queue(maxsize=1)

    def trabajo():
        try:
            q.put((True, fn(*args, **kwargs)))
        except BaseException as exc:  # noqa: BLE001
            q.put((False, exc))
    threading.Thread(target=trabajo, daemon=True).start()
    try:
        ok, val = q.get(timeout=segundos)
    except queue.Empty as exc:
        raise Tarda(f"El cálculo simbólico tarda más de {segundos:.0f} s; prueba con una expresión más sencilla.") from exc
    if ok:
        return val
    raise val
