# src/utils.py

def box(text: str, width_padding: int = 2, style: str = "ascii") -> None:
    """
    Imprime `text` encerrado en un recuadro.
    - width_padding: espacios a cada lado del texto.
    - style: "ascii" (─│┌┐└┘) o "simple" (- | +).
    """
    
    if style == "ascii":
        h, v, tl, tr, bl, br = "─", "│", "┌", "┐", "└", "┘"
    else:
        h, v, tl, tr, bl, br = "-", "|", "+", "+", "+", "+"

    inner = " " * width_padding + text + " " * width_padding
    line_top    = tl + h * len(inner) + tr
    line_middle = f"{v}{inner}{v}"
    line_bot    = bl + h * len(inner) + br

    print(line_top)
    print(line_middle)
    print(line_bot)

def success(msg: str) -> None:
    """Mensaje de éxito con icono verde."""
    print(f"✅ {msg}")

def error(msg: str) -> None:
    """Mensaje de error con icono rojo."""
    print(f"❌ {msg}")