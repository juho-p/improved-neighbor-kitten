import kitty
import kitty.boss
from kitty.window import Window
from kitty.constants import WindowGeometry
from kitty.layout.splits import Splits
from kittens.tui.loop import debug
from kittens.tui.handler import result_handler
from typing import cast, List, Optional, Tuple

from typing import List

def main(args: List[str]) -> None:
    pass

@result_handler(no_ui=True)
def handle_result(args: List[str], answer: str, target_window_id: int, boss: kitty.boss.Boss) -> None:
    _, operation, direction = args

    w: Optional[Window] = boss.window_id_map.get(target_window_id)
    if w is None:
        return
    tab = boss.tab_for_window(w)
    if tab is None:
        return

    layout = tab.current_layout
    neighbors = layout.neighbors_for_window(w, tab.windows)

    neighbor_ids = cast(List[int], neighbors.get(direction))
    groups = dict((g.id, g) for g in tab.windows.groups)
    neighbor_groups = [groups[group_id] for group_id in neighbor_ids]

    candidates = dict((x.id, x) for x in neighbor_groups
            if x.geometry is not None and is_really_neighbor(w.geometry, x.geometry, direction))

    target = None
    for window_id in reversed(tab.windows.active_window_history):
        cand = candidates.get(window_id)
        if cand:
            target = cand
            break
    target = target or next(iter(candidates.values()), None)

    if not target:
        return

    if operation == 'activate':
        tab.windows.set_active_group(target.id)
    elif operation == 'move' and isinstance(layout, Splits):
        split_move_hack(tab, layout, tab.windows, target.id)

def split_move_hack(tab: kitty.tabs.Tab,
        layout: Splits,
        all_windows: kitty.window_list.WindowList,
        target_group: int) -> None:
    # horrible copy paste hack from Splits-layout. Will most likely break in future Kitty versions!
    before = all_windows.active_group
    if before is None:
        return
    before_idx = all_windows.active_group_idx
    moved = tab.windows.move_window_group(to_group=target_group)
    after = all_windows.groups[before_idx]
    if moved and before.id != after.id:
        layout.pairs_root.swap_windows(before.id, after.id)

    if moved:
        tab.relayout()

def is_really_neighbor(a: WindowGeometry, b: WindowGeometry, direction: str) -> bool:
    start_attr, end_attr = \
        ('top', 'bottom') if direction in ['left', 'right'] else \
        ('left', 'right')
    
    def edge(g: WindowGeometry) -> Tuple[int, int]:
        return getattr(g, start_attr), getattr(g, end_attr)

    a1, a2 = edge(a)
    b1, b2 = edge(b)

    if a1 >= b2:
        return False
    if a2 <= b1:
        return False

    return True
