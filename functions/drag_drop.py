import flet as ft
from flet import GridView
from flet import *
from views.components.ItemCard import ItemCard, DraggableItemCard

class DragDrop(GridView):

    def __init__(self, expand=1, max_extent=300, child_aspect_ratio=1.40, spacing=10, run_spacing=10, padding=padding.all(5)):
        super().__init__(
            expand=expand,
            max_extent=max_extent,
            child_aspect_ratio=child_aspect_ratio,
            spacing=spacing,
            run_spacing=run_spacing,
            padding=padding,
        )
        self.draggable = True
        self.on_drag_start = self._on_drag_start
        self.on_drag_end = self._on_drag_end
        self.on_drag_enter = self._on_drag_enter
        self.on_drag_leave = self._on_drag_leave
        self.on_drag_over = self._on_drag_over
        self.on_drop = self._on_drop
        self._drag_data = None

    def _on_drag_start(self, e):
        # Get the item being dragged
        item_card = e.control.content
        self._drag_data = item_card.item_dict

    def _on_drag_end(self, e):
        print("Drag ended")

    def _on_drag_enter(self, e):
        print("Drag entered")

    def _on_drag_leave(self, e):
        print("Drag left")

    def _on_drag_over(self, e):
        print("Drag over")

    def _on_drop(self, e):
        # Get the item being dropped
        item_dict = self._drag_data
        # Get the target container
        target_container = e.control
        # Add the item to the target container
        target_container.content.controls.append(
            Container(
                content=DraggableItemCard(item_dict=item_dict, handle_detailed_view=ItemCard().handle_detailed_view),
                alignment=alignment.center,
            )
        )
        print("Item dropped")
